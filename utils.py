import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
from openai import OpenAI
from collections import Counter
import re
from newspaper import Article
import gspread
from google.oauth2.credentials import Credentials
import feedparser

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_text(text, max_tokens=350):
    prompt = (
        "You are a policy analyst writing for a professional audience in planning, housing, infrastructure, and governance. "
        "Summarize the following article in 3–5 concise sentences. "
        "Include: (1) what happened, (2) why it matters, and (3) any relevance to planners, developers, housing officials, or civic leaders.\n\n"
        "Avoid generalities, focus on specifics. Be objective but insightful. Write clearly and professionally.\n\n"
        f"Article:\n{text}"
    )
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("⚠️ GPT Summary Error:", e)
        return None

def extract_tags(title, summary, max_tags=5):
    """Extract basic tags from title and summary"""
    text = f"{title} {summary}"
    words = re.findall(r"\b\w{5,}\b", text.lower())  # filter short/common words
    stopwords = {"about", "which", "their", "would", "could", "should", "therefore", "however"}
    filtered = [word for word in words if word not in stopwords]
    common = Counter(filtered).most_common(max_tags)
    return [tag for tag, _ in common]

def get_full_article_text(url):
    """Extract article text using newspaper3k library or fallback to requests"""
    # Special handling for federalregister.gov URLs which have redirect issues
    if "federalregister.gov" in url:
        try:
            response = requests.get(url, allow_redirects=True, timeout=10)
            if response.status_code == 200:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')
                content_div = soup.find('div', class_='body-content')
                if content_div:
                    return content_div.get_text(separator='\n', strip=True)
                return soup.get_text(separator='\n', strip=True)
            else:
                return None
        except Exception as e:
            return None
    
    # For other URLs, use newspaper3k
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        return None

def log_to_gsheet(date, category, title, link, summary, tags, published_iso):
    """Log article to Google Sheet"""
    try:
        creds = Credentials.from_authorized_user_file('token.json', ['https://www.googleapis.com/auth/spreadsheets'])
        client = gspread.authorize(creds)
        sheet = client.open("Exelant News Log").sheet1
        
        # Prepare tags as a comma-separated string
        tags_str = ", ".join(tags)
        
        # Append row with all necessary article data
        sheet.append_row([date, category, title, link, summary, tags_str, published_iso])
        print(f"✅ Logged to sheet: {title}")
        return True
    except Exception as e:
        print(f"⚠️ Error logging to sheet: {e}")
        return False

def post_to_wordpress(title, content, category_name="News Bot", tags=None):
    url = f"{os.getenv('WP_URL')}/wp-json/wp/v2/posts"
    auth = (os.getenv("WP_USER"), os.getenv("WP_PASS"))

    # Create tags if needed
    tag_ids = []
    if tags:
        for tag in tags:
            tag_res = requests.get(f"{os.getenv('WP_URL')}/wp-json/wp/v2/tags", params={"search": tag}, auth=auth)
            existing = tag_res.json()
            if existing:
                tag_ids.append(existing[0]['id'])
            else:
                create_tag = requests.post(f"{os.getenv('WP_URL')}/wp-json/wp/v2/tags", json={"name": tag}, auth=auth)
                if create_tag.status_code == 201:
                    tag_ids.append(create_tag.json()["id"])

    # Get category ID dynamically based on category_name
    cat_res = requests.get(f"{os.getenv('WP_URL')}/wp-json/wp/v2/categories", params={"search": category_name}, auth=auth)
    if cat_res.status_code == 200 and cat_res.json():
        category_id = cat_res.json()[0]["id"]
    else:
        category_id = 11  # fallback to News Bot

    payload = {
        "title": title,
        "content": content,
        "status": "publish",
        "categories": [category_id],
        "tags": tag_ids
    }

    response = requests.post(url, json=payload, auth=auth)
    return response.status_code == 201


def fetch_recent_articles(url, days_back=1):
    """Fetch articles from RSS feed that were published within `days_back`."""
    articles = []
    try:
        feed = feedparser.parse(url)
    except Exception as e:
        print(f"⚠️ Error parsing RSS feed {url}: {e}")
        return []

    cutoff = datetime.now() - timedelta(days=days_back)

    for entry in feed.entries:
        try:
            published = datetime(*entry.published_parsed[:6])
            if published >= cutoff:
                articles.append({
                    "title": entry.title,
                    "link": entry.link,
                    "published": published.strftime("%Y-%m-%d"),
                    "published_iso": published.isoformat(),
                    "summary": entry.get("summary", "")
                })
        except Exception as e:
            print(f"⚠️ Error parsing article date: {e}")
            continue

    return articles

def process_article(article):
    """Get article text, summarize, return HTML block and tags."""
    skip_sources = [
        "flsenate.gov/Media/VideoPlayer",
        "thefloridachannel.org/videos",
        "govinfo.gov/app/details"
    ]
    if any(skip in article["link"] for skip in skip_sources):
        print(f"⏭️ Skipping media or metadata-only link: {article['link']}")
        return "", None, []

    full_text = get_full_article_text(article["link"])
    if not full_text:
        full_text = f"Title: {article['title']}\nLink: {article['link']}\nSummary: {article.get('summary', '')}"

    full_text = full_text[:8000]  # Truncate to avoid GPT token limits

    # Summarize the article
    summary = summarize_text(full_text)
    
    # Check if the summary starts with error-related words (e.g., "sorry," "unable," etc.)
    error_phrases = ["sorry", "apologies", "unable", "can't", "not available"]
    if summary and any(summary.lower().startswith(phrase) for phrase in error_phrases):
        print(f"⚠️ GPT summary failed for: {article['title']} - Skipping this article")
        return "", None, []  # Skip the article if GPT cannot summarize it properly

    if not summary:
        print(f"⚠️ Summary failed for: {article['title']}")
        return "", None, []  # If GPT didn't return a summary, skip the article

    # Extract tags based on title and summary
    tags = extract_tags(article["title"], summary)

    # Format HTML block for the article
    html = f"""
        <article class="news-article">
            <h4 class="news-title"><a href="{article['link']}" target="_blank">{article['title']}</a></h4>
            <time class="news-date">{article['published']}</time>
            <div class="news-summary"><p>{summary}</p></div>
        </article>
        <hr/>
    """

    return html, summary, tags


def run_bot():
    today = datetime.now().strftime("%m/%d")
    full_html = "<h2>TLDR: Daily Summary</h2>"

    all_tags = set()
    category_summaries = {}

    # Fetch articles by category
    for category, urls in rss_feeds.items():
        # Dynamically set the post title based on category and date
        post_title = f"TLDR on {category} - {today}"
        category_summary = f"<h3>{category} – {today}</h3><hr>"  # Add category name and date
        
        for url in urls:
            articles = fetch_recent_articles(url)
            for article in articles:
                html_block, summary, tags = process_article(article)
                if not html_block:
                    continue  # Skip if GPT couldn't process the article

                category_summary += html_block
                all_tags.update(tags)

                # Log the full article metadata to Google Sheets
                log_to_gsheet(
                    article["published"],
                    category,
                    article["title"],
                    article["link"],
                    summary,
                    tags,
                    article["published_iso"]
                )

        # Add the category summary to the full HTML
        category_summaries[category] = category_summary

    # Combine category summaries into the full HTML for the post
    for category, summary in category_summaries.items():
        full_html += f"<h4>{category} Summary</h4>{summary}"

    # Publish daily summary to WordPress
    post_to_wordpress(post_title, full_html, category_name="News Bot", tags=list(all_tags))


if __name__ == "__main__":
    run_bot()
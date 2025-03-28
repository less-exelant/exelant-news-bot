import os
import feedparser
from datetime import datetime, timedelta
from utils import (
    summarize_text,
    post_to_wordpress,
    log_to_gsheet,
    get_full_article_text,
    extract_tags
)
from rss_feeds import rss_feeds

# Available tags for categorization
available_tags = [
    "Urban Planning", "Affordable Housing", "Housing Policy", "Zoning Laws", "Real Estate",
    "Infrastructure", "Sustainability", "Federal Law", "State Law", "Technology",
    "Economic Development", "Transit-Oriented Development", "Community Development", "Public Policy", "Smart Cities"
]

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

def process_article(article, category):
    """Get article text, summarize, return HTML block and tags."""
    # Skip known non-article/video URLs
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

    # Summarize
    summary = summarize_text(full_text)
    if not summary:
        print(f"⚠️ Summary failed for: {article['title']}")
        return "", None, []

    # Extract tags
    tags = extract_tags(article["title"], summary)

    # Format HTML
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
    post_title = f"TLDR on [category] - {today}"  # This will be replaced dynamically per category
    full_html = "<h2>TLDR: Daily Summary</h2>"

    all_tags = set()
    category_summaries = {}

    # Fetch articles by category
    for category, urls in rss_feeds.items():
        category_summary = f"<h3>{category} – {today}</h3><hr>"  # Add category name and date
        for url in urls:
            articles = fetch_recent_articles(url)
            for article in articles:
                html_block, summary, tags = process_article(article, category)
                if not html_block:
                    continue

                category_summary += html_block
                all_tags.update(tags)

                # Log the full article metadata
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

    # Combine category summaries into the full HTML
    for category, summary in category_summaries.items():
        full_html += summary

    # Publish daily summary to WordPress
    post_to_wordpress(post_title, full_html, category_name="News Bot", tags=list(all_tags))


if __name__ == "__main__":
    run_bot()
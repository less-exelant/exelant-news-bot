# **Exelant News Bot**

This bot fetches news articles from various RSS feeds, summarizes them using GPT-4, logs metadata to Google Sheets, and posts the summaries to WordPress. It categorizes the articles based on predefined topics and includes tags and summaries.

---

## **Requirements**

Before you begin, ensure you have the following:

- **Python 3.x** installed.
- **API keys** for OpenAI (GPT-4) and WordPress.
- **Google Sheets API credentials** for logging article data.
- **Environment variables** to store sensitive information securely.

---

## **Setup Instructions**

### 1. Clone the Repository

If you haven’t already, clone the repository to your local machine:

```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Install Dependencies

Install the required dependencies via pip:
pip install -r requirements.txt
The requirements.txt file includes:
	•	openai: For GPT-4 summarization.
	•	feedparser: For parsing RSS feeds.
	•	requests: For sending HTTP requests to WordPress.
	•	gspread: For interacting with Google Sheets.
	•	newspaper3k: For extracting full article content.
	•	python-dotenv: For managing environment variables.
	•	beautifulsoup4: For parsing HTML content if necessary.

### 3. Set Up Environment Variables

Create a .env file in the project directory and add the following environment variables:
OPENAI_API_KEY=your-openai-api-key
WP_URL=your-wordpress-site-url
WP_USER=your-wordpress-username
WP_PASS=your-wordpress-password
GOOGLE_SHEET_ID=your-google-sheet-id
GOOGLE_SHEET_NAME=your-google-sheet-name

Replace the placeholder values with your actual keys and credentials:
	•	OPENAI_API_KEY: Your OpenAI GPT-4 API key.
	•	WP_URL: Your WordPress site URL.
	•	WP_USER: Your WordPress username.
	•	WP_PASS: Your WordPress password.
	•	GOOGLE_SHEET_ID: The ID of your Google Sheets document.
	•	GOOGLE_SHEET_NAME: The name of the sheet where article metadata will be logged.

### 4. Authenticate Google Sheets API

You need to authenticate the Google Sheets API to log article data.
	1.	Set up Google Sheets API: Follow the steps in Google Sheets API Quickstart to enable the API and download your credentials.json file.
	2.	Rename the downloaded credentials file to credentials.json and place it in the project directory.
	3.	Authenticate: Run the following command to authenticate and generate a token.json file:

```python gsheet_auth.py```

### 5. Verify and Run

After setting everything up, you can run the bot:

```python news_bot.py```

This will:
	•	Fetch articles from the defined RSS feeds.
	•	Summarize each article using GPT-4.
	•	Log article metadata to Google Sheets.
	•	Post the summaries to WordPress.

### 6. Logs and Errors

Check the following places for logs:
	•	Console output: The bot prints logs for errors, skipped links, and successful operations in the terminal.
	•	Google Sheets: Article metadata (title, summary, category, tags, etc.) will be logged in your specified Google Sheets.
	•	WordPress: The summaries will be published as new posts in WordPress.

## Troubleshooting

Common Issues
	•	Google Sheets Authentication: Ensure that you have the correct credentials.json and have authenticated with gsheet_auth.py.
	•	GPT-4 Summary Errors: If GPT-4 cannot summarize an article, the bot will skip it, logging a “summary failed” message.
	•	RSS Feed Parsing: Ensure that the URLs in the rss_feeds configuration are valid and the feed is accessible.

Bot Configuration

The bot is configured with several RSS feed categories. You can modify the rss_feeds dictionary in the news_bot.py file to add or remove categories:

## Customizing Tags

Tags are extracted automatically based on the article title and summary. If you want to adjust the tags, modify the available_tags list in the code.
You can also modify the extract_tags() function to improve how tags are extracted based on your specific needs.

## Contributing

If you find bugs or want to add new features, feel free to fork the repository and submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For any questions or feedback, feel free to reach out to me by [email](aposes@exelant.io) or visit [exelant](exelant.io).




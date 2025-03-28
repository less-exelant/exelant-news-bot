#!/bin/bash

# Activate the virtual environment
source /Users/alexadraposes/exelant-news-bot/.venv/bin/activate

# Authenticate Google Sheets API (if needed)
python /Users/alexadraposes/exelant-news-bot/gsheet_auth.py

# Run the news bot script
python /Users/alexadraposes/exelant-news-bot/news_bot.py
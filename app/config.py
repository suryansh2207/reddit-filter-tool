# app/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask configuration
    SECRET_KEY = os.urandom(24)
    
    # Reddit API credentials
    REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
    REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
    REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT', 'RedditSearchTool/1.0')
    REDDIT_REDIRECT_URI = os.getenv('REDDIT_REDIRECT_URI', 'http://127.0.0.1:5000/callback')
    
    # Session configuration
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False
    PERMANENT_SESSION_LIFETIME = 3600  # Session lifetime in seconds (1 hour)
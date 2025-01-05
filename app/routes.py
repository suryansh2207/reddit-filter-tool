# app/routes.py
from flask import Blueprint, render_template, redirect, request, session, url_for, jsonify
from functools import wraps
import praw
from prawcore import NotFound
from .config import Config
import random
import string
from datetime import datetime, timezone

main = Blueprint('main', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'reddit_refresh_token' not in session:
            return redirect(url_for('main.login'))
        return f(*args, **kwargs)
    return decorated_function

@main.route('/')
@login_required
def index():
    return render_template('search.html')

@main.route('/login')
def login():
    if 'reddit_refresh_token' in session:
        return redirect(url_for('main.index'))
    
    reddit = praw.Reddit(
        client_id=Config.REDDIT_CLIENT_ID,
        client_secret=Config.REDDIT_CLIENT_SECRET,
        redirect_uri=Config.REDDIT_REDIRECT_URI,
        user_agent=Config.REDDIT_USER_AGENT
    )
    
    state = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    session['state'] = state
    auth_url = reddit.auth.url(['identity', 'read', 'history'], state, 'permanent')
    
    return render_template('login.html', auth_url=auth_url)

@main.route('/callback')
def callback():
    error = request.args.get('error')
    if error:
        return render_template('login.html', error=error)
    
    state = request.args.get('state')
    if state != session.get('state'):
        return render_template('login.html', error="Invalid state parameter")
    
    code = request.args.get('code')
    
    try:
        reddit = praw.Reddit(
            client_id=Config.REDDIT_CLIENT_ID,
            client_secret=Config.REDDIT_CLIENT_SECRET,
            redirect_uri=Config.REDDIT_REDIRECT_URI,
            user_agent=Config.REDDIT_USER_AGENT
        )
        
        refresh_token = reddit.auth.authorize(code)
        session['reddit_refresh_token'] = refresh_token
        
        # Get username
        reddit_user = reddit.user.me()
        session['reddit_username'] = reddit_user.name
        
        return redirect(url_for('main.index'))
    except Exception as e:
        return render_template('login.html', error=str(e))

@main.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.login'))

@main.route('/api/search')
@login_required
def api_search():
    subreddit = request.args.get('subreddit', '')
    keywords = request.args.get('keywords', '').split(',')
    sort = request.args.get('sort', 'new')
    limit = min(int(request.args.get('limit', 100)), 100)
    
    reddit = praw.Reddit(
        client_id=Config.REDDIT_CLIENT_ID,
        client_secret=Config.REDDIT_CLIENT_SECRET,
        refresh_token=session['reddit_refresh_token'],
        user_agent=Config.REDDIT_USER_AGENT
    )
    
    try:
        results = search_subreddit(reddit, subreddit, keywords, sort, limit)
        formatted_results = format_search_results(results)
        return jsonify(formatted_results)
    except NotFound:
        return jsonify({"error": "Subreddit not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


def search_subreddit(reddit, subreddit_name, keywords, sort='new', limit=25):
    try:
        subreddit = reddit.subreddit(subreddit_name)
        search_query = ' OR '.join(keywords)
        
        if sort == 'new':
            posts = subreddit.new(limit=limit)
        elif sort == 'hot':
            posts = subreddit.hot(limit=limit)
        elif sort == 'top':
            posts = subreddit.top(limit=limit)
        else:
            posts = subreddit.new(limit=limit)
            
        results = []
        for post in posts:
            if any(keyword.lower() in post.title.lower() or 
                  (post.selftext and keyword.lower() in post.selftext.lower()) 
                  for keyword in keywords):
                results.append({
                    'title': post.title,
                    'url': f"https://reddit.com{post.permalink}",
                    'score': post.score,
                    'num_comments': post.num_comments,
                    'created_utc': post.created_utc,
                    'author': str(post.author),
                    'is_self': post.is_self,
                    'thumbnail': post.thumbnail if hasattr(post, 'thumbnail') else None
                })
                
        return results
    except Exception as e:
        print(f"Error searching subreddit: {str(e)}")
        raise

def format_search_results(results):
    formatted_results = []
    for post in results:
        time_ago = format_time_ago(post['created_utc'])
        formatted_results.append({
            'title': post['title'],
            'url': post['url'],
            'score': format_number(post['score']),
            'num_comments': format_number(post['num_comments']),
            'author': post['author'],
            'time_ago': time_ago,
            'thumbnail': post['thumbnail'] if post['thumbnail'] and post['thumbnail'] not in ['self', 'default'] else None
        })
    return formatted_results

def format_number(num):
    if num >= 1000000:
        return f"{num/1000000:.1f}M"
    if num >= 1000:
        return f"{num/1000:.1f}K"
    return str(num)

def format_time_ago(created_utc):
    now = datetime.now(timezone.utc)
    created = datetime.fromtimestamp(created_utc, timezone.utc)
    diff = now - created
    
    seconds = diff.total_seconds()
    if seconds < 60:
        return "just now"
    elif seconds < 3600:
        minutes = int(seconds / 60)
        return f"{minutes}m ago"
    elif seconds < 86400:
        hours = int(seconds / 3600)
        return f"{hours}h ago"
    else:
        days = int(seconds / 86400)
        return f"{days}d ago"
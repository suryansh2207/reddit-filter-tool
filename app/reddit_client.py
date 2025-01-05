import praw
from prawcore import NotFound
from flask import session

def get_reddit_instance():
    if 'reddit_refresh_token' in session:
        return praw.Reddit(
            client_id="tL0fmz_JNzCbEBrbTIxCgA",
            client_secret="wGxOpFfEJlDCvEWxWwam0_dlQpEgkw",
            user_agent="my_reddit_bot/1.0",
            refresh_token=session['reddit_refresh_token']
        )
    return None

def search_subreddit(reddit, subreddit_name, keywords, sort='new', limit=25):
    try:
        subreddit = reddit.subreddit(subreddit_name)
        search_query = ' OR '.join(keywords)
        
        # Get posts based on sorting option
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
            # Check if post contains any of the keywords
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
    except NotFound:
        return []
    except Exception as e:
        print(f"Error searching subreddit: {str(e)}")
        return []
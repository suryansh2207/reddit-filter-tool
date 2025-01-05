from flask import Flask, flash, render_template, request, redirect, session, url_for
import praw
import prawcore

# Reddit API credentials
REDDIT_CLIENT_ID = "your_id"
REDDIT_CLIENT_SECRET = "your_secret"
REDDIT_USER_AGENT = "your_agent"
REDDIT_REDIRECT_URI = "your_redirect_url"

# Initialize PRAW
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    redirect_uri=REDDIT_REDIRECT_URI,
    user_agent=REDDIT_USER_AGENT,
)

def init_app(app: Flask):
    @app.route("/")
    def index():
        if "username" in session:
            return redirect(url_for("home"))
        auth_url = reddit.auth.url(["identity"], "random_string", "permanent")
        return render_template("index.html", auth_url=auth_url)

    @app.route("/callback")
    def callback():
        code = request.args.get("code")
        state = request.args.get("state")  # Retrieve the state parameter if used for CSRF protection
        print("Received code:", code)
        print("Received state:", state)

        if code:
            try:
                reddit.auth.authorize(code)
                session["username"] = reddit.user.me().name
                return redirect(url_for("home"))
            except prawcore.exceptions.ResponseException as e:
                print("Response Exception:", e.response)  # Debugging line
                return "Authorization failed: " + str(e), 400
            except Exception as e:
                print("General Exception:", e)
                return "Authorization failed", 400
        return "No code provided", 400

    @app.route('/home', methods=['GET', 'POST'])
    def home():
        if request.method == 'POST':
            subreddit_name = request.form['subreddit']
            keywords = request.form['keywords'].split(',')
            sort = request.form['sort']
            limit = int(request.form['limit'])

            try:
                subreddit = reddit.subreddit(subreddit_name)
                subreddit_data = subreddit.search(" OR ".join(keywords), sort=sort, limit=limit)

                # Prepare posts data to send to results page
                posts = []
                for submission in subreddit_data:
                    # Include all submissions, but filter later if necessary
                    posts.append({
                        'title': submission.title,
                        'url': submission.url,
                        'score': submission.score,
                        'num_comments': submission.num_comments
                    })

                    print(f"Raw submission: Title: {submission.title}, URL: {submission.url}")

                # Filter posts for valid Reddit URLs if needed
                posts = [post for post in posts if "reddit.com/r/" in post['url'] or "i.redd.it" in post['url']]

                if not posts:
                    flash('No relevant Reddit posts found for your search.', 'warning')

                # Store posts in session and redirect to results route
                session['posts'] = posts
                return redirect(url_for('results'))

            except praw.exceptions.APIException as e:
                flash(f'API error: {e}', 'danger')
                return redirect(url_for('home'))  # Redirect back to home after an error
            except Exception as e:
                flash(f'An error occurred: {e}', 'danger')
                return redirect(url_for('home'))  # Redirect back to home after an error

        return render_template('home.html')

    @app.route("/results")
    def results():
        # Get the posts from the session
        posts = session.get('posts', [])
        return render_template('results.html', posts=posts)


    @app.route("/logout")
    def logout():
        session.clear()
        return redirect(url_for("index"))

# Create and configure the Flask app
app = Flask(__name__)
init_app(app)

if __name__ == "__main__":
    app.run(debug=True)

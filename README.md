# Reddit Filter Tool

This is a web application that allows users to filter and search for Reddit posts based on specific keywords, subreddit, and sorting options. The application uses the Reddit API (PRAW) and Flask for the web framework.

## Features

- User authentication with Reddit
- Search for Reddit posts by subreddit, keywords, and sorting options
- Display search results with post titles, URLs, scores, and number of comments
- Logout functionality

## Prerequisites

- Python 3.x
- Reddit API credentials (client ID, client secret, user agent)

## Getting Started

### 1. Clone the repository

```sh
git clone https://github.com/your-username/reddit-filter-tool.git
cd reddit-filter-tool
```

### 2. Create a virtual environment

```sh
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install dependencies

```sh
pip install -r requirements.txt
```

### 4. Set up Reddit API credentials

Create a .env file in the root directory of the project and add your Reddit API credentials:

```
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=your_user_agent
REDDIT_REDIRECT_URI=http://127.0.0.1:5000/callback
```

You can obtain these credentials by creating an application on the [Reddit Developer Portal](https://www.reddit.com/prefs/apps).

### 5. Run the application

```sh
python run.py
```

The application will be available at `http://127.0.0.1:5000`.

## Project Structure

```
.env
app/
    __init__.py
    config.py
    reddit_client.py
    routes.py
    static/
        style.css
    templates/
        search.html
        login.html
        index.html
        results.html
requirements.txt
run.py
```

- __init__.py: Initializes the Flask application. 

- config.py: Configuration file for Reddit API credentials.

- reddit_client.py: Creates a Reddit client using PRAW.

- routes.py: Defines the routes and logic for the web application.

- style.css: CSS styles for the application.

- templates/: HTML templates for the application.

- requirements.txt: List of dependencies.

- run.py: Entry point to run the Flask application.

## Usage

1. Open your browser and navigate to `http://127.0.0.1:5000`.
2. Click on the "Login with Reddit" button to authenticate with Reddit.
3. After logging in, you will be redirected to the search page.
4. Enter the subreddit, keywordsand sorting option.
5. Click the "Search" button to view the search results.
6. Click on the post titles to view them on Reddit.
7. Use the "Logout" button to log out of the application.

import json
import time
from datetime import datetime
import os
import sys
from urllib import error, request

# --- Configuration ---
CONFIG_FILE = 'scheduler_config.json'
XQUIK_TWEET_URL = os.environ.get('XQUIK_API_URL', 'https://xquik.com/api/v1/x/tweets')

def load_schedule():
    """Loads the posting schedule from the configuration file."""
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Configuration file '{CONFIG_FILE}' not found. Please create one.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{CONFIG_FILE}'.")
        sys.exit(1)

def get_api_key(platform):
    """Retrieves the required API key/token from environment variables."""
    if platform == "mastodon":
        return os.environ.get('MASTODON_ACCESS_TOKEN')
    elif platform == "bluesky":
        # BlueSky commonly uses an application password for bots/apps
        return os.environ.get('BLUESKY_APP_PASSWORD')
    elif platform == "twitter":
        if get_twitter_backend() == "xquik":
            return os.environ.get('XQUIK_API_KEY')
        # Placeholder for X/Twitter API
        return os.environ.get('TWITTER_API_KEY')
    return None

def get_twitter_backend():
    """Returns the configured Twitter/X posting backend."""
    return os.environ.get('TWITTER_BACKEND', 'twitter').strip().lower()

def format_xquik_success(response_data):
    """Formats a concise result for accepted Xquik tweet requests."""
    tweet_url = response_data.get('url')
    if tweet_url:
        return f"SUCCESS: Posted to Twitter/X via Xquik. URL: {tweet_url}"

    write_action_id = response_data.get('writeActionId')
    if write_action_id:
        return f"SUCCESS: Xquik accepted the tweet for posting. Write action ID: {write_action_id}"

    return "SUCCESS: Xquik accepted the tweet for posting."

def post_to_xquik(content, api_key):
    """Posts Twitter/X content through Xquik's REST API."""
    account = os.environ.get('XQUIK_ACCOUNT')
    if not account:
        return "FAILURE: Missing XQUIK_ACCOUNT for Xquik Twitter/X posting."

    payload = json.dumps({
        "account": account,
        "text": content,
    }).encode("utf-8")

    post_request = request.Request(
        XQUIK_TWEET_URL,
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with request.urlopen(post_request, timeout=30) as response:
            response_body = response.read().decode("utf-8")
            response_data = json.loads(response_body) if response_body else {}
            if response.getcode() in (200, 202):
                return format_xquik_success(response_data)
            return f"FAILURE: Xquik returned HTTP {response.getcode()}."
    except error.HTTPError as exc:
        return f"FAILURE: Xquik returned HTTP {exc.code}."
    except error.URLError as exc:
        return f"FAILURE: Could not reach Xquik. Error: {exc.reason}"

def simulate_post(platform, content):
    """
    Simulates posting content to a social media platform via its API.
    In a real application, this would contain the platform-specific API client logic.
    """
    api_key = get_api_key(platform)
    
    if not api_key:
        # Crucial security failure mode: exit if key is missing
        return f"FAILURE: Missing API Key/Token for {platform}. Set the corresponding environment variable."

    if platform == "mastodon":
        # Mastodon API usage simulation (e.g., toot creation)
        print("-> [MASTODON API] Authenticating with configured token...")
        time.sleep(0.5)
        return f"SUCCESS: Tooted to Mastodon. Content: '{content[:50]}...'"
        
    elif platform == "bluesky":
        # BlueSky API usage simulation (e.g., creation of 'post')
        print("-> [BLUESKY API] Authenticating with configured app password...")
        time.sleep(0.5)
        return f"SUCCESS: Posted to BlueSky. Content: '{content[:50]}...'"

    elif platform == "twitter":
        if get_twitter_backend() == "xquik":
            print("-> [XQUIK API] Sending Twitter/X post through Xquik...")
            return post_to_xquik(content, api_key)

        print("-> [TWITTER/X API] Authenticating and sending tweet...")
        time.sleep(0.5)
        return f"SUCCESS: Posted to Twitter/X. Content: '{content[:50]}...'"
        
    else:
        return f"FAILURE: Unknown platform '{platform}'. Skipping."

def run_scheduler():
    """Checks the schedule and executes posts that are due."""
    schedule_data = load_schedule()

    print("--- Social Media Scheduler Initialized ---")
    
    current_time = datetime.now()
    current_time_str = current_time.strftime("%Y-%m-%d %H:%M")
    print(f"Current System Time: {current_time_str}")

    posts_executed = 0
    
    # Process all scheduled items
    for item in schedule_data.get('scheduled_posts', []):
        try:
            # We assume all scheduled posts in the config file are past the current date 
            # for this simple portfolio demonstration, thus they are 'due'.
            
            # If this were a real cron job, we would check: 
            # scheduled_time = datetime.strptime(item['time'], "%Y-%m-%d %H:%M")
            # if scheduled_time <= current_time: 
            
            print(f"\n[POST DUE] Time: {item['time']} | Platform: {item['platform']}")
            result = simulate_post(item['platform'], item['content'])
            print(result)
            posts_executed += 1

        except ValueError as e:
            print(f"Warning: Skipping malformed schedule item. Error: {e}")

    print(f"\n--- Scheduler Run Complete. {posts_executed} posts attempted. ---")
    print("In production, successfully posted items would be marked as 'done' in the persistent storage.")

if __name__ == "__main__":
    run_scheduler()

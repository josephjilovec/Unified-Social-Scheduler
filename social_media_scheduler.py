import json
import time
from datetime import datetime
import os
import sys

# --- Configuration ---
CONFIG_FILE = 'scheduler_config.json'

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
        # Placeholder for X/Twitter API
        return os.environ.get('TWITTER_API_KEY')
    return None

def simulate_post(platform, content):
    """
    Simulates posting content to a social media platform via its API.
    In a real application, this would contain the platform-specific API client logic.
    """
    api_key = get_api_key(platform)
    
    if not api_key:
        # Crucial security failure mode: exit if key is missing
        return f"FAILURE: Missing API Key/Token for {platform}. Set the corresponding environment variable."

    # Use a truncated key prefix for logging, demonstrating the key was loaded without exposing it
    key_prefix = api_key[:5]

    if platform == "mastodon":
        # Mastodon API usage simulation (e.g., toot creation)
        print(f"-> [MASTODON API] Authenticating using token prefix: {key_prefix}...")
        time.sleep(0.5)
        return f"SUCCESS: Tooted to Mastodon. Content: '{content[:50]}...'"
        
    elif platform == "bluesky":
        # BlueSky API usage simulation (e.g., creation of 'post')
        print(f"-> [BLUESKY API] Authenticating with App Password prefix: {key_prefix}...")
        time.sleep(0.5)
        return f"SUCCESS: Posted to BlueSky. Content: '{content[:50]}...'"

    elif platform == "twitter":
        print(f"-> [TWITTER/X API] Authenticating and sending tweet (Key prefix: {key_prefix})...")
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

Unified Social Scheduler (Cross-Platform Automation Engine)

💡 Why This Exists

Fragmented communication across platforms is a major vector for misaligned incentives and brand dissonance within a company. Custom, proprietary systems are often more reliable and cost-effective than generic SaaS subscriptions, offering tighter control and better integration.

This tool is a proof-of-concept for a centralized, custom-built social media management system.

It demonstrates the ability to:

Integrate with external APIs (simulated here for security and simplicity).

Manage structured data for complex schedules.

Execute time-based, mission-critical tasks (posting on schedule).

Securely handle credentials using environment variables.

The goal is to move clients off costly, generic tools and onto bespoke, automated systems that run cleaner and faster—the definition of an "aligned organism."

🛠️ Setup Instructions

This is a Python CLI application.

Prerequisites: You need Python 3.8+ installed.

Install Dependencies:

pip install -r requirements.txt


Secure Configuration (MANDATORY):
For security, API credentials must be set as environment variables.

MASTODON_ACCESS_TOKEN

BLUESKY_APP_PASSWORD (This is typically an application password, not a user password)

TWITTER_API_KEY (Example placeholder)

LINKEDIN_ACCESS_TOKEN (Example placeholder)

You can set these in your terminal (e.g., export MASTODON_ACCESS_TOKEN="your-token") or use a local .env file with a tool like python-dotenv.

Run the Scheduler:

python social_media_scheduler.py


⚙️ Example Config (scheduler_config.json)

The schedule uses a clean JSON structure to separate settings and the posting data array. Time format must be YYYY-MM-DD HH:MM.

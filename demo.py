import csv
import time
from datetime import datetime, timedelta
from github import Github

g = Github("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")

def get_user_details(username):
    user = g.get_user(username)
    user_details = {
        'login': user.login,
        'name': user.name,
        'bio': user.bio,
        'public_repos': user.public_repos,
        'followers_count': user.followers,
        'following_count': user.following,
        'created_at': user.created_at,
        'updated_at': user.updated_at,
        'avatar_url': user.avatar_url,
        'profile_url': user.html_url,
        'total_commits': 0,
        'contributions_per_month': {}
    }

    # Get user's contributions from January 2023 to current date
    end_date = datetime.utcnow()
    start_date = datetime(2023, 1, 1)

    # Get user events
    events = user.get_events()
    
    for event in events:
        created_at = event.created_at
        # Filter push events
        if event.type == "PushEvent" and start_date <= created_at <= end_date:
            month_year = created_at.strftime("%Y-%m")
            user_details['total_commits'] += event.payload['size']
            if month_year not in user_details['contributions_per_month']:
                user_details['contributions_per_month'][month_year] = event.payload['size']
            else:
                user_details['contributions_per_month'][month_year] += event.payload['size']

    print(user_details)

get_user_details("nethajinirmal13")

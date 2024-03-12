import csv
import time
from github import Github


g = Github("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")

def get_user_details(username):
    user = g.get_user(username)

    # Get languages
    languages = {}
    for repo in user.get_repos():
        try:
            for language, bytes in repo.get_languages().items():
                languages[language] = languages.get(language, 0) + bytes
        except Exception as e:
            print(f"Error fetching languages for repository {repo.full_name}: {e}")

    # Get starred repositories
    starred_repositories = []
    try:
        starred_repositories = [repo.html_url for repo in user.get_starred()]
    except Exception as e:
        print(f"Error fetching starred repositories for user {username}: {e}")

    # Get subscriptions
    subscriptions = []
    try:
        subscriptions = [repo.html_url for repo in user.get_subscriptions()]
    except Exception as e:
        print(f"Error fetching subscriptions for user {username}: {e}")

    # Get organizations
    organizations = []
    try:
        organizations = [org.login for org in user.get_orgs()]
    except Exception as e:
        print(f"Error fetching organizations for user {username}: {e}")

    # Get followers list
    followers_list = []
    try:
        followers_list = [follower.login for follower in user.get_followers()]
    except Exception as e:
        print(f"Error fetching followers for user {username}: {e}")

    # Get following list
    following_list = []
    try:
        following_list = [following.login for following in user.get_following()]
    except Exception as e:
        print(f"Error fetching following for user {username}: {e}")

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
        'languages': languages,
        'starred_repositories': starred_repositories,
        'subscriptions': subscriptions,
        'organizations': organizations,
        'followers_list': followers_list,
        'following_list': following_list
    }
    return user_details

def write_to_csv(user_details, filename):
    header = list(user_details.keys())
    try:
        with open(filename, 'a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=header)
            if file.tell() == 0:
                writer.writeheader()
            writer.writerow(user_details)
    except Exception as e:
        print(f"Error writing to CSV: {e}")

def get_organization_members_details(organization_name, count=10, filename='user_details.csv'):
    organization = g.get_organization(organization_name)
    members = organization.get_members()
    try:
        for member in members[:count]:  # Fetch details for the first 'count' members
            try:
                user_details = get_user_details(member.login)
                write_to_csv(user_details, filename)
            except Exception as e:
                print(f"Error fetching details for member {member.login}: {e}")
            # Add a small delay to avoid rate limiting
            time.sleep(1)  # You can adjust this delay as needed
    except Exception as e:
        print(f"Error fetching organization members: {e}")

# Example usage:
organization_name = 'wordpress'  
get_organization_members_details(organization_name, count=600)

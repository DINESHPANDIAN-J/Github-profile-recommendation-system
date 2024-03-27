# import pandas as pd
# import re
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity

# # read file
# data = pd.read_csv('data_for_building_model.csv')

# # Preprocessing functions
# def preprocess_organization(org):
#     if pd.isnull(org):
#         return ''
#     org = org.strip('][').replace('"', '').split(', ')
#     org = [word.strip("'") for word in org]
#     org = [word.lower().strip() for word in org]
#     return ' '.join(org)

# def clean_github_links(link):
#     if isinstance(link, str):
#         link = link.replace('https://github.com/', '')
#         link = re.sub(r'[^a-zA-Z0-9\s]', ' ', link).lower().strip()
#         link = re.sub(r'\s+', ' ', link)
#         return link
#     else:
#         return None



# # TF-IDF Vectorization
# tfidf_vectorizer = TfidfVectorizer()
# tfidf_matrix = tfidf_vectorizer.fit_transform(data['combined_text'])

# removing_columns = ['login', 'profile_url', 'organizations', 'starred_repositories_cleaned','subscriptions_cleaned', 'combined_text']
# new_df = data.drop(columns=removing_columns, inplace=True)
# final_df = pd.concat(tfidf_matrix, new_df, axis = 1)

# # Compute cosine similarity matrix
# cosine_sim = cosine_similarity(final_df, final_df)

# # Function to get top recommendations based on input values
# def get_top_recommendations(org, starred_repo, subscription, top_n=10):
#     # Preprocess the input values
#     org = preprocess_organization(org)
#     starred_repo = clean_github_links(starred_repo)
#     subscription = clean_github_links(subscription)
    
#     # Combine the preprocessed values into a single string
#     input_text = org + ' ' + starred_repo + ' ' + subscription
    
#     # Transform input text into TF-IDF vector
#     input_tfidf = tfidf_vectorizer.transform([input_text])
    
#     # Calculate cosine similarity with other documents
#     sim_scores = cosine_similarity(input_tfidf, tfidf_matrix)
    
#     # Get indices of top recommendations
#     top_recommendation_indices = sim_scores.argsort()[0][-top_n:][::-1]
    
#     return data.iloc[top_recommendation_indices]


# # Provide input values and get top recommendation
# org_input = 'Microsoft'
# starred_repo_input = 'https://github.com/repo'
# subscription_input = 'https://github.com/sub'
# top_recommendation = get_top_recommendations(org_input, starred_repo_input, subscription_input)
# print("Top recommendation:", top_recommendation[['profile_url','login']])

## MODEL WITH NUMERIC DATA INCLUDED.
import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def clean_github_links(link):
    if isinstance(link, str):
        link = link.replace('https://github.com/', '')
        link = re.sub(r'[^a-zA-Z0-9\s]', ' ', link).lower().strip()
        link = re.sub(r'\s+', ' ', link)
        return link
    else:
        return None

# Function to preprocess the organization column
def preprocess_organization(org):
    if pd.isnull(org):
        return ''
    org = org.strip('][').replace('"', '').split(', ')
    org = [word.strip("'") for word in org]
    org = [word.lower().strip() for word in org]
    return ' '.join(org)

data = pd.read_csv('new_data_for_building_model.csv')

# Handle NaN values in 'combined_text' column
data['combined_text'].fillna('', inplace=True)

# TF-IDF Vectorization
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(data['combined_text'])

removing_columns = ['login', 'profile_url', 'organizations', 'starred_repositories_cleaned','subscriptions_cleaned', 'combined_text']
new_df = data.drop(columns=removing_columns)

# Convert TF-IDF matrix to DataFrame
tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=tfidf_vectorizer.get_feature_names_out())

# Concatenate horizontally
final_df = pd.concat([new_df.reset_index(drop=True), tfidf_df], axis=1)

# Drop rows with NaN values after concatenation
final_df.dropna(inplace=True)

# Compute cosine similarity matrix
cosine_sim = cosine_similarity(final_df, final_df)

# Function to get top recommendations based on input values
def get_top_recommendations(org, starred_repo, subscription, public_repos, followers_count, following_count, organizations, created_year, created_month, created_day, updated_year, updated_month, updated_day, top_n=10):
    org = preprocess_organization(org)
    starred_repo = clean_github_links(starred_repo)
    subscription = clean_github_links(subscription)
    input_text = f"{org} {starred_repo} {subscription} {public_repos} {followers_count} {following_count} {organizations} {created_year} {created_month} {created_day} {updated_year} {updated_month} {updated_day}"
    input_tfidf = tfidf_vectorizer.transform([input_text])
    sim_scores = cosine_similarity(input_tfidf, tfidf_matrix)
    top_recommendation_indices = sim_scores.argsort()[0][-top_n:][::-1]
    return data.iloc[top_recommendation_indices]

# main
org_input = 'Microsoft'
starred_repo_input = 'https://github.com/rep'
subscription_input = 'https://github.com/sub'
public_repos_input = 10
followers_count_input = 100
following_count_input = 50
organizations_input = 'org1 org2'
created_year_input = 2022
created_month_input = 1
created_day_input = 15
updated_year_input = 2023
updated_month_input = 5
updated_day_input = 20

top_recommendation = get_top_recommendations(org_input, starred_repo_input, subscription_input, public_repos_input, followers_count_input, following_count_input, organizations_input, created_year_input, created_month_input, created_day_input, updated_year_input, updated_month_input, updated_day_input)
print("Top recommendation:", top_recommendation[['profile_url', 'login']])
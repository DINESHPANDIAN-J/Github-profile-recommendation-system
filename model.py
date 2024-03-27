import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# read file
data = pd.read_csv('data_for_building_model.csv')

# Preprocessing functions
def preprocess_organization(org):
    if pd.isnull(org):
        return ''
    org = org.strip('][').replace('"', '').split(', ')
    org = [word.strip("'") for word in org]
    org = [word.lower().strip() for word in org]
    return ' '.join(org)

def clean_github_links(link):
    if isinstance(link, str):
        link = link.replace('https://github.com/', '')
        link = re.sub(r'[^a-zA-Z0-9\s]', ' ', link).lower().strip()
        link = re.sub(r'\s+', ' ', link)
        return link
    else:
        return None



# TF-IDF Vectorization
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(data['combined_text'])

# Compute cosine similarity matrix
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Function to get top recommendations based on input values
def get_top_recommendations(org, starred_repo, subscription, top_n=10):
    # Preprocess the input values
    org = preprocess_organization(org)
    starred_repo = clean_github_links(starred_repo)
    subscription = clean_github_links(subscription)
    
    # Combine the preprocessed values into a single string
    input_text = org + ' ' + starred_repo + ' ' + subscription
    
    # Transform input text into TF-IDF vector
    input_tfidf = tfidf_vectorizer.transform([input_text])
    
    # Calculate cosine similarity with other documents
    sim_scores = cosine_similarity(input_tfidf, tfidf_matrix)
    
    # Get indices of top recommendations
    top_recommendation_indices = sim_scores.argsort()[0][-top_n:][::-1]
    
    return data.iloc[top_recommendation_indices]


# Provide input values and get top recommendation
org_input = 'Microsoft'
starred_repo_input = 'https://github.com/repo2'
subscription_input = 'https://github.com/sub2'
top_recommendation = get_top_recommendations(org_input, starred_repo_input, subscription_input)
print("Top recommendation:", top_recommendation[['profile_url','login']])

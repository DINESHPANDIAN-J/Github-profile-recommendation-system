import streamlit as st
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import pandas as pd

# Load the saved model
with open('recommendation_model.pkl', 'rb') as f:
    tfidf_vectorizer, tfidf_matrix, cosine_sim, df = pickle.load(f)

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
    
    return df.iloc[top_recommendation_indices]

# Function to preprocess the organization column
def preprocess_organization(org):
    if pd.isnull(org):
        return ''
    org = org.strip('][').replace('"', '').split(', ')
    org = [word.strip("'") for word in org]
    org = [word.lower().strip() for word in org]
    return ' '.join(org)

# Function to clean GitHub links
def clean_github_links(link):
    if isinstance(link, str):
        link = link.replace('https://github.com/', '')
        link = re.sub(r'[^a-zA-Z0-9\s]', ' ', link).lower().strip()
        link = re.sub(r'\s+', ' ', link)
        return link
    else:
        return None

# Streamlit UI
st.title('GitHub Profile Recommendation System')

# Input fields
org_input = st.text_input('Enter Organization:', '')
starred_repo_input = st.text_input('Enter Starred Repository:', '')
subscription_input = st.text_input('Enter Subscription:', '')

# Button to get recommendations
if st.button('Get Recommendations'):
    top_recommendations = get_top_recommendations(org_input, starred_repo_input, subscription_input)
    st.write('Top Recommendations:')
    st.write(top_recommendations[['profile_url','login']])

import streamlit as st
import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

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

# Load the saved model
with open('new_recommendation_model.pkl', 'rb') as f:
    tfidf_vectorizer, tfidf_matrix, cosine_sim, data = pickle.load(f)

# Streamlit UI
st.title('GitHub Profile Recommendation System')

# Input fields
org_input = st.text_input('Enter Organization:', '')
starred_repo_input = st.text_input('Enter Starred Repository:', '')
subscription_input = st.text_input('Enter Subscription:', '')
public_repos_input = st.number_input('Enter Public Repositories:', value=0)
followers_count_input = st.number_input('Enter Followers Count:', value=0)
following_count_input = st.number_input('Enter Following Count:', value=0)
organizations_input = st.text_input('Enter Organizations (comma-separated):', '')
created_year_input = st.number_input('Enter Created Year:', value=0)
created_month_input = st.number_input('Enter Created Month:', value=0)
created_day_input = st.number_input('Enter Created Day:', value=0)
updated_year_input = st.number_input('Enter Updated Year:', value=0)
updated_month_input = st.number_input('Enter Updated Month:', value=0)
updated_day_input = st.number_input('Enter Updated Day:', value=0)

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
    
# Button to get recommendations
if st.button('Get Recommendations'):
    top_recommendations = get_top_recommendations(org_input, starred_repo_input, subscription_input, public_repos_input, followers_count_input, following_count_input, organizations_input, created_year_input, created_month_input, created_day_input, updated_year_input, updated_month_input, updated_day_input)
    st.write('Top Recommendations:')
    st.write(top_recommendations[['profile_url', 'login']])



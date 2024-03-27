import streamlit as st
import pandas as pd
import pymongo

# Function to retrieve data from MongoDB
def fetch_data_from_mongodb():
    # Connect to MongoDB
    client = pymongo.MongoClient("mongodb+srv://Dinesh_pandian_j:14114@cluster0.kxes2.mongodb.net/")
    db = client["GRS"]
    collection = db["github_users"]

    # Fetch user data
    user_data = collection.find({})  # You may add query parameters if needed

    return pd.DataFrame(list(user_data))

# Function to display user statistics
def display_user_statistics(data):
    st.subheader("User Statistics")
    st.write("Number of Users:", len(data))
    st.write("Total Repositories:", data['public_repos'].sum())
    st.write("Total Commits:", data['total_commits'].sum())
    st.write("Average Followers:", data['followers_count'].mean())
    st.write("Average Following:", data['following_count'].mean())

# Function to visualize popular languages
def visualize_popular_languages(data):
    st.subheader("Popular Languages")
    language_counts = data.iloc[:, 6:].sum().sort_values(ascending=False)
    st.bar_chart(language_counts)

# Function to display individual profile analytics
def display_profile_analytics(data):
    st.subheader("Profile Analytics")

    # User selection dropdown
    selected_user = st.selectbox("Select User:", data['login'])

    # Display profile details
    profile_data = data[data['login'] == selected_user]
    st.write("Username:", profile_data['login'].values[0])
    st.write("Total Repositories:", profile_data['public_repos'].values[0])
    st.write("Total Commits:", profile_data['total_commits'].values[0])
    # Add more profile details as needed

# Main function
def main():
    # Page title
    st.title("GitHub Analytics Dashboard")

    # Fetch data from MongoDB
    data = fetch_data_from_mongodb()

    # Display user statistics
    display_user_statistics(data)

    # Visualize popular languages
    visualize_popular_languages(data)

    # Display individual profile analytics
    display_profile_analytics(data)

# Execute the main function
if __name__ == "__main__":
    main()

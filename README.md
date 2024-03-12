# GitHub Profile Recommendation System

## Introduction

This repository contains the code and resources for a GitHub Profile Recommendation System. The system aims to provide personalized recommendations to users based on their preferences, including organizations of interest, starred repositories, and subscriptions.
### You can use the APP here: https://dinesh-recommendation-system.streamlit.app/

## Data Collection and Preprocessing

### LinkedIn Data Retrieval
- User data was collected from LinkedIn using the LinkedIn API.
- Information such as organizations, starred repositories, subscriptions, followers, and following was extracted.

### Data Cleaning and Transformation
- The raw LinkedIn data was cleaned and transformed to prepare it for building the recommendation system.
- Preprocessing steps included handling null values, extracting relevant information, and formatting data for analysis.

## Model Building

### Content-Based Filtering
- A content-based filtering approach was adopted to build the recommendation system.
- Text data, including organizations, starred repositories, and subscriptions, were vectorized using TF-IDF.
- Cosine similarity was computed to measure the similarity between user profiles.

## Model Evaluation

### Top Recommendations
- A Streamlit application was implemented to demonstrate the functionality of the recommendation system.
- Users can input their preferences, such as organization, starred repository, and subscription, to receive personalized recommendations.
- The system retrieves the top recommended GitHub profiles based on the input values and displays them to the user.

## Usage

To use the GitHub Profile Recommendation System, follow these steps:
1. Clone the repository to your local machine.
2. Install the necessary dependencies.
3. Run the Streamlit application using the provided script.
4. Input your preferences and receive personalized recommendations.

## Conclusion

The GitHub Profile Recommendation System provides an effective way to discover relevant GitHub profiles based on user preferences. By leveraging content-based filtering, the system offers personalized recommendations tailored to individual interests.

## Future Improvements

- Enhance the user interface for better usability and visualization of recommendations.
- Incorporate additional features, such as user feedback and collaborative filtering, to improve recommendation accuracy.
- Optimize model performance and scalability for handling large datasets.

## Contributors

- Dinesh Pandian J (https://github.com/DINESHPANDIAN-J)


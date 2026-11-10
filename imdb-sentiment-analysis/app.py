import streamlit as st
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib

# Load the performance metrics CSV file
metrics_df = pd.read_csv('performance_metrics.csv')

# Create a dictionary to map model names to their corresponding file names
model_files = {
    'SVM': 'model_svm.pkl',
    'Logistic Regression': 'model_lr.pkl',
    'Naive Bayes': 'model_nb.pkl',
    'Random Forest': 'model_rfc.pkl',
    'Ensemble': 'model_ensemble.pkl'
}

# Load models
models = {}
for model_name, model_file in model_files.items():
    models[model_name] = joblib.load(model_file)

# Function to get performance metrics for selected models
def get_metrics(model_names):
    selected_metrics = metrics_df[metrics_df['Model'].isin(model_names)]
    return selected_metrics

# Function to predict sentiment of a review using the selected model
def predict_sentiment(review, model):
    prediction = model.predict([review])
    sentiment = 'Positive' if prediction == 1 else 'Negative'
    return sentiment

# Streamlit app
def main():
    st.title('IMDB Sentiment Analysis')

    # Sidebar for model selection
    st.sidebar.title('Choose Models')
    model_1 = st.sidebar.selectbox('Select Model 1', list(models.keys()))
    model_2 = st.sidebar.selectbox('Select Model 2', list(models.keys()))

    # Display performance metrics for selected models
    st.subheader('Performance Metrics')
    selected_metrics = get_metrics([model_1, model_2])
    st.write(selected_metrics)

    # Determine best model
    st.subheader('Best Model')
    best_model = selected_metrics.loc[selected_metrics['Accuracy'].idxmax(), 'Model']
    st.write(f"The best model between {model_1} and {model_2} is: {best_model}")

    # Input for movie review
    st.subheader('Enter a Movie Review')
    review = st.text_area('Type your review here')

    # Prediction
    if st.button('Predict Sentiment'):
        if review:
            best_model_obj = models[best_model]
            sentiment = predict_sentiment(review, best_model_obj)
            st.write(f'The sentiment of the review is: {sentiment}')
        else:
            st.warning('Please enter a movie review.')

if __name__ == '__main__':
    main()

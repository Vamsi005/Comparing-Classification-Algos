import streamlit as st
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
import time
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import roc_curve, auc

# Load the performance metrics CSV files
imdb_metrics_df = pd.read_csv('imdb_performance_metrics.csv')
twitter_metrics_df = pd.read_csv('twitter_performance_metrics.csv')

# Define the dictionary mapping model names to their corresponding confusion matrix file names
confusion_matrix_files = {
    'IMDB': {
        'SVM': 'imdb_SVM_cm.pkl',
        'Logistic Regression': 'imdb_Logistic Regression_cm.pkl',
        'Naive Bayes': 'imdb_Naive Bayes_cm.pkl',
        'Random Forest': 'imdb_Random Forest_cm.pkl',
        'Ensemble': 'imdb_Ensemble_cm.pkl'
    },
    'Twitter': {
        'SVM': 'twitter_SVM_cm.pkl',
        'Logistic Regression': 'twitter_Logistic Regression_cm.pkl',
        'Naive Bayes': 'twitter_Naive Bayes_cm.pkl',
        'Random Forest': 'twitter_Random Forest_cm.pkl',
        'Ensemble': 'twitter_Ensemble_cm.pkl'
    }
}



# Create dictionaries to map model names to their corresponding file names for IMDb and Twitter datasets
imdb_model_files = {
    'SVM': 'imdb_model_svm.pkl',
    'Logistic Regression': 'imdb_model_lr.pkl',
    'Naive Bayes': 'imdb_model_nb.pkl',
    'Random Forest': 'imdb_model_rfc.pkl',
    'Ensemble': 'imdb_model_ensemble.pkl'
}

twitter_model_files = {
    'SVM': 'twitter_model_svm.pkl',
    'Logistic Regression': 'twitter_model_lr.pkl',
    'Naive Bayes': 'twitter_model_nb.pkl',
    'Random Forest': 'twitter_model_rfc.pkl',
    'Ensemble': 'twitter_model_ensemble.pkl'
}

# Function to load confusion matrix from pickle file
def load_confusion_matrix(dataset, model_name):
    filename = confusion_matrix_files[dataset][model_name]
    return joblib.load(filename)

# Load models for IMDb and Twitter datasets
imdb_models = {}
twitter_models = {}

for model_name, model_file in imdb_model_files.items():
    imdb_models[model_name] = joblib.load(model_file)

for model_name, model_file in twitter_model_files.items():
    twitter_models[model_name] = joblib.load(model_file)

# Function to get performance metrics for selected models and dataset
def get_metrics(dataset_metrics_df, model_names):
    selected_metrics = dataset_metrics_df[dataset_metrics_df['Model'].isin(model_names)]
    return selected_metrics

# Function to load ROC curve data from joblib file
def load_roc_curve_data(dataset):
    filename = f'{dataset.lower()}_roc_curve_data.joblib'
    return joblib.load(filename)

# Streamlit app
def main():
    st.title('Sentiment Analysis Comparison')

    # Sidebar for dataset selection
    st.sidebar.title('Choose Dataset')
    dataset = st.sidebar.selectbox('Select Dataset', ['IMDB', 'Twitter'])

    if dataset == 'IMDB':
        roc_curve_data = load_roc_curve_data('IMDB')
        selected_metrics_df = imdb_metrics_df
    else:
        roc_curve_data = load_roc_curve_data('Twitter')
        selected_metrics_df = twitter_metrics_df
        #data_path = 'data/training.1600000.processed.noemoticon.csv'

    # Load review data with explicit encoding
    #data = pd.read_csv(data_path, encoding='latin-1')

    # Sidebar for model selection
    st.sidebar.title('Choose Models')
    model_1 = st.sidebar.selectbox('Select Model 1', list(roc_curve_data.keys()))
    model_2 = st.sidebar.selectbox('Select Model 2', list(roc_curve_data.keys()))

    # Display performance metrics for selected models and dataset
    st.subheader('Performance Metrics')
    selected_metrics = get_metrics(selected_metrics_df, [model_1, model_2])
    st.write(selected_metrics)

    # Determine best model
    st.subheader('Best Model')
    best_model = selected_metrics.loc[selected_metrics['Accuracy'].idxmax(), 'Model']
    st.write(f"The best model between {model_1} and {model_2} is: {best_model}")
    
    #Display confusion matrices for selected models and dataset
    st.subheader('Confusion Matrices')
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))  # Adjust the figure size as needed
    for i, model_name in enumerate([model_1, model_2]):
        ax = axes[i]
        ax.set_title(f'Confusion Matrix for {model_name}')
        confusion_matrix_data = load_confusion_matrix(dataset, model_name)
        sns.heatmap(confusion_matrix_data, annot=True, fmt="d", cmap="Blues", cbar=False, ax=ax)
        ax.set_xlabel('Predicted Labels')
        ax.set_ylabel('True Labels')
    st.pyplot(fig)

    # Display ROC curves for the chosen models side by side
    st.subheader('ROC Curves')
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))  # Create subplots
    for i, model_name in enumerate([model_1, model_2]):
        ax = axes[i]
        roc_curve_data = load_roc_curve_data(dataset)
        fpr = roc_curve_data[model_name]['fpr']
        tpr = roc_curve_data[model_name]['tpr']
        ax.plot(fpr, tpr, label=f'{model_name} ROC curve')
        ax.plot([0, 1], [0, 1], color='gray', linestyle='--')
        ax.set_xlabel('False Positive Rate')
        ax.set_ylabel('True Positive Rate')
        ax.set_title(f'ROC Curve for {model_name}')
        ax.legend(loc='lower right')
    st.pyplot(fig)  # Display the subplots

if __name__ == '__main__':
    main()

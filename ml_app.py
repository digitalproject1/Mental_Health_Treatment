import streamlit as st
import pandas as pd
import numpy as np
import joblib as jl
import pickle as pk
from sklearn import metrics
from sklearn.metrics import confusion_matrix, accuracy_score, f1_score, \
                            precision_score,_dist_metrics,recall_score, fbeta_score                           
from sklearn.metrics import classification_report, precision_recall_curve
from sklearn.metrics import auc, roc_auc_score, roc_curve
from sklearn.metrics import make_scorer, recall_score, log_loss
from sklearn.metrics import average_precision_score


# Function to preprocess the data and encode categorical variables
def preprocess_data(data):
    data["Gender"] = data["Gender"].replace({'Male': 0, 'Female': 1, 'Other': 2}).astype(int)
    data["self_employed"] = data["self_employed"].replace({'Yes': 1, 'No': 0}).astype(int)
    data["family_history"] = data["family_history"].replace({'Yes': 1, 'No': 0}).astype(int)
    data["work_interfere"] = data["work_interfere"].replace({'Never': 0, 'Rarely': 1, 'Sometimes': 2, 'Often': 3}).astype(int)
    data["remote_work"] = data["remote_work"].replace({'Yes': 1, 'No': 0}).astype(int)
    return data

# Load the pre-trained machine learning model
@st.cache()
def load_model(ml_model):
    if ml_model == 'Logistic Regression':
        return jl.load('Model/LR_Classifier.pkl')
    elif ml_model == 'Decision Tree':
        return jl.load('Model/DT_Classifier.pkl')
    elif ml_model == 'Random Forest Classifier':
        return jl.load('Model/RF_Classifier.pkl')
    elif ml_model == 'KNeighborsClassifier':
        return jl.load('Model/KNN.pkl') 
    elif ml_model == 'Support Vector Classifier':
        return jl.load('Model/SVM.pkl')
    elif ml_model == 'XGBoost Classifier':
        return jl.load('Model/XGBoost_Classifier.pkl')
    else:
        return jl.load('Model/Stacking_Classifier.pkl')

def ds_ml_app():
    
    # Add your machine learning content here

    st.write('')
    
    with st.expander("Modeling and Evaluation"):
        st.write("Data Preprocessing:")
        st.write("To prepare the data for modeling, we first dropped unnecessary columns that were not relevant to our research purpose. The columns dropped include 'Country', 'benefits', 'care_options', 'wellness_program', 'seek_help', 'anonymity', 'leave', 'mental_health_consequence', 'phys_health_consequence', 'coworkers', 'supervisor', 'mental_health_interview', 'phys_health_interview', 'mental_vs_physical', and 'obs_consequence'.")
        st.write("Next, we performed manual encoding for categorical variables with more than two values. The following variables were encoded:")
        st.write(" - 'self_employed': Replaced 'No' with 0 and 'Yes' with 1.")
        st.write(" - 'family_history': Replaced 'No' with 0 and 'Yes' with 1.")
        st.write(" - 'treatment': Replaced 'No' with 0 and 'Yes' with 1.")
        st.write(" - 'remote_work': Replaced 'No' with 0 and 'Yes' with 1.")
        st.write(" - 'tech_company': Replaced 'No' with 0 and 'Yes' with 1.")
        st.write(" - 'Gender': Replaced 'Male' with 0, 'Female' with 1, and 'Other' with 2.")
        st.write(" - 'work_interfere': Replaced 'Never' with 0, 'Rarely' with 1, 'Sometimes' with 2, and 'Often' with 3.")
        st.write(" - 'no_employees': Replaced categorical ranges with numerical values, e.g., '1-5' with 0, '6-25' with 1, and so on.")

        st.write("Feature Importance:")
        st.write("To understand the importance of each feature in predicting the need for mental health treatment, we used mutual information (MI) scores. The MI scores provide insights into how strongly each variable influences the 'treatment' column. The results showed that 'work_interfere' and 'family_history' have the highest MI scores, indicating that they are the most influential variables in determining an employee's mental health treatment needs. On the other hand, 'no_employees' and 'tech_company' had MI scores of 0, suggesting that they do not have any predictive power in this context.")

        st.write("Data Splitting:")
        st.write("Before modeling, we split the dataset into dependent and independent variables. The 'treatment' column was designated as the dependent variable, while the rest of the columns were considered independent variables. We used an 80-20 train-test split with stratification to ensure balanced representation of the target variable in both sets.")

        st.write("Feature Scaling:")
        st.write("To standardize the independent variables, we performed feature scaling using the StandardScaler. This step is important for models that are sensitive to the scale of input features, such as logistic regression.")

        st.write("Model Evaluation:")
        st.write("We evaluated the performance of three different models: Logistic Regression, Decision Tree Classifier, and Random Forest. We used two main evaluation metrics - ROC AUC and Accuracy - to assess each model's predictive capabilities.")

        st.write("Logistic Regression:")
        st.write("Despite promising ROC AUC and Accuracy mean scores of 76.75 and 71.72, respectively, we observed issues with this model. When predicting a single sample, the model consistently predicts a treatment value of 1, with probabilities close to 1 for all samples. This behavior indicates that the logistic regression model might be overfitting to the data or encountering convergence issues.")

        st.write("Decision Tree Classifier:")
        st.write("The Decision Tree model showed lower ROC AUC and Accuracy mean scores of 64.98 and 63.29, respectively. Additionally, the probabilities for the predicted classes were consistently between 0 and 1, suggesting that the model may not be effectively capturing the underlying patterns in the data.")

        st.write("Random Forest:")
        st.write("Despite slightly lower ROC AUC mean score of 70.26, the Random Forest model exhibited better generalization. The probabilities of the predicted classes were not highly polarized, indicating a more balanced and reasonable model output.")

        st.write("Based on the evaluation results, we have decided to use the Random Forest model for its more reliable and stable predictions, considering the probabilities and overall performance compared to the other models. Further tuning and optimization of the Random Forest model could potentially improve its performance and make it a robust predictor for mental health treatment needs.")

    st.subheader('Mental Health Treatment Prediction')
    st.write('Enter the following information:')
    
    # Input fields
    age = st.number_input('Age', min_value=18, max_value=100, value=30)
    gender = st.selectbox('Gender', ['Male', 'Female', 'Other'])
    self_employed = st.selectbox('Self Employed', ['No', 'Yes'])
    family_history = st.selectbox('Family History of Mental Illness', ['No', 'Yes'])
    work_interfere = st.selectbox('Mental Illness Interferes with Work', ['Never', 'Rarely', 'Sometimes', 'Often'])
    remote_work = st.selectbox('Remote Work', ['No', 'Yes'])
    ml_model = st.selectbox('Machine Learning Model', ['Random Forest Classifier', 'Logistic Regression', 'Decision Tree Classifier',
                                                       'XBoost Classifier','KNeighbors Classifier','Support Vector Classifier',
                                                        'Stacking Classifier' ])
    
    # Convert input to a DataFrame
    input_data = pd.DataFrame({
        'Age': [age],
        'Gender': [gender],
        'self_employed': [self_employed],
        'family_history': [family_history],
        'work_interfere': [work_interfere],
        'remote_work': [remote_work]
    })
    
    # Preprocess the input data
    input_data_encoded = preprocess_data(input_data)

    model = load_model(ml_model)
    
    # Make predictions
    prediction = model.predict(input_data_encoded)
    prediction_proba = model.predict_proba(input_data_encoded)[:, 1]  # Probability of positive class (treatment needed)
    prediction_text = "Mental health treatment is needed." if prediction[0] == 1 else "Mental health treatment is not needed."

    # Display the prediction
    st.subheader('Prediction')
    st.write(prediction_text)

    # Improve prediction_proba text
    st.subheader('Prediction Probability')
    if prediction[0] == 1:
        st.write(f"There is a {prediction_proba[0]*100:.2f}% probability that mental health treatment is needed.")
    else:
        st.write(f"There is a {prediction_proba[0]*100:.2f}% probability that mental health treatment is not needed.")

# Improve prediction_proba text
    st.subheader('Suggestion')
    if prediction[0] == 1:
        st.write("If you or someone you know is struggling with mental health, it's essential to seek help. Reach out to mental health professionals, support groups, or helplines to get the support you need.")
        st.write("- Seeking professional help can make a difference -")
    else:
        st.write("Even if mental health treatment is not predicted to be needed, it's crucial to prioritize your mental well-being. Engaging in self-care practices, talking to friends or family, and seeking professional guidance can contribute to a healthier and happier life.")
        st.write("- Taking care of your mental health is essential for overall well-being -")

if __name__ == "__main__":
    ds_ml_app()

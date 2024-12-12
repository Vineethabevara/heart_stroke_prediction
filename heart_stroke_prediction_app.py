import pandas as pd
import numpy as np
import pickle
import streamlit as st
from PIL import Image

pickle_in = open('stroke_detection/classifier.pkl', 'rb')
classifier = pickle.load(pickle_in)

def welcome():
    return 'welcome all'

def prediction(classifier, gender, hypertension, heart_disease, married, residence, age1, avg_glucose1, work_type1, bmi1, smoking_stat1):
    # Binary encoding for categorical variables
    gender = 0 if gender == "Male" else 1
    hypertension = 1 if hypertension == "Yes" else 0
    heart_disease = 1 if heart_disease == "Yes" else 0
    married = 1 if married == "Yes" else 0
    residence = 1 if residence == "Rural" else 0

    # Initialize one-hot encoding arrays
    age = [0, 0, 0, 0]  # Age groups: <20, 20-40, 40-60, >60
    glucose_level = [0, 0, 0, 0]  # Glucose groups
    work_type = [0, 0, 0, 0, 0]  # Work types
    bmi = [0, 0, 0, 0]  # BMI categories
    smoking = [0, 0, 0, 0]  # Smoking status

    # Age group
    if age1 < 20:
        age[3] = 1
    elif 20 <= age1 < 40:
        age[0] = 1
    elif 40 <= age1 < 60:
        age[1] = 1
    else:
        age[2] = 1

    # Glucose level group
    if avg_glucose1 < 77:
        glucose_level[3] = 1
    elif avg_glucose1 < 91:
        glucose_level[0] = 1
    elif avg_glucose1 < 114:
        glucose_level[1] = 1
    else:
        glucose_level[2] = 1

    # Work type
    if work_type1 == "Govt job":
        work_type[0] = 1
    elif work_type1 == "Never worked":
        work_type[1] = 1
    elif work_type1 == "Private":
        work_type[2] = 1
    elif work_type1 == "Self-employed":
        work_type[3] = 1
    else:
        work_type[4] = 1

    # BMI category
    if bmi1 < 23:
        bmi[3] = 1
    elif bmi1 < 28:
        bmi[0] = 1
    elif bmi1 < 33:
        bmi[1] = 1
    else:
        bmi[2] = 1

    # Smoking status
    if smoking_stat1 == "Unknown":
        smoking[0] = 1
    elif smoking_stat1 == "Formerly smoked":
        smoking[1] = 1
    elif smoking_stat1 == "Never smoked":
        smoking[2] = 1
    else:
        smoking[3] = 1

    # Prepare input for the classifier
    features = [
        gender, hypertension, heart_disease, married, residence,
        *age, *glucose_level, *work_type, *bmi, *smoking
    ]

    # Predict and return result
    prediction = classifier.predict([features])
    return prediction


def main():
	st.title("Heart ❤ Stroke Prediction App")
	html_temp=""
	ans=0
	st.markdown(html_temp,unsafe_allow_html = True)
	get_Gender = st.sidebar.radio("Select your gender",("Male","Female"))
	get_Hypertension = st.sidebar.radio("Do you have hypertension?",("Yes","No"))
	get_heartDisease = st.sidebar.radio("Do you have heart disease?",("Yes","No"))
	get_married = st.sidebar.radio("Have you ever been married?",("Yes","No"))
	get_residence = st.selectbox("Select your residence type",("Rural","Urban"))
	get_age = st.slider("How old are you?",value=25)
	get_workType = st.selectbox("Select the type of work you do.",("Govt job","Never worked","Private","Self-employed","Children"))
	get_bmi = st.slider("How much is your bmi?",min_value=10,max_value=100,value=65)
	get_glucose = st.slider("How much is your glucose level?",min_value=55,max_value=272,value=50)
	get_smoke = st.selectbox("What's your smoking history",("Unknown","Formerly smoked","Never smoked","Smokes"))

	if st.button("Predict"):
		ans=prediction(get_Gender,get_age,get_Hypertension,get_heartDisease,get_married,get_workType,get_residence,get_glucose,get_bmi,get_smoke)[0]
		if ans==0:
			st.success('You have no chance of getting stroke')
			st.image('stroke_detection/images/happy_heart.jfif')
		else:
			st.success('You are at risk of getting stroke')
			st.image('stroke_detection/images/damaged_heart.jfif')

if __name__=='__main__':
    main()

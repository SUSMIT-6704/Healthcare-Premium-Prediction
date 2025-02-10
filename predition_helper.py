import pandas as pd
from joblib import load

# Load models and scalers
model_rest = load("artifacts/model_rest.joblib")
model_young = load("artifacts/model_young.joblib")
scaler_rest = load("artifacts/scaler_rest.joblib")
scaler_young = load("artifacts/scaler_young.joblib")


# Calculate normalized risk
def calculate_normalized_risk(medical_history):
    risk_scores = {
        "diabetes": 4,
        "high blood pressure": 3,
        "thyroid": 2,
        "heart disease": 5,
        "no disease": 0,
        "none": 0
    }
    diseases = medical_history.lower().split(" & ")
    total_risk_score = sum(risk_scores.get(disease, 0) for disease in diseases)
    max_score = 9  # Max risk score
    min_score = 0
    normalized_risk_score = (total_risk_score - min_score) / (max_score - min_score)
    return normalized_risk_score


# Preprocess input data
# Preprocess input data
def preprocess_input(input_data):
    expected_columns = [
        'age', 'number_of_dependants', 'bmi_category', 'smoking_status',
        'income_lakhs', 'insurance_plan', 'genetical_risk',
        'normalized_risk_score', 'gender_Male', 'region_Northwest',
        'region_Southeast', 'region_Southwest', 'marital_status_Unmarried',
        'employment_status_Salaried', 'employment_status_Self-Employed'
    ]

    insurance_plan_encoding = {'Bronze': 1, 'Silver': 2, 'Gold': 3}
    smoking_status_encoding = {'Non-Smoker': 1, 'Regular': 3, 'Occasional': 2}
    bmi_category_encoding = {'Normal': 2, 'Obesity': 4, 'Overweight': 3, 'Underweight': 1}

    df = pd.DataFrame(0, columns=expected_columns, index=[0])
    # df.fillna(0, inplace=True)

    # Manually assign values for each categorical input based on input_dict
    for key, value in input_data.items():
        if key == 'Gender' and value == 'Male':
            df['gender_Male'] = 1
        elif key == 'Region':
            if value == 'Northwest':
                df['region_Northwest'] = 1
            elif value == 'Southeast':
                df['region_Southeast'] = 1
            elif value == 'Southwest':
                df['region_Southwest'] = 1
        elif key == 'Marital Status' and value == 'Unmarried':
            df['marital_status_Unmarried'] = 1
        elif key == 'Employment Status':
            if value == 'Salaried':
                df['employment_status_Salaried'] = 1
            elif value == 'Self-Employed':
                df['employment_status_Self-Employed'] = 1
        elif key == 'Insurance Plan':  # Correct key usage with case sensitivity
            df['insurance_plan'] = insurance_plan_encoding.get(value, 1)
        elif key == 'BMI Category':
            df['bmi_category'] = bmi_category_encoding.get(value,1)
        elif key == 'Smoking Status':
            df['smoking_status'] = smoking_status_encoding.get(value, 1)
        elif key == 'Age':  # Correct key usage with case sensitivity
            df['age'] = value
        elif key == 'Number of Dependants':  # Correct key usage with case sensitivity
            df['number_of_dependants'] = value
        elif key == 'Income in Lakhs':  # Correct key usage with case sensitivity
            df['income_lakhs'] = value
        elif key == "Genetical Risk":
            df['genetical_risk'] = value

    # Assuming the 'normalized_risk_score' needs to be calculated based on the 'age'
    df['normalized_risk_score'] = calculate_normalized_risk(input_data['Medical History'])
    df = handle_scaling(input_data['Age'], df)

    return df



# Handle scaling based on age
def handle_scaling(age, df):
    scaler_object = scaler_young if age <= 25 else scaler_rest
    col_to_scale = scaler_object['col_to_scale']
    scaler = scaler_object['scaler']
    df['income_level'] = None  # Placeholder for scaler compatibility
    df[col_to_scale] = scaler.transform(df[col_to_scale])
    df.drop('income_level', axis='columns', inplace=True)
    return df


# Predict premium based on input data
def predict(input_data):
    input_df = preprocess_input(input_data)
    model = model_young if input_data['Age'] <= 25 else model_rest
    prediction = model.predict(input_df)
    return int(prediction[0])

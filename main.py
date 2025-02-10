import streamlit as st
import time
from predition_helper import predict
# Set up the Streamlit interface
st.title("🏦 Health Premium Prediction")
st.subheader("Provided by AtliQ Health Insurance")

# Display bank banner
st.image("https://via.placeholder.com/728x90.png?text=YourBank+Health+Insurance", use_container_width=True)

# Add a simple animation
with st.spinner('Loading health premium prediction interface...'):
    time.sleep(1)

# Arrange inputs in three columns per row with emojis
col1, col2, col3 = st.columns(3)
with col1:
    age = st.slider("🎂 Age", min_value=18, max_value=100, value=30)
with col2:
    gender = st.selectbox("👫 Gender", ["Male", "Female"])
with col3:
    region = st.selectbox("🌍 Region", ["Northwest", "Southeast", "Northeast", "Southwest"])

col4, col5, col6 = st.columns(3)
with col4:
    marital_status = st.selectbox("💍 Marital Status", ["Unmarried", "Married"])
with col5:
    number_of_dependants = st.selectbox("👨‍👩‍👧‍👦 Number of Dependants", [0, 1, 2, 3, 4, 5])
with col6:
    bmi_category = st.selectbox("🏋️ BMI Category", ["Underweight", "Normal", "Overweight", "Obesity"])

col7, col8, col9 = st.columns(3)
with col7:
    smoking_status = st.selectbox("🚬 Smoking Status", ["Non-Smoker", "Occasional", "Regular"])
with col8:
    employment_status = st.selectbox("💼 Employment Status", ["Salaried", "Self-Employed", "Freelancer"])
with col9:
    income_lakhs = st.number_input("💰 Income in Lakhs", min_value=1, max_value=100, value=10)

col10, col11, col12 = st.columns(3)
with col10:
    medical_history = st.selectbox(
        "🩺 Medical History",
        ["No Disease", "Diabetes", "High blood pressure", "Heart disease", "Thyroid",
         "Diabetes & High blood pressure", "High blood pressure & Heart disease", "Diabetes & Thyroid", "Diabetes & Heart disease"]
    )
with col11:
    insurance_plan = st.selectbox("📜 Insurance Plan", ["Bronze", "Silver", "Gold"])
with col12:
    genetical_risk = st.slider("🧬 Genetical Risk (0-5)", min_value=0, max_value=5, value=2)
input_data = {
    'Age': age,
    'Number of Dependants': number_of_dependants,
    'Income in Lakhs': income_lakhs,
    'Genetical Risk': genetical_risk,
    'Insurance Plan': insurance_plan,
    'Employment Status': employment_status,
    'Gender': gender,
    'Marital Status': marital_status,
    'BMI Category': bmi_category,
    'Smoking Status': smoking_status,
    'Region': region,
    'Medical History': medical_history
}
# Button to trigger prediction (placeholder)
if st.button("Predict Premium"):
    with st.spinner('Calculating premium...'):
        time.sleep(2)  # Simulate calculation delay
    prediction = predict(input_data)
    st.success(f'Predicted Health Insurance Cost :{prediction}')


import streamlit as st
from fitness_prompt import (
    generate_workout_plan,
    generate_meal_plan,
    generate_pdf
)

# Streamlit page configuration
st.set_page_config(page_title="AI Fitness Trainer", layout="centered")
st.title("✨ FitGenie AI ✨")

# Create tabs for Workout and Meal Plan
tab1, tab2 = st.tabs(["💪 Workout Plan", "🍽️ Meal Plan"])

# ======================== Workout Plan Tab ======================== #
with tab1:
    st.subheader("Generate Your Personalized Workout Plan")

    # Input sidebar for workout
    st.sidebar.header("Workout Info")
    age = st.sidebar.number_input("Age", min_value=10, max_value=100, value=25)
    gender = st.sidebar.selectbox("Gender", ["Male", "Female"])
    height = st.sidebar.number_input("Height (cm)", min_value=100, max_value=250, value=175)
    weight = st.sidebar.number_input("Weight (kg)", min_value=30, max_value=200, value=70)
    goal = st.sidebar.selectbox("Fitness Goal", ["Strength", "Hypertrophy", "Toning"])

    # BMI Calculation
    height_m = height / 100
    bmi = round(weight / (height_m ** 2), 2)
    st.markdown(f"**Your BMI:** `{bmi}`")

    if st.button("Generate Workout Plan"):
        with st.spinner("Generating your workout plan using AI..."):
            plan = generate_workout_plan(age, gender, height, weight, bmi, goal)
            st.success("✅ Workout Plan Generated")
            st.markdown(plan)

            # Export as PDF
            pdf_bytes = generate_pdf("Workout Plan", plan)
            st.download_button("📄 Download Workout Plan as PDF", data=pdf_bytes, file_name="workout_plan.pdf")

# ======================== Meal Plan Tab ======================== #
with tab2:
    st.subheader("Generate Your Personalized Meal Plan")

    # Input sidebar for meal
    st.sidebar.header("Meal Plan Info")
    meal_goal = st.sidebar.selectbox("Meal Goal", ["Muscle Gain", "Fat Loss", "Maintenance"])
    meal_type = st.sidebar.selectbox("Diet Type", ["No Preference", "Vegetarian", "Vegan", "Keto", "High Protein"])

    if st.button("Generate Meal Plan"):
        with st.spinner("Generating your meal plan using AI..."):
            meal_plan = generate_meal_plan(weight, height, age, gender, meal_goal, meal_type)
            st.success("✅ Meal Plan Generated")
            st.markdown(meal_plan)

            # Export as PDF
            pdf_bytes = generate_pdf("Meal Plan", meal_plan)
            st.download_button("📄 Download Meal Plan as PDF", data=pdf_bytes, file_name="meal_plan.pdf")

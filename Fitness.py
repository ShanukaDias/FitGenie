import streamlit as st
from fitness_prompt import (
    generate_workout_plan,
    generate_home_workout_plan,
    generate_meal_plan,
    calculate_bmi,
    generate_pdf
)

# Set page config
st.set_page_config(page_title="FitGenie", layout="wide", page_icon="🏋️")
st.markdown("<h1 style='text-align: center;'>✨ FitGenie ✨</h1>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center; color: grey;'>Your Personalized Workout & Meal Plans Powered by AI</h5>", unsafe_allow_html=True)
st.divider()

# Tabs
tab1, tab2 = st.tabs(["💪 Workout Plan", "🍽️ Meal Plan"])

# ======================== Workout Plan Tab ======================== #
with tab1:
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("👤 Enter Your Details")
        age = st.number_input("Age", min_value=10, max_value=100, value=25)
        gender = st.selectbox("Gender", ["Male", "Female"])
        height = st.number_input("Height (cm)", min_value=100, max_value=250, value=170)
        weight = st.number_input("Weight (kg)", min_value=30, max_value=200, value=70)
        goal = st.selectbox("Fitness Goal", ["Strength", "Hypertrophy", "Toning"])
        workout_type = st.radio("Workout Type", ["Gym", "Home"], horizontal=True)

        bmi = calculate_bmi(weight, height)
        st.markdown(f"### 🧮 Your BMI: `{bmi}`")

        if st.button("Generate Workout Plan", use_container_width=True):
            with st.spinner("💡 AI is generating your workout plan..."):
                if workout_type == "Gym":
                    plan = generate_workout_plan(age, gender, height, weight, bmi, goal)
                else:
                    plan = generate_home_workout_plan(age, gender, height, weight, bmi, goal)

                st.success("✅ Workout Plan Generated Successfully!")
                st.markdown("### 📋 Your AI-Powered Workout Plan:")
                st.markdown(plan)
                st.balloons()

                pdf_bytes = generate_pdf("Workout Plan", plan)
                st.download_button("📄 Download as PDF", data=pdf_bytes, file_name="workout_plan.pdf", use_container_width=True)

    with col2:
        st.image("https://images.pexels.com/photos/414029/pexels-photo-414029.jpeg", use_container_width=True, caption="Train Smart with AI 💪")

# ======================== Meal Plan Tab ======================== #
with tab2:
    col3, col4 = st.columns([1, 2])

    with col3:
        st.subheader("🍏 Nutrition Profile")
        meal_goal = st.selectbox("Nutrition Goal", ["Muscle Gain", "Fat Loss", "Maintenance"])
        meal_type = st.selectbox("Diet Preference", ["No Preference", "Vegetarian", "Vegan", "Keto", "High Protein"])

        if st.button("Generate Meal Plan", use_container_width=True):
            with st.spinner("🍽️ AI is preparing your personalized meal plan..."):
                meal_plan = generate_meal_plan(weight, height, age, gender, meal_goal, meal_type)

                st.success("✅ Meal Plan Ready!")
                st.markdown("### 🥗 Your AI-Powered Meal Plan:")
                st.markdown(meal_plan)
                st.balloons()

                pdf_bytes = generate_pdf("Meal Plan", meal_plan)
                st.download_button("📄 Download as PDF", data=pdf_bytes, file_name="meal_plan.pdf", use_container_width=True)

    with col4:
        st.image("https://images.pexels.com/photos/1640777/pexels-photo-1640777.jpeg", use_container_width=True, caption="Eat Smart, Stay Fit 🥗")

# Footer
st.divider()
st.markdown("<p style='text-align: center; color: grey;'>Made By Shanuka Dias</p>", unsafe_allow_html=True)

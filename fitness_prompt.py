
import requests
import os
from dotenv import load_dotenv
from fpdf import FPDF
from io import BytesIO


API_KEY = st.secrets["OPENROUTER_API_KEY"]
MODEL = "openai/gpt-3.5-turbo"

# ------------------ OpenRouter Prompt Caller ------------------ #
def call_openrouter(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://yourprojectname.streamlit.app",  # Optional
        "X-Title": "AI Fitness Trainer"
    }

    data = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
    response.raise_for_status()
    return response.json()['choices'][0]['message']['content']

# ------------------ Generate Workout Plan ------------------ #
def generate_workout_plan(age, gender, height, weight, bmi, goal):
    prompt = f"""
You are a certified personal trainer. Based on this user profile:

- Age: {age}
- Gender: {gender}
- Height: {height} cm
- Weight: {weight} kg
- BMI: {bmi}
- Fitness Goal: {goal}

Create a detailed weekly workout plan:
- Include days (e.g., Monday, Tuesday…)
- 4–6 exercises per day
- Mention sets and reps
- Highlight which muscles are trained each day
"""
    return call_openrouter(prompt)

# ------------------ Generate Meal Plan ------------------ #
def generate_meal_plan(weight, height, age, gender, goal, diet_type):
    prompt = f"""
You are a certified nutritionist. Based on this profile:

- Age: {age}
- Gender: {gender}
- Height: {height} cm
- Weight: {weight} kg
- Goal: {goal}
- Diet Preference: {diet_type}

Create a full daily meal plan including:
- Breakfast, Lunch, Dinner, Snacks
- Approximate calories per meal
- Macronutrient breakdown if possible
"""
    return call_openrouter(prompt)

# ------------------ PDF Generation ------------------ #
def generate_pdf(title, content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.multi_cell(0, 10, title)
    pdf.set_font("Arial", size=12)

    # Write content line-by-line
    for line in content.split("\n"):
        pdf.multi_cell(0, 8, line)

    # Convert to byte stream
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    return BytesIO(pdf_bytes)

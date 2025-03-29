# 💪🏼 AI based Personal Fitness Tracker App

A simple and interactive fitness tracking web application built with **Python** and **Streamlit**, designed to estimate calories burned during workouts and log fitness activities. This project was developed as part of AICTE- Internship on AI: Transformative Learning with TechSaksham, to demonstrate applied knowledge of machine learning and data visualization.
You can view it 👉🏼 [here](https://im-poojitha-ai-based-fitness-tracker-app-dfr7ab.streamlit.app/)

---

## 🚀 Features

- 📈 Predict calories burned based on user parameters (age, gender, height, weight, BMI, heart rate, body temperature, and workout duration)
- 📝 Automatically log each workout session with a timestamp
- 📊 View your complete workout history in an interactive table
- 🎯 Track monthly calorie burn progress against a custom fitness goal
- 🔍 Filter logs by date for better analysis
- 📉 Visual insights from workout logs using line charts, bar plots, and boxplots
- 📤 Download your log as a CSV file
- 🧹 Option to clear all logs with a single click

---

## ⚙️ Tech Stack

- **Python**
- **Streamlit** – for building the frontend interface
- **Scikit-learn** – for model training and prediction
- **Pandas & NumPy** – for data handling
- **Matplotlib & Seaborn** – for data visualization
- **Joblib** – for saving/loading the ML model

---

## 📂 Project Structure
```
📁 Fitness_Tracker/ 
├── datasets/
│   ├── cleaned_data.csv 
│   └── user_logs.csv 
├── calories_burned_model.pkl 
├── app.py 
└── README.md
```

---

## 💡 How It Works

1. The user enters personal and workout details through the sidebar.
2. The app calculates BMI and predicts calories burned using a pre-trained machine learning model.
3. Each prediction is saved in a log file (`user_logs.csv`) with timestamped entries.
4. The Workout Log tab provides detailed comparisons, and progress tracking visuals.

---

## 📦 Installation & Setup

1. **Clone the repository**
```bash
git clone https://github.com/your-username/personal-fitness-tracker.git
cd personal-fitness-tracker
```

2. **Install required packages**
Make sure you have Python installed. Then install all the necessary dependencies using:
```bash
pip install -r requirements.txt
```

3. **Run the Streamlit app**
Use the following command to start the app:
```bash
streamlit run app.py
```

4. **Explore the application**
Once the app launches, your default web browser will open the Streamlit interface.  
From there, you can:
- Enter your workout details in the sidebar
- View calorie predictions
- Explore logs and visual insights
- Download or clear your workout history

---

✅ *Note*: Make sure the following files are present in the project directory:
- `calories_burned_model.pkl` (pre-trained model file)
- `datasets/cleaned_data.csv` (for similar user comparison)

If not present, update paths or add the required files to ensure smooth functioning.

import streamlit as st
import joblib
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os
from datetime import datetime, date

# loading the model
model = joblib.load("calories_burned_model.pkl")

st.set_page_config(
    page_title = "💪 Personal Fitness Tracker",
    layout = "wide"
)

log_path = os.path.join("datasets", "user_logs.csv")

# session state logs initialization
if "logs" not in st.session_state:
    if os.path.exists(log_path):
        st.session_state.logs = pd.read_csv(log_path)
        st.session_state.logs["Timestamp"] = pd.to_datetime(st.session_state.logs["Timestamp"], errors='coerce')
        st.session_state.logs = st.session_state.logs.dropna(subset=["Timestamp"])
    else:
        st.session_state.logs = pd.DataFrame(columns=["Timestamp", "Age", "Gender", "Height_cm", "Weight_kg", "BMI", "Duration_mins", "Heart_Rate", "Body_Temperature", "Calories_Burned"])


# naviagtion tabs setup
tab1, tab2 = st.tabs(["💪 Calorie Prediction", "📜 Workout Log"])

# TAB 1: CALORIE PREDICTION

with tab1:
    st.title("Personal Fitness Tracker")
    st.subheader("Track your workout and understand how many calories you burn!")


    st.sidebar.header("Enter your details")

    age = st.sidebar.slider("Age", 16, 80, 24)
    gender_display = st.sidebar.selectbox("Gender", ["Male", "Female"])
    gender = gender_display.lower()

    height_cm = st.sidebar.number_input("Height (cm)", min_value = 100, max_value = 220, value = 150)
    weight_kg = st.sidebar.number_input("Weight (kg)", min_value = 30.0, max_value = 200.0, value = 55.0)

    height_m = height_cm/100
    bmi = round(weight_kg/(height_m ** 2), 2)

    st.sidebar.markdown(f"**BMI:**`{bmi:.2f}`")

    duration = st.sidebar.slider("Workout Duration(mins)", 5, 120, 30)
    heart_rate = st.sidebar.slider("Heart Rate (bpm)", 60, 200, 100)
    body_temp = st.sidebar.slider("Body Temperate (C)", 35.0, 42.0, 37.0)

    gender_encode = 1 if gender == "Male" else 0


    # User inputs
    if st.sidebar.button("Check Calories Burned"):
        user_input = pd.DataFrame([{
            "Gender": gender_encode,
            "Age": age,
            "Height": height_cm,
            "Weight": weight_kg,
            "Duration": duration,
            "Heart_Rate": heart_rate,
            "Body_Temp": body_temp
        }])
        predicted_calories = model.predict(user_input)[0]

        # logging user data 

        log_data = {
            "Timestamp": datetime.now(),
            "Age": age,
            "Gender": gender,
            "Height_cm": height_cm,
            "Weight_kg": weight_kg,
            "BMI": bmi,
            "Duration_mins": duration,
            "Heart_Rate": heart_rate,
            "Body_Temperature": body_temp,
            "Calories_Burned": predicted_calories
        }

        new_log = pd.DataFrame([log_data])
        st.session_state.logs = pd.concat([st.session_state.logs, new_log], ignore_index=True)

        st.session_state.logs.to_csv("datasets/user_logs.csv", index=False)

        # User input summary
        summary_data = {
            "Parameter": ["Age", "Gender", "Height (cm)", "Weight (kg)", "BMI", "Duration (mins)", "Heart Rate (bpm)", "Body Temperature (°C)"],
            "Value": [age, gender, height_cm, weight_kg, bmi, duration, heart_rate, body_temp]
        }
        summary_df = pd.DataFrame(summary_data)

        # section break
        st.markdown("---")

        # input summary
        st.markdown("### 🧾 Summary of Your Inputs")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Age", age)
            st.metric("Gender", gender.capitalize())

        with col2:
            st.metric("Height (cm)", height_cm)
            st.metric("Weight (kg)", weight_kg)

        with col3:
            st.metric("BMI", round(bmi, 2))
            st.metric("Duration (mins)", duration)

        with col4:
            st.metric("Heart Rate (bpm)", heart_rate)
            st.metric("Body Temp (°C)", body_temp)
        
        st.success(f"🔥Estimated Calories Burned: **{predicted_calories:.2f} kcal**")

        # section break
        st.markdown("---")

        # finding similar users based on calories burned

        exercise_df = pd.read_csv("datasets/cleaned_data.csv")
        similar_users = exercise_df[(exercise_df["Calories"] >= predicted_calories - 10) &
                                    (exercise_df["Calories"] >= predicted_calories + 10)]
        st.markdown("### 🧑‍🤝‍🧑 Similar Results")
        st.dataframe(similar_users[['Age', 'Gender', 'Duration', 'Calories']].head(10))

        # section break
        st.markdown("---")
        ## calories vs age
        exercise_df["age_group"] = pd.cut(exercise_df["Age"], bins=[10, 20, 30, 40, 50, 60, 70, 80], 
                                    labels=["10-20", "21-30", "31-40", "41-50", "51-60", "61-70", "71-80"])

        avg_by_age = exercise_df.groupby("age_group")["Calories"].mean().reset_index()
        avg_by_gender = exercise_df.groupby("Gender")["Calories"].mean().reset_index()

        if gender in avg_by_gender["Gender"].values:
            avg_gender_val = avg_by_gender.loc[avg_by_gender["Gender"] == gender, "Calories"].values[0]
        else:
            avg_gender_val = 0


        # Find age group for current user
        def get_age_group(age):
            if age <= 20: return "10-20"
            elif age <= 30: return "21-30"
            elif age <= 40: return "31-40"
            elif age <= 50: return "41-50"
            elif age <= 60: return "51-60"
            elif age <= 70: return "61-70"
            else: return "71-80"

        user_age_group = get_age_group(age)
        if user_age_group in avg_by_age["age_group"].values:
            avg_age_val = avg_by_age.loc[avg_by_age['age_group'] == user_age_group, "Calories"].values[0]
        else:
            avg_age_val = 0

        st.markdown("## 📊 Comparison with Average Calories Burned")
        col1, col2, col3 = st.columns(3)
        col1.metric("Predicted Calories", f"{predicted_calories:.2f} cal")
        col2.metric(f"Avg Calories (Age {user_age_group})", f"{avg_age_val:.2f} cal")
        col3.metric(f"Avg Calories ({gender_display})", f"{avg_gender_val:.2f} cal")


        # data visualization

        st.markdown("### Calories Burned vs Workout Duration")

        avg_calories = np.mean(exercise_df["Calories"])
        labels = ['Your Calories', 'Avg Calories']

        values = [predicted_calories, avg_calories]
        colors = ['orange', 'skyblue']

        fig, ax = plt.subplots()
        bars = ax.barh(labels, values, color=colors)

        for bar in bars:
            xval = bar.get_width()
            ax.text(xval + 5, bar.get_y() + bar.get_height()/2, f"{xval:.0f}", va="center", fontsize=10)

        plt.figure(figsize=(2,5))
        ax.set_xlabel("Calories Burned Comparison")
        st.pyplot(fig)


    else:
        st.write("👆 Enter your workout details from the sidebar to get started!")


# TAB 2: WORKOUT LOG VIEW

with tab2:
    st.title("📝 Your Workout Log")

    if not st.session_state.logs.empty:
        logs = st.session_state.logs.copy()
        st.subheader("📋 Full Workout Logs")
        st.dataframe(logs)

        st.markdown("---")
        
        st.subheader("📆 Filter Logs by Date")
        start_date = st.date_input("Start Date", date.today())
        filtered_logs = logs[logs["Timestamp"] >= pd.to_datetime(start_date)]


        if not filtered_logs.empty:
            st.dataframe(filtered_logs)

            # Monthly goal tracking
            st.markdown("### 🎯 Monthly Goal Tracker")
            goal = st.number_input("Enter Monthly Calorie Goal (kcal)", value=5000)

            current_month = datetime.now().month
            monthly_burned = filtered_logs[filtered_logs["Timestamp"].dt.month == current_month]["Calories_Burned"].sum()

            progress = (monthly_burned / goal) * 100
            st.metric("Calories Burned This Month", f"{monthly_burned:.2f} kcal")
            st.progress(min(progress/100, 1.0), text=f"{progress:.2f}% of Monthly Goal Achieved")

        else:
            st.info("No logs found for the selected date range.")


        st.markdown("---")
        # data visualization
        st.markdown("### 📈 Calories Burned Over Time")

        fig1, ax1 = plt.subplots(figsize=(10, 5))
        ax1.plot(logs["Timestamp"], logs["Calories_Burned"], marker='o', linestyle='-', color='crimson')
        ax1.set_xlabel("Date")
        ax1.set_ylabel("Calories Burned")
        ax1.set_title("Calories Burned Over Time")
        ax1.grid(True)
        st.pyplot(fig1)


        st.markdown("---")
        st.write("⬇️ Download your workout log file!")
        # download log
        st.download_button("⬇️ Download Log", logs.to_csv(index=False), file_name="my_workout_log.csv")

        st.markdown("---")
        if st.button("🧹 Clear Workout Logs"):
            # Clear from session
            st.session_state.logs = pd.DataFrame(columns=["Timestamp", "Age", "Gender", "Height_cm", "Weight_kg", "BMI",
                                                        "Duration_mins", "Heart_Rate", "Body_Temperature", "Calories_Burned"])
            
            # Clear from file (optional)
            st.session_state.logs.to_csv(log_path, index=False)
            
            st.success("✅ Workout logs cleared successfully!")


    else:
        st.warning("No workouts logged yet! Try logging a workout first.")

from flask import Flask, request, render_template
import joblib
import os  # ✅ Import os to manage file paths

app = Flask(__name__)

# ✅ Construct full path to model.pkl regardless of where script is run
model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
model = joblib.load(model_path)  # Load trained model

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        study_hours = float(request.form['StudyHours'])
        sleep_hours = float(request.form['SleepHours'])
        internet_hours = float(request.form['InternetUsage'])
        travel_hours = float(request.form['TravelTime'])

        # 🛑 Validation: Check if total hours exceed 24
        total_hours = study_hours + sleep_hours + internet_hours + travel_hours
        if total_hours > 24:
            error_msg = f"Error: You entered a total of {total_hours} hours, which exceeds 24 hours in a day. ⏳ Please adjust your inputs."
            return render_template('index.html', prediction_text=error_msg)

        # ✅ If valid, continue
        features = [
            float(request.form['Age']),
            float(request.form['Gender']),
            study_hours,
            sleep_hours,
            float(request.form['Attendance']),
            float(request.form['HomeworkDone']),
            internet_hours,
            float(request.form['PartTimeJob']),
            float(request.form['ClassParticipation']),
            float(request.form['HealthRating']),
            float(request.form['ParentEducation']),
            travel_hours,
            float(request.form['PastFailures']),
            float(request.form['FamilySupport']),
            float(request.form['ExtraActivities'])
        ]

        prediction = model.predict([features])[0]
        grade = round(prediction, 2)

        if grade >= 80:
            advice = "Excellent! Keep up the great work. 🎉"
        elif grade >= 60:
            advice = "Good job! Stay consistent to improve further. 💪"
        elif grade >= 40:
            advice = "You need to work on studies and class participation. 📚"
        else:
            advice = "Warning! Increase study hours and focus more in class. 🚨"

        result = f"Predicted Grade: {grade}%. {advice}"
        return render_template('index.html', prediction_text=result)

    except Exception as e:
        return render_template('index.html', prediction_text=f'Error: {str(e)}')

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
        features = [
            float(request.form['Age']),
            float(request.form['Gender']),
            float(request.form['StudyHours']),
            float(request.form['SleepHours']),
            float(request.form['Attendance']),
            float(request.form['HomeworkDone']),
            float(request.form['InternetUsage']),
            float(request.form['PartTimeJob']),
            float(request.form['ClassParticipation']),
            float(request.form['HealthRating']),
            float(request.form['ParentEducation']),
            float(request.form['TravelTime']),
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

if __name__ == '__main__':
    app.run(debug=True)

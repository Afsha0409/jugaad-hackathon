from flask import Flask, render_template, request
import datetime
import random

app = Flask(__name__)
companion = None

class StudyCompanion:
    def __init__(self):
        self.study_schedule = []

    def generate_study_schedule(self, daily_routine, total_study_hours, subjects):
        print("\nLet's create your personalized study schedule!")
        study_start_time = daily_routine['wakeup_time'] + datetime.timedelta(hours=8)  # Start from 8 AM

        while total_study_hours > 0 and subjects:
            session_duration = min(random.randint(30, 120), total_study_hours * 60)  # Random duration, max 2 hours
            study_end_time = study_start_time + datetime.timedelta(minutes=session_duration)

            subject = subjects.pop(0)  # Pop the first subject/plan
            self.study_schedule.append(
                {
                    'start_time': study_start_time.strftime('%I:%M %p'),
                    'end_time': study_end_time.strftime('%I:%M %p'),
                    'subject': subject,
                }
            )

            study_start_time = study_end_time
            total_study_hours -= session_duration / 60

    def display_schedule(self):
        return self.study_schedule

@app.route('/', methods=['GET', 'POST'])
def index():
    global companion
    if request.method == 'POST':
        student_wakeup_time = request.form['wakeup_time']
        wakeup_time = datetime.datetime.strptime(student_wakeup_time, '%H:%M')

        total_study_hours = int(request.form['total_study_hours'])

        # Get subjects/plans from the form
        subjects = request.form.getlist('subject')

        companion = StudyCompanion()
        student_daily_routine = {
            'wakeup_time': wakeup_time,
        }

        companion.generate_study_schedule(student_daily_routine, total_study_hours, subjects)

    return render_template('index.html', schedule=companion.display_schedule() if companion else None)

if __name__ == '__main__':
    app.run(debug=True)

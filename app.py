from flask import Flask, render_template, request, jsonify
#from time import sleep
from RpiMotorLib import RpiMotorLib

#define GPIO pins
#GPIO_pins = (14, 15, 18) # Microstep Resolution MS1-MS3 -> GPIO Pin
direction= 20       # Direction -> GPIO Pin
step = 21      # Step -> GPIO Pin

# Declare an named instance of class pass GPIO pins numbers
stepper = RpiMotorLib.A4988Nema(direction, step, (21,21,21), "A4988")

app = Flask(__name__)

steps = 300

# Variable to store the scores
current_scores = []

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/process_result', methods=['POST'])
def process_result():
    global current_scores
    if request.method == 'POST':
        # Get the JSON data sent from the frontend
        data = request.json

        # Process the data as needed
        scores = data.get('scores', [])

        # Update the current scores
        current_scores = scores

        moveMotor(current_scores)

        # You can perform further processing or return the scores as JSON
        return jsonify({'scores': scores})


@app.route('/get_scores')
def get_scores():
    return jsonify({'scores': current_scores})


def moveMotor(result):
    if result == "Background Noise":
        stepper.motor_run(steps)
        print("moving motor")
    elif result == "Class 2":
        stepper.motor_run(-steps)
        print("moving motor")
    

if __name__ == '__main__':
    app.run(debug=True, port=8000)

    
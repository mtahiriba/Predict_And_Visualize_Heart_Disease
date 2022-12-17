from flask import Flask, render_template, request
from sklearn.preprocessing import LabelEncoder
import webbrowser
from pickle import load

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def predict():

    if request.method == 'POST':
        bmi = request.form['BMI']
        physical = request.form['Physical']
        mental = request.form['Mental']
        smoking = request.form.get('Smoking')
        stroke = request.form.get('Stroke')
        diffWalking = request.form.get('DiffWalking')
        diabetic = request.form.get('Diabetic')
        asthma = request.form.get('Asthma')
        kidneyDisease = request.form.get('KidneyDisease')
        skinCancer = request.form.get('SkinCancer')
        sex = request.form.get('sex')
        age = request.form.get('age')
        race = request.form.get('race')
        
        # Convert to float
        bmi = float(bmi)
        physical = float(physical)
        mental = float(mental)

        # Convert to binary
        if(smoking == "YES"):
            smoking = 1
        else:
            smoking = 0

        if(stroke == "YES"):
            stroke = 1
        else:
            stroke = 0

        if(diffWalking == "YES"):
            diffWalking = 1
        else:
            diffWalking = 0
        
        if(asthma == "YES"):
            asthma = 1
        else:
            asthma = 0
        
        if(kidneyDisease == "YES"):
            kidneyDisease = 1
        else:
            kidneyDisease = 0

        if(skinCancer == "YES"):
            skinCancer = 1
        else:
            skinCancer = 0

        le = LabelEncoder()
        le.fit(["male",'female'])
        sex = le.transform([sex])[0]


        le.fit(['White','Black','Asian','American Indian/Alaskan Native','Hispanic','Other'])
        race = le.transform([race])[0]

        le.fit(["18-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-59", "60-64", "65-69", "70-74", "75-79", "80 or older"])
        age = le.transform([age])[0]

        le.fit(["Yes", "No", "Yes (during pregnancy)", "No borderline diabetes"])
        diabetic = le.transform([diabetic])[0]

        lis = [bmi, smoking, stroke, physical, mental, diffWalking, sex, age, race, diabetic, asthma, kidneyDisease, skinCancer]

        scl = load(open('scalar.pkl', 'rb'))
        x = scl.transform([lis])

        model = load(open('Random_forest_classifier.pkl', 'rb'))
        prediction = model.predict(x)[0]

        if(prediction == 1):
            prediction = "Positive"
        else:
            prediction = "Negative"

    return render_template('result.html', 
                            LIST = lis,
                            X = x,
                            PREDICTION = prediction
                            )

if __name__ == '__main__':
    # webbrowser.open_new('http://127.0.0.1:5000/')
    app.run(port=5000 ,debug=True)


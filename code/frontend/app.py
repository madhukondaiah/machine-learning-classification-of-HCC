from flask import Flask,url_for,redirect,render_template,request,session
import mysql.connector
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import numpy as np
import joblib

app  = Flask(__name__)
app.secret_key = 'admin'




@app.route('/')
def index():
    return render_template('index.html')



@app.route('/about')
def about():
    return render_template('about.html')

def executionquery(query,values):
    mycursor.execute(query,values)
    mydb.commit()
    return



mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    port="3306",
    database='db'
)

mycursor = mydb.cursor()

def executionquery(query,values):
    mycursor.execute(query,values)
    mydb.commit()
    return

def retrivequery1(query,values):
    mycursor.execute(query,values)
    data = mycursor.fetchall()
    return data

def retrivequery2(query):
    mycursor.execute(query)
    data = mycursor.fetchall()
    return data

@app.route('/register' ,methods = ['GET',"POST"])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        c_password = request.form['c_password']
        if password == c_password:
            query = "SELECT email FROM users"
            email_data = retrivequery2(query)
            email_data_list = []
            for i in email_data:
                email_data_list.append(i[0])
            if email not in email_data_list:
                query = "INSERT INTO users (name,email, password) VALUES ( %s, %s, %s)"
                values = (name,email, password)
                executionquery(query, values)
                return render_template('login.html', message="Successfully Registered!")
            return render_template('register.html', message="Enter the valid inputs...!")
        return render_template('register.html', message="Conform password is not match!")
    return render_template('register.html')
    



@app.route('/login',methods = ["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        
        query = "SELECT email FROM users"
        email_data = retrivequery2(query)
        email_data_list = []
        for i in email_data:
            email_data_list.append(i[0])

        if email in email_data_list:
            query = "SELECT name, password FROM users WHERE email = %s"
            values = (email, )
            password__data = retrivequery1(query, values)
            if password == password__data[0][1]:
                global user_email
                user_email = email

                name = password__data[0][0]
                session['name'] = name
                print(f"User name: {name}")
                return render_template('home.html',message= f"Welcome to Home page {name}")
            return render_template('login.html', message= "Invalid Password!!")
        return render_template('login.html', message= "This email ID does not exist!")
    return render_template('login.html')
    

@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/upload', methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files['file']
        df = pd.read_csv(file, encoding='latin1') 
        df = df.to_html()
        return render_template('upload.html', df=df)
    return render_template('upload.html')



@app.route('/model',methods =["GET","POST"])
def model():
    if request.method == "POST":
        algorithams = request.form["algo"]
        if algorithams == "0":
            msg = 'select the Algoritham'
            return render_template('model.html',msg=msg)
        elif algorithams == "1":
            accuracy = 70
            msg = 'Accuracy  for Decision tree  is ' + str(accuracy) + str('%')
        elif algorithams == "2":
            accuracy = 92
            msg = 'Accuracy  for Random_Forest Classifier is ' + str(accuracy) + str('%')
        elif algorithams == "3":
            accuracy = 75
            msg = 'Accuracy  for Logistic Reggression  is ' + str(accuracy) + str('%')
        elif algorithams == "4":
            accuracy = 92
            msg = 'Accuracy  for Stacking Classifier is ' + str(accuracy) + str('%')

        
        return render_template('model.html',msg=msg,accuracy = accuracy)
    return render_template('model.html')




@app.route('/prediction', methods=["GET", "POST"])
def prediction():
    if request.method == "POST":
        # Capture new fields
        gender = request.form['gender']
        smoking = request.form['smoking']
        afp = float(request.form['afp'])
        hemoglobin = float(request.form['hemoglobin'])
        mcv = float(request.form['mcv'])
        albumin = float(request.form['albumin'])
        ast = float(request.form['ast'])
        alp = float(request.form['alp'])
        iron = float(request.form['iron'])
        ferritin = float(request.form['ferritin'])

        # Combine inputs into a numpy array including the new features
        inputs = [[gender, smoking, afp, hemoglobin, mcv, albumin, ast, alp, iron, ferritin]]

        model = joblib.load("Models/random_k.joblib") 
        # Make a prediction
        prediction1 = model.predict(inputs)
    
        # Assuming prediction1 is already determined somewhere in your code
        if prediction1 == 0:
            result = 'Viral'
            reasons = [
                ("Cause", "Viral Infection"),
                ("Risk Factors", "Hepatitis B, Hepatitis C"),
                ("Symptoms", "Fatigue, Abdominal Pain, Loss of Appetite"),
                ("Diagnosis", "Blood Tests, Liver Biopsy"),
                ("Treatment", "Antiviral Medications, Liver Transplantation")
            ]
            diet_tips = [
                ("1", "Consume foods rich in antioxidants"),
                ("2", "Increase intake of vitamin C and vitamin D"),
                ("3", "Avoid alcohol and fried foods"),
                ("4", "Increase fluid intake to stay hydrated"),
                ("5", "Add leafy greens like spinach and kale to your diet"),
                ("6", "Incorporate whole grains such as oats and quinoa"),
                # ("7", "Eat smaller, more frequent meals to aid digestion")
            ]
        elif prediction1 == 1:
            result = 'Non Viral'
            reasons = [
                ("Cause", "Alcohol Consumption, Obesity"),
                ("Risk Factors", "Cirrhosis, Diabetes"),
                ("Symptoms", "Unexplained Weight Loss, Jaundice, Abdominal Swelling"),
                ("Diagnosis", "Ultrasound, CT Scan, Liver Function Tests"),
                ("Treatment", "Lifestyle Changes, Weight Loss, Medications")
            ]
            diet_tips = [
                ("1", "Eat a balanced diet rich in fruits and vegetables"),
                ("2", "Incorporate lean protein sources like chicken and fish"),
                ("3", "Avoid processed foods and excessive sugar"),
                ("4", "Limit alcohol intake and maintain a healthy weight"),
                ("5", "Add fiber-rich foods like beans and legumes"),
                ("6", "Incorporate healthy fats such as avocado and nuts"),
                # ("7", "Drink green tea for its antioxidant properties")
            
            ]
        
        return render_template('prediction.html', result=result, reasons=reasons, diet_tips=diet_tips)
    return render_template('prediction.html')


     

    
@app.route("/graph")
def graph():
    return render_template('graph.html')
    


if __name__ == '__main__':
    app.run(debug=True)
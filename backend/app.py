from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Shivu@24'
app.config['MYSQL_DB'] = 'healthcare_app'

mysql = MySQL(app)

# ---------------- HOME ----------------
@app.route('/')
def home():
    return "Healthcare Backend Running"


# ---------------- REGISTER USER ----------------
@app.route('/register', methods=['POST'])
def register():

    data = request.json
    name = data['name']
    email = data['email']
    password = data['password']
    age = data['age']
    gender = data['gender']

    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM users WHERE email=%s",(email,))
    user = cur.fetchone()

    if user:
        return jsonify({"message":"Email already registered"})

    cur.execute(
        "INSERT INTO users(name,email,password,age,gender) VALUES(%s,%s,%s,%s,%s)",
        (name,email,password,age,gender)
    )

    mysql.connection.commit()
    cur.close()

    return jsonify({"message":"User Registered Successfully"})

# ---------------- LOGIN USER ----------------
@app.route('/login', methods=['POST'])
def login():

    data = request.json
    email = data['email']
    password = data['password']

    cur = mysql.connection.cursor()

    cur.execute(
        "SELECT * FROM users WHERE email=%s AND password=%s",
        (email,password)
    )

    user = cur.fetchone()
    cur.close()

    if user:
        return jsonify({"message":"Login Success"})
    else:
        return jsonify({"message":"Invalid Credentials"})


# ---------------- GET DOCTORS ----------------
@app.route('/doctors', methods=['GET'])
def doctors():

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM doctors")
    data = cur.fetchall()
    cur.close()

    return jsonify(data)


# ---------------- BOOK APPOINTMENT ----------------
@app.route('/book_appointment', methods=['POST'])
def book_appointment():

    data = request.json

    user_id = data['user_id']
    doctor_id = data['doctor_id']
    appointment_date = data['appointment_date']
    status = "Booked"

    cur = mysql.connection.cursor()

    cur.execute(
        "INSERT INTO appointments(user_id,doctor_id,appointment_date,status) VALUES(%s,%s,%s,%s)",
        (user_id,doctor_id,appointment_date,status)
    )

    mysql.connection.commit()
    cur.close()

    return jsonify({"message":"Appointment Booked"})


# ---------------- HEALTH RECORD ----------------
@app.route('/add_health_record', methods=['POST'])
def add_health_record():

    data = request.json

    user_id = data['user_id']
    height = data['height']
    weight = data['weight']
    blood_pressure = data['blood_pressure']
    notes = data['notes']

    cur = mysql.connection.cursor()

    cur.execute(
        """INSERT INTO health_records(user_id,height,weight,blood_pressure,notes)
           VALUES(%s,%s,%s,%s,%s)""",
        (user_id,height,weight,blood_pressure,notes)
    )

    mysql.connection.commit()
    cur.close()

    return jsonify({"message":"Health record added"})


# ---------------- HEALTH TIPS / REELS ----------------
@app.route('/health_tips', methods=['GET'])
def health_tips():

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM health_tips")
    data = cur.fetchall()
    cur.close()

    return jsonify(data)


#if __name__ == "__main__":
   # app.run(debug=True)
@app.route('/search_doctors', methods=['GET'])
def search_doctors():

    specialization = request.args.get('specialization')

    cur = mysql.connection.cursor()

    cur.execute(
        "SELECT * FROM doctors WHERE specialization LIKE %s",
        ('%' + specialization + '%',)
    )

    data = cur.fetchall()
    cur.close()

    return jsonify(data)
@app.route('/health_ai', methods=['POST'])
def health_ai():

    data = request.json
    question = data['question']

    if "fever" in question:
        answer="Drink fluids and rest. Consult doctor if fever persists."

    elif "headache" in question:
        answer="Stay hydrated and rest. If severe consult doctor."

    else:
        answer="Please consult a doctor for better advice."

    return jsonify({"response":answer})    
@app.route('/get_health_records/<int:user_id>', methods=['GET'])
def get_health_records(user_id):

    cur = mysql.connection.cursor()

    cur.execute(
        "SELECT height, weight, blood_pressure, notes, created_at FROM health_records WHERE user_id=%s",
        (user_id,)
    )

    data = cur.fetchall()
    cur.close()

    return jsonify(data)
@app.route('/add_review', methods=['POST'])
def add_review():

    data = request.json

    doctor_id = data['doctor_id']
    user_id = data['user_id']
    rating = data['rating']
    review = data['review']

    cur = mysql.connection.cursor()

    cur.execute(
        "INSERT INTO doctor_reviews (doctor_id,user_id,rating,review) VALUES (%s,%s,%s,%s)",
        (doctor_id,user_id,rating,review)
    )

    mysql.connection.commit()

    return jsonify({"message":"Review added"})
@app.route('/get_reviews/<doctor_id>')
def get_reviews(doctor_id):

    cur = mysql.connection.cursor()

    cur.execute(
        "SELECT rating,review,created_at FROM doctor_reviews WHERE doctor_id=%s",
        (doctor_id,)
    )

    data = cur.fetchall()

    return jsonify(data)
if __name__ == "__main__":
    port=int(os.environ.get("port",5000))
     app.run(host="0.0.0.0",port=port)

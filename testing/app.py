from flask import Flask, render_template, request, redirect, url_for, flash
import pymongo
import bcrypt

app = Flask(__name__)  #for creating flask web server
app.secret_key = "your_secret_key"  # Used for session and flashing messages

# MongoDB connection
client = pymongo.MongoClient("mongodb://localhost:27017/")  # Adjust with your MongoDB connection string
db = client["user_database"]  # Database name
student_collection = db['student']  # Student collection
teacher_collection = db['teacher']  # Teacher collection

# Route for home page
@app.route('/')
def home():
    return redirect(url_for('login'))

# Route for registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        phone_number = request.form['phone_number']
        birth_date = request.form['birth_date']
        gender = request.form['gender']  # Get selected gender
        role = request.form.get('role')

        # Check if user already exists
        if role == 'student' and student_collection.find_one({"username": username}):
            flash("Student already exists!", "error")
            return redirect(url_for('register'))
        elif role == 'teacher' and teacher_collection.find_one({"username": username}):
            flash("Teacher already exists!", "error")
            return redirect(url_for('register'))

        # Hash the password using bcrypt
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Insert user data into the collection
        user_data = {
            "username": username,
            "password": hashed_password,
            "phone_number": phone_number,
            "birth_date": birth_date,
            "gender": gender,
            "role": role
        }

        # Insert into the corresponding collection based on role
        if role == 'student':
            student_collection.insert_one(user_data)
        elif role == 'teacher':
            teacher_collection.insert_one(user_data)

        flash("Registration successful!", "success")
        return redirect(url_for('login'))  # Redirect the user to the login page

    # Render the registration form
    return render_template('register.html')

# Route for login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        # Check role and authenticate from the corresponding collection
        if role == 'student':
            user = student_collection.find_one({"username": username})
        elif role == 'teacher':
            user = teacher_collection.find_one({"username": username})
        else:
            flash("Invalid role selected!", "error")
            return redirect(url_for('login'))

        if user:
            # Compare hashed password
            if bcrypt.checkpw(password.encode('utf-8'), user['password']):
                flash("Login successful!", "success")
                return redirect(url_for('welcome', username=username))  # Redirect to the welcome page
            else:
                flash("Incorrect password!", "error")
        else:
            flash("User not found!", "error")
    
    return render_template('login.html')

# Route for welcome page
@app.route('/welcome/<username>')
def welcome(username):
    return render_template('welcome.html', username=username)

if __name__ == "__main__":
    app.run(debug=True)

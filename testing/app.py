from flask import Flask, render_template, request, redirect, url_for, flash
import pymongo
import bcrypt

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Used for session and flashing messages

# MongoDB connection
client = pymongo.MongoClient("mongodb://localhost:27017/")  # Adjust with your MongoDB connection string
db = client["user_database"]  # Database name
collection = db["users"]  # Collection name

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
        
        # Check if user already exists
        if collection.find_one({"username": username}):
            flash("User already exists!", "error")
            return redirect(url_for('register'))
        
        # Hash the password using bcrypt
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Insert user data into the collection
        user_data = {"username": username,
                     "password": hashed_password,
                    "phone_number": phone_number,
                    "birth_date": birth_date,
                    "gender": gender}
        
        
        collection.insert_one(user_data)
        flash("Registration successful!", "success")
        return redirect(url_for('login'))
    
    return render_template('register.html')

# Route for login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = collection.find_one({"username": username})
        
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

from flask import Flask, request, redirect, session, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "secret_key"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'login'

mysql = MySQL(app)

@app.route("/")
def home():
    if "user_id" in session:
        user_id = session["user_id"]

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cur.fetchone()
        cur.close()

        return redirect("/dashboard")
    return render_template("login.html")

@app.route("/login", methods=['GET', 'POST'])
def login():

    if "user_id" in session:
        user_id = session["user_id"]

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cur.fetchone()
        cur.close()

        return redirect("/dashboard")
    
    if request.method == 'GET':
        return redirect('/')
    
    
    username = request.form["username"]
    password = request.form["password"]

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    cur.close()

    if user and user[2] == password:
        session["user_id"] = user[0]
        return redirect("/dashboard")
    else:
        return "Invalid username or password"

@app.route("/dashboard")
def dashboard():
    if "user_id" in session:
        user_id = session["user_id"]

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cur.fetchone()
        cur.close()

        return render_template("dashboard.html", user = user)
    else:
        return redirect("/")

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
    
if __name__ == "__main__":
    app.run(port = 8000)
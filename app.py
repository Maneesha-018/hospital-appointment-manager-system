from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


# DATABASE CREATE FUNCTION

def create_table():

    conn = sqlite3.connect("hospital.db")

    cursor = conn.cursor()

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS patients(

    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age TEXT,
    weight TEXT,
    bp TEXT,
    doctor TEXT,
    date TEXT,
    problem TEXT,
    payment TEXT

    )

    """)

    conn.commit()

    conn.close()


create_table()


# HOME PAGE

@app.route("/")

def home():

    return render_template("home.html")


# APPOINTMENT PAGE

@app.route("/appointment")

def appointment():

    return render_template("index.html")


# SAVE DATA INTO DATABASE

@app.route("/register", methods=["POST"])

def register():

    name = request.form["name"]

    age = request.form["age"]

    weight = request.form["weight"]

    bp = request.form["bp"]

    doctor = request.form["doctor"]

    date = request.form["date"]

    problem = request.form["problem"]

    payment = request.form["payment"]


    conn = sqlite3.connect("hospital.db")

    cursor = conn.cursor()


    cursor.execute("""

    INSERT INTO patients

    (name, age, weight, bp, doctor, date, problem, payment)

    VALUES (?, ?, ?, ?, ?, ?, ?, ?)

    """, (name, age, weight, bp, doctor, date, problem, payment))


    conn.commit()

    conn.close()


    return render_template("home.html")


# VIEW RECORD PAGE

@app.route("/view")

def view():

    conn = sqlite3.connect("hospital.db")

    cursor = conn.cursor()


    cursor.execute("SELECT * FROM patients")

    data = cursor.fetchall()


    conn.close()


    return render_template("view.html", patients=data)


# DELETE RECORD OPTION

@app.route("/delete/<int:id>")

def delete(id):

    conn = sqlite3.connect("hospital.db")

    cursor = conn.cursor()


    cursor.execute("DELETE FROM patients WHERE id=?", (id,))


    conn.commit()

    conn.close()


    return redirect("/view")


# SEARCH OPTION

@app.route("/search", methods=["POST"])

def search():

    keyword = request.form["keyword"]


    conn = sqlite3.connect("hospital.db")

    cursor = conn.cursor()


    cursor.execute("""

    SELECT * FROM patients

    WHERE name LIKE ?

    OR doctor LIKE ?

    OR payment LIKE ?

    """,

    ("%"+keyword+"%",

     "%"+keyword+"%",

     "%"+keyword+"%"))


    data = cursor.fetchall()


    conn.close()


    return render_template("view.html", patients=data)


# RUN SERVER

if __name__ == "__main__":

    app.run(debug=True)
    
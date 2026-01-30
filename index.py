from flask import Flask, render_template, request, redirect, url_for
import random
users = []
app = Flask(__name__)
@app.route("/")
def index():
    return render_template("index.html")
    
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST": 
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        password = request.form["password"]
        phone_num = request.form["phone_num"]
        acct_num = random.randint(0, 10000000000)
        Balance = 0
    
        user = {

            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password,
            "phone_num": phone_num,
            "acct_num":  acct_num,
            "balance": Balance

        }
        users.append(user)
        return redirect(url_for("dashboard", email=email))
    return render_template("register.html")
    
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        for user in users:
            if user["email"] == email and user["password"] == password:
                return redirect(url_for("dashboard", email=email))
        return "Invalid email or password!"
    return render_template("login.html")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if len(users) == 0:
        return "No users registered"

    user = users[0]

    if request.method == "POST":
        action = request.form["action"]
        amount = float(request.form.get("amount", 0))

        if action == "deposit":
            user["balance"] += amount

        elif action == "withdraw":
            if amount <= user["balance"]:
                user["balance"] -= amount

        elif action == "transfer":
            receiver_email = request.form["receiver_email"]
            for u in users:
                if u["email"] == receiver_email:
                    if amount <= user["balance"]:
                        user["balance"] -= amount
                        u["balance"] += amount

    return render_template("dashboard.html", user=user, users=users)
@app.route("/delete", methods=["GET", "POST"])
def delete():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        global users
        users = [u for u in users if not (u["email"] == email and u["password"] == password)]
        return redirect(url_for("index"))
    return render_template("delete.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000)

            
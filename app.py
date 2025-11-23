from flask import Flask, render_template, request, redirect, url_for, session, flash
from db import (get_donor_by_email, create_donor, add_food, get_foods_for_donor,
                get_available_foods, get_available_foods_by_location, delete_expired_foods, delete_food_by_id)
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "fallback_insecure_key")  # Load SECRET_KEY from env or fallback

@app.before_request
def before_request_func():
    delete_expired_foods()

@app.route("/")
def home():
    return redirect(url_for("user_page"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        donor = get_donor_by_email(email)
        if donor and donor['password'] == password:
            session["logged_in"] = True
            session["role"] = "donor"
            session["donor"] = {"id": donor["id"], "name": donor["name"], "email": donor["email"]}
            return redirect(url_for("donor_page"))
        else:
            flash("Invalid email or password", "danger")
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        if not (name and email and password):
            flash("Fill all fields", "warning")
        else:
            existing = get_donor_by_email(email)
            if existing:
                flash("Email already registered", "danger")
            else:
                create_donor(name, email, password)
                flash("Account created, please login", "success")
                return redirect(url_for("login"))
    return render_template("login.html")

@app.route("/donor", methods=["GET", "POST"])
def donor_page():
    if not session.get("logged_in") or session.get("role") != "donor":
        return redirect(url_for("login"))

    donor = session["donor"]

    if request.method == "POST":
        food_name = request.form.get("food_name")
        quantity = request.form.get("quantity")
        location = request.form.get("location")
        contact_phone = request.form.get("contact_phone")
        expiry_date = request.form.get("expiry_date")
        expiry_time = request.form.get("expiry_time")

        if not food_name or not location or not contact_phone or not expiry_date or not expiry_time:
            flash("Please fill all required fields", "warning")
        else:
            expiry_str = expiry_date + " " + expiry_time
            expiry_ts = datetime.strptime(expiry_str, "%Y-%m-%d %H:%M")

            add_food(
                donor_id=donor["id"],
                food_name=food_name,
                quantity=quantity,
                location=location,
                contact_phone=contact_phone,
                expiry_timestamp=expiry_ts,
            )
            flash(f"Food '{food_name}' uploaded successfully", "success")

    foods = get_foods_for_donor(donor["id"])
    return render_template("donor.html", donor=donor, foods=foods)

@app.route("/donor/delete/<int:food_id>", methods=["POST"])
def donor_delete_food(food_id):
    if not session.get("logged_in") or session.get("role") != "donor":
        flash("Please login as donor to delete food.", "danger")
        return redirect(url_for("login"))

    donor_id = session["donor"]["id"]

    success = delete_food_by_id(food_id, donor_id)
    if success:
        flash("Food deleted successfully.", "success")
    else:
        flash("Food not found or unauthorized deletion attempt.", "danger")

    return redirect(url_for("donor_page"))

@app.route("/user")
def user_page():
    search_location = request.args.get("location", "").strip()

    if search_location:
        foods = get_available_foods_by_location(search_location)
    else:
        foods = get_available_foods()

    return render_template(
        "user.html",
        foods=foods,
        search_location=search_location,
    )

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("user_page"))

if __name__ == "__main__":
    app.run(debug=True)

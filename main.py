import os

from flask import Flask, render_template, request, redirect, url_for, flash

from database import *
from password_checker import *

from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail, Message

load_dotenv()

new_user=None

app=Flask(__name__, template_folder="template")

app.secret_key=os.getenv("SECRET_KEY")

# settings for auto email sending
app.config['MAIL_SERVER']=os.getenv("MAIL_SERVER")
app.config['MAIL_PORT'] = os.getenv("MAIL_PORT")
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_API")
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER")
app.config['MAIL_USE_TLS'] = bool(os.getenv("MAIL_USE_TLS"))
app.config['MAIL_USE_SSL'] = bool(os.getenv("MAIL_USE_SSL"))

mail=Mail(app)

s=URLSafeTimedSerializer(app.secret_key)

def generation_of_verification(email):
    return s.dumps(email, salt="email-confirm")

def confirmation(token, expiration=3600):
    try:
        email=s.loads(token, salt="email-confirm", max_age=expiration)
    except:
        email=None
    return email

@app.route("/", methods=["GET"])
def home():
    return render_template("main_page.html")

@app.route("/send_name", methods=["POST", "GET"])
# GET is a request sending
# POST is an information sending
def send_name():
    global new_user
    if request.method=="GET":
        return render_template("registration.html")
    if request.method=="POST":
        email=request.form.get("email")
        username=request.form.get("username")
        password=request.form.get("password")
        password_checker=request.form.get("password_again")

        search_user=create_blind_key(username)
        search_email=create_blind_key(email)

        if password!=password_checker:
            flash("Checking password was input wrongly!")
            return redirect(url_for('send_name'))
        elif (session.query(Users).filter_by(username_index=search_user).first() or
            session.query(Users).filter_by(email_index=search_email).first()):
            flash("User with input email/username already exists!")
            return redirect(url_for('send_name'))
        elif Password.analise(password) in ["Weak password"]:
            flash("Password should have at least a capital and a small letter, number, "
                  "special symbol and 13 symbols length", "warning")
            return redirect(url_for('send_name'))

        token=generation_of_verification(email)
        verify_url=url_for('verify_email', token=token, _external=True)
        html=render_template('verify_email.html', verify_url=verify_url)
        subject="Please verify your email"

        msg=Message(subject=subject,
                    sender="hello@demomailtrap.co",
                    recipients=[email],
                    body=f"Name {username}",
                    html=html)

        mail.send(msg)

        new_user=Users(email=email, username=username, password=password)

        flash("A verification email has been sent to your email address.")

        return redirect(url_for("send_name"))

@app.route('/verify/<token>')
def verify_email(token):
    email=confirmation(token)
    if not email:
        flash("The verification link is invalid or has expired")
        return redirect(url_for("home"))
    elif email:
        flash("Registration successful")
        try:
            session.add(new_user)
            session.commit()
            session.close()
        except Exception as error:
            session.rollback()
            session.close()
            print("Some error occur", error)
        return redirect(url_for("home"))

@app.route("/sign_in", methods=["POST", "GET"])
def sign_in():
    print(request)
    if request.method=="GET":
        return render_template("sign_in.html")
    elif request.method=="POST":
        email=request.form.get("email")
        password=request.form.get("password")

        index_email=create_blind_key(email)

        try:
            user=session.query(Users).filter_by(email_index=index_email).first()
            if user and user.check_password(password):
                flash("Sign in is successful, user!")
                return redirect(url_for("home"))
        except Exception as e:
            flash("Are you sure you're registered?")
            print(e, type(e))
            return redirect(url_for("sign_in"))

if __name__ == '__main__':
    app.run(debug=True)

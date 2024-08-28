from flask import Flask, render_template, request, redirect, url_for, session, flash
from cryptocurrency import Cryptocurrency
from logreg import LogReg
from portfolio import Portfolio
import os

crypto = Cryptocurrency()
log = LogReg()
portf = Portfolio()
secret_key = os.getenv("key")

app = Flask("__name__")
app.config['SECRET_KEY'] = secret_key


def round_number(value, decimals=0):
    return round(value, decimals)


@app.context_processor
def utility_processor():
    return dict(round_number=round_number)


@app.route("/")
def home():
    data = crypto.get_data()
    username = session.get('username')
    error = session.pop("error", None)
    return render_template('home_page.html', username=username, data=data, error=error)


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    userid = log.check_data(username, password)
    if userid != 404:
        session["user_id"] = userid
        session['username'] = username
        return redirect(url_for("home"))
    else:
        login_error = 0
    return render_template("log_reg.html", error=login_error)


@app.route("/logout")
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return render_template("log_reg.html")


@app.route("/registred", methods=["POST"])
def registred():
    name = request.form.get("name")
    lastname = request.form.get("lastname")
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    return log.save_data(name, lastname, username, email, password)


@app.route("/login-register")
def log_reg():
    return render_template("log_reg.html")


@app.route('/search')
def search():
    query = request.args.get('query')
    return redirect(url_for('dynamic_page', subpath=query))


@app.route('/home/cryptocurrency/<path:subpath>')
def dynamic_page(subpath):
    try:
        return cryptocurr(subpath)
    except (KeyError, IndexError, ValueError):
        session["error"] = 0
        return redirect(url_for("home"))


@app.route("/myportfolio")
def portfolio():
    user_id = session.get("user_id")
    try:
        Portfolio().pie_chart(user_id)
        user_portfolio = portf.user_portfolio(user_id)
        if user_id == 404:
            pass
        else:
            return render_template("portfolio.html", data=user_portfolio)

    except Exception:
        return redirect(url_for("log_reg"))


@app.route("/trade", methods=["POST"])
def trade():
    userid = session.get("user_id")
    asset = request.form.get("asset")
    amount = request.form.get("amount")
    price = request.form.get("price")
    transaction_type = request.form.get("action")

    output = Portfolio().add_transaction(userid, asset, amount, price, transaction_type)
    return render_template("portfolio.html", error=output)


@app.route("/cryptocurrency/<crypto_currency>")
def cryptocurr(crypto_currency):
    data = crypto.crypto_data(crypto_currency.lower())
    crypto.chart(crypto_currency.lower())
    return render_template("graph.html", data=data[0])


@app.route("/cryptocurrency")
def cryptocurrency():
    data = crypto.get_data()
    return render_template("crypto_list.html", data=data)


if __name__ == "__main__":
    app.run(debug=True)

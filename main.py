from flask import Flask, render_template, request, redirect, url_for, session, flash
from cryptocurrency import Cryptocurrency
from log_reg import Log_reg
from portfolio import Portfolio

crypto = Cryptocurrency()
log = Log_reg()
portf = Portfolio()

app = Flask("__name__")
app.config['SECRET_KEY'] = '1999'


def round_number(value, decimals=0):
    return round(value, decimals)


@app.context_processor
def utility_processor():
    return dict(round_number=round_number)


@app.route("/")
def home():
    error = request.args.get('error', None)
    data = crypto.get_data()
    username = session.get('username')
    return render_template('home_page.html', username=username, data=data)


@app.route("/login", methods=["POST"])
def login():
    global user_id
    username = request.form.get("username")
    password = request.form.get("password")
    user_id = log.check_data(username, password)
    print(user_id)
    if user_id != 404:
        session["user_id"] = user_id
        session['username'] = username
        return redirect(url_for("home"))
    else:
        flash('Invalid username or password', 'danger')
    return render_template("log_reg.html")


@app.route("/logout")
def logout():
    global user_id
    session.pop('user_id', None)
    session.pop('username', None)
    user_id = None
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
    new_url = url_for('dynamic_page', subpath=query)
    return redirect(new_url)

@app.route('/home/cryptocurrency/<path:subpath>')
def dynamic_page(subpath):
    try:
        return cryptocurr(subpath)
    except (KeyError, IndexError, ValueError):
        error = 0
        return redirect(url_for("home", error=error))


@app.route("/myportfolio")
def portfolio():
    Portfolio().pie_chart()
    user_portfolio = portf.user_portfolio(user_id)
    return render_template("portfolio.html", data=user_portfolio)

@app.route("/trade", methods=["POST"])
def trade():
    userid = user_id
    asset = request.form.get("asset")
    amount = request.form.get("amount")
    price = request.form.get("price")
    return Portfolio().add_transaction(userid, asset, amount, price)


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
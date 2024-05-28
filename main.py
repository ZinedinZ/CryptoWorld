from flask import Flask, render_template
from cryptocurrency import Cryptocurrency


crypto = Cryptocurrency()
app = Flask("__name__")


def round_number(value, decimals=0):
    return round(value, decimals)


@app.context_processor
def utility_processor():
    return dict(round_number=round_number)


@app.route("/")
def home():
    return render_template("home_page.html")


@app.route("/myportfolio")
def portfolio():
    return "<h1>svaka cast</h1>"


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
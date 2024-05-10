from flask import Flask, render_template
from cryptocurrency import Cryptocurrency


crypto = Cryptocurrency()
app = Flask("__name__")
@app.route("/")
def home():
    return render_template("home_page.html")
@app.route("/myportfolio")
def portfolio():
    return "<h1>svaka cast</h1>"

@app.route("/cryptocurrency/<crypto_currency>")
def cryptocurr(crypto_currency):
    crypto.chart("cardano")
    return render_template("graph.html")

@app.route("/cryptocurrency")
def cryptocurrency():
    data = crypto.get_data()
    print(data)
    return render_template("crypto_list.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)
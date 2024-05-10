import matplotlib.pyplot as plt
import requests
import datetime
import plotly.graph_objs as go
import plotly.io as pio


class Cryptocurrency:
    def __init__(self):
        self.Api_key = "API_KEY"
        self.headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': "8ee55bfa-7185-405e-962d-8c23c4177921",
        }


    def get_data(self):
        url = "https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest"
        params = {
            "slug": "bitcoin,ethereum,cardano,bnb,xrp,solana,dogecoin,tron,chainlink,polygon,"
                    "avalanche,polkadot,cosmos,stellar,hedera,aptos,singularitynet"

        }
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': "8ee55bfa-7185-405e-962d-8c23c4177921",
        }
        request = requests.get(url, params=params, headers=headers)
        if request.status_code == 200:
            data = request.json()
            new_data = {}
            for id, info in data["data"].items():
                new_data[info["name"]] = {"Symbol": info["symbol"], "Max Supply": info['max_supply'],
                                          "Rank": info["cmc_rank"], "price": round(info["quote"]["USD"]["price"],2),
                                          "percent_change_24h": round(info["quote"]["USD"]["percent_change_24h"],2),
                                          "percent_change_30d": round(info["quote"]["USD"]["percent_change_30d"],2),
                                          "market cap": f"{round(info["quote"]["USD"]["market_cap"], 2):,}"}
            new_data = dict(sorted(new_data.items(), key=lambda x: x[1]["Rank"]))
            return new_data

        else:
            return "api nije pozvan"

    def chart(self, coin_name):
        url = f'https://api.coingecko.com/api/v3/coins/{coin_name}/market_chart?vs_currency=usd&days=30&interval=daily'
        api = "CG-mK38Sw5UeKe2CJq15bGX43ju"
        headers = {
            'Accepts': 'application/json',
            "x-cg-demo-api-key": "CG-mK38Sw5UeKe2CJq15bGX43ju"
        }

        response = requests.get(url, headers=headers)
        data = response.json()
        print(data)
        if data["prices"][0][1] > 1:
            price_data = [round(x[1]) for x in data["prices"]]
        else:
            price_data = [x[1] for x in data["prices"]]
        time_data = [datetime.datetime.fromtimestamp(int(x[0]) / 1000) for x in data["prices"]]
        time_data = [date.strftime("%Y-%m-%d") for date in time_data]

        trace = go.Scatter(x=time_data, y=price_data, mode="lines+markers", line=dict(color="red"))
        layout = go.Layout(width=1100, height=650,
                           title=dict(text=f"{coin_name.capitalize()} price in last 30 Days", y=0.9, x=0.5, xanchor="center",
                                      yanchor="top",
                                      font=dict(size=20, color='black', family='Arial', weight='bold')),
                           xaxis=dict(title=dict(text="Date", font=dict(weight="bold", size=20)),
                                      range=[min(time_data), datetime.datetime.today()],
                                      tickfont=dict(size=14, color='black', family='Arial', weight='bold')),
                           yaxis=dict(title=dict(text="Price", font=(dict(size=20, weight="bold"))),
                                      tickfont=dict(size=14, color='black', family='Arial', weight='bold')))

        fig = go.Figure(data=[trace], layout=layout)
        fig.write_image("static/graph.png")
        # pio.write_html(fig, file="templates/bitcoin_price.html")

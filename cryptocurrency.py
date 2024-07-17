
import requests
import datetime
import plotly.graph_objs as go


class Cryptocurrency:
    def __init__(self):
        self.Api_key = "Coingecko_Api"

    def get_data(self):
        url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc"
        headers = {
            'Accepts': 'application/json',
            "x-cg-demo-api-key": self.Api_key
        }

        request = requests.get(url, headers=headers)
        data = request.json()
        return data

    def chart(self, coin_name):
        url = f'https://api.coingecko.com/api/v3/coins/{coin_name}/market_chart?vs_currency=usd&days=30&interval=daily'
        headers = {
            'Accepts': 'application/json',
            "x-cg-demo-api-key": "CG-mK38Sw5UeKe2CJq15bGX43ju"
        }

        response = requests.get(url, headers=headers)
        data = response.json()
        # Round number if is bigger then 1
        if data["prices"][0][1] > 1:
            price_data = [round(x[1]) for x in data["prices"]]
        else:
            price_data = [x[1] for x in data["prices"]]
        # Create time data fot scatter chart
        time_data = [datetime.datetime.fromtimestamp(int(x[0]) / 1000) for x in data["prices"]]
        time_data = [date.strftime("%Y-%m-%d") for date in time_data]
        # Plot scatter chart
        trace = go.Scatter(x=time_data, y=price_data, mode="lines+markers", line=dict(color="red"))
        layout = go.Layout(width=1300, height=750,
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

    def crypto_data(self, coin):
        url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids={coin}"
        header = {"accept": "application/json",
                  "x-cg-demo-api-key": self.Api_key}
        response = requests.get(url=url, headers=header)
        data = response.json()
        del data[0]["image"]
        return data

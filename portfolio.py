import psycopg2
from cryptocurrency import Cryptocurrency
import plotly.graph_objs as go
import os

crypto = Cryptocurrency()
data = crypto.get_data()
crypto_name = [c["name"] for c in data]
db_password = os.getenv("db_password")
db_name = os.getenv("db_name")
username = os.getenv("user")


class Portfolio:
    def __init__(self):
        pass
        self.conn = psycopg2.connect(host="localhost", dbname=db_name, user=username, password=db_password, port=5432)
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS portfolio (
                                   id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY NOT NULL,
                                   user_id int NOT NULL,
                                   asset varchar(40) NOT NULL,
                                   amount decimal NOT NULL,
                                   price decimal NOT NULL,
                                   transaction_type varchar(5) NOT NULL)
            """)
        self.conn.commit()

    def add_transaction(self, user_id, asset, amount, price, transaction_type):
        # Check if asset exist in list
        if asset not in crypto_name:
            return "asset"
        elif not amount.isdigit():
            return "amount"
        elif not price.isdigit():
            return "price"
        else:
            insert_query = "INSERT INTO portfolio (user_id, asset, amount, price, transaction_type)" \
                           " Values(%s, %s, %s, %s, %s)"
            self.cur.execute(insert_query, (user_id, asset, amount, price, transaction_type))
            self.conn.commit()
            self.conn.close()
            self.conn.close()

    def user_portfolio(self, userid):
        self.cur.execute(f"SELECT asset, SUM(CASE WHEN transaction_type = 'buy' THEN amount ELSE 0 END) - \
                         SUM(CASE WHEN transaction_type = 'sell' THEN amount ELSE 0 END) \
                         FROM portfolio WHERE user_id = {userid} GROUP BY asset")
        user_data = self.cur.fetchall()

        convert_number = lambda x: int(x) if x == int(x) else float(x)
        clear_data = [(row[0], convert_number(row[1])) for row in user_data]
        new_data = []
        for item in clear_data:
            item = list(item)
            data2 = crypto.crypto_data(item[0])
            price = data2[0]["current_price"]
            item.append(round(price, 2))
            new_data.append(tuple(item))
        return new_data

    # Create pie chart for users portfolio
    def pie_chart(self, userid):
        values = self.user_portfolio(userid)
        val = [x[1] * x[2] for x in values]
        chart_data = [y[0] for y in values]
        trace = go.Pie(
            labels=chart_data,
            values=val,
            textinfo='label+percent',
            textposition='inside',
            insidetextorientation='radial'
        )
        fig = go.Figure(data=[trace])
        fig.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            legend=dict(x=-0.1, y=1)
        )
        fig.write_image("static/pie.png", width=600)


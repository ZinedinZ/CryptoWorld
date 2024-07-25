import psycopg2
from cryptocurrency import Cryptocurrency
import plotly.graph_objs as go
import pandas as pd

crypto = Cryptocurrency()
data = crypto.get_data()
crypto_name = [c["name"] for c in data]


class Portfolio():
    def __init__(self):
        pass
        self.conn = psycopg2.connect(host="localhost", dbname="Users", user="postgres", password="postgresql",
                                     port=5432)
        self.cur = self.conn.cursor()

    def add_transaction(self, user_id, asset, amount, price):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS portfolio (
                            id int PRIMARY KEY NOT NULL,
                            user_id int NOT NULL,
                            asset varchar(40) NOT NULL,
                            amount decimal NOT NULL,
                            price decimal NOT NULL)
     """)
        self.conn.commit()
        # Check if asset exist in list
        if asset not in crypto_name:
            return f"{asset} doesn't exist"
        elif not amount.isdigit():
            return "Amout number is not valid, please enter again"
        elif not price.isdigit():
            return "price number is not valid, please enter again"
        else:
            insert_query = "INSERT INTO portfolio (user_id, asset, amount, price) Values(%s, %s, %s, %s)"
            self.cur.execute(insert_query, (user_id, asset, amount, price))
            self.conn.commit()
            self.conn.close()
            self.conn.close()
            return "sve radi, malo sutra"

    def user_portfolio(self, userid):
        self.cur.execute(f"SELECT asset, amount, price FROM portfolio WHERE user_id = {userid}")
        data = self.cur.fetchall()

        convert_number = lambda x: int(x) if x == int(x) else float(x)
        clear_data = [(row[0], convert_number(row[1]), convert_number(row[2])) for row in data]
        print(clear_data)

        #  query = sql.SQL("""
        #     SELECT
        #         currency,
        #         SUM(CASE WHEN transaction_type = 'buy' THEN amount ELSE 0 END) -
        #         SUM(CASE WHEN transaction_type = 'sell' THEN amount ELSE 0 END) AS total_amount,
        #         SUM(CASE WHEN transaction_type = 'buy' THEN amount * price ELSE 0 END) /
        #         NULLIF(SUM(CASE WHEN transaction_type = 'buy' THEN amount ELSE 0 END), 0) AS avg_buy_price
        #     FROM
        #         transactions
        #     WHERE
        #         user_id = %s
        #     GROUP BY
        #         currency;
        # """)

        
        return clear_data

    # Create pie chart for users portfolio
    def pie_chart(self):
        val = [30, 20, 10, 340, 240, 104, 310, 210, 110]
        data = ["ada", "eth", "btc","aada", "etha", "batc", "asda", "esth", "bstc"]
        trace = go.Pie(
            labels=data,
            values=val,
            textinfo='label+percent',
            textposition='inside',
            insidetextorientation='radial'
        )
        fig = go.Figure(data=[trace])
        fig.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            legend=dict(x=-0.1, y=1)  # Pomjerite legendu lijevo
        )
        fig.write_image("static/pie.png", width=600)


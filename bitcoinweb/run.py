from flask import Flask, render_template, redirect
import sqlite3
from blockchain import blockexplorer
from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired

class MyForm(Form):
    name = StringField('My wallet:', validators=[DataRequired()])

wallet_key = 'thman'

app = Flask(__name__)

@app.route('/', methods=('GET', 'POST'))
def index():
    form = MyForm(csrf_enabled=False)
    if form.validate_on_submit():
        if form.name.data == wallet_key:
            return redirect('/wallet')
    conn = sqlite3.connect('../bitcoin/bitcoin.db')
    cu = conn.cursor()
    cu.execute("select * from ordertable")
    orders_list = cu.fetchall()
    cost_mean = sum([x[4] for x in orders_list])/sum([x[3] for x in orders_list])
    cu.execute("select cost from indextable where name='daysmean'")
    days_mean = cu.fetchall()[0][0]
    message_tuple = cu.execute("select price,buy from message where name='now'").fetchall()[0]
    conn.close()
    return render_template('index', form=form, days_mean=days_mean, cost_mean=cost_mean, orders_list=orders_list, message_tuple=message_tuple)

@app.route('/wallet')
def wallet():
    address = blockexplorer.get_address('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
    return render_template('wallet', address=address)

if __name__ == '__main__':
    app.debug = False
    app.run()

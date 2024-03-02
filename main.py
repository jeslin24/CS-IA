import csv
import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
from flask_bootstrap import Bootstrap
from flask import render_template
from StockSystem import StockSystem
from StockNode import StockNode
import sqlite3

app = Flask(__name__)
bootstrap = Bootstrap(app)
stockSystem = StockSystem()

# Store stock symbol and name
stock_list = []

with open('NASDAQStockList.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)

    for row in reader:
        stock_list.append(row)

stock_list.pop(0)

# Add stock to the stockSystem
for i in range(3):
    temp = stock_list[i]
    istock = StockNode(temp[1].rstrip(' Common Stock'), temp[0])
    stockSystem.addStock(istock)

@app.route('/')
def index():
    
    # Fetch stock current price from Google's stock page
    list_stock_info = []
    for i in range(3):
        istock = stockSystem.getStock(i)

        stock_code = istock.getStockCode()

        URL = f"https://www.google.com/finance/quote/{stock_code}:NASDAQ"
        page = requests.get(URL)

        soup = BeautifulSoup(page.content, "html.parser")


        price_div = soup.find_all("div", class_="YMlKec fxKbKc")
        temp = str(price_div[0])
        stock_price = float(temp[temp.find('$')+1:temp.find('<', temp.find('$'))])
        istock.setCurrentPrice(stock_price)

        last_price_div = soup.find('div', {'class': 'P6K39c'}).get_text()
        temp = str(last_price_div[0])
        last_price = float(last_price_div.lstrip('$'))
        istock.setLastPrice(last_price)


        list_stock_info.append([istock.getStockCode(), istock.getStockName()])

    # Load balance and stock inventory from database to display them
    connection = sqlite3.connect("stock.db")
    first_row = connection.execute("SELECT * FROM stock ORDER BY ROWID ASC LIMIT 1;")

    for row in first_row:
        balance = row[0]
    print(balance)
    
    stock_row = connection.execute("SELECT * FROM stock WHERE stockName IS NOT 'init'")
    stock_db = []
    inv_dict = {}

    for row in stock_row:
        stock_db.append(row[1:])
        inv_dict[row[1]] = row[4]

    stockSystem.getInventory().setDict(inv_dict)
    
    return render_template('stockpage.html', list_stocks=list_stock_info, balance=balance, stock_db=stock_db)

# This route allows JavaScript to retrieve the stock current price and last price
@app.route('/price/<stockCode>')
def stock_price(stockCode):
    stock_list = stockSystem.getStockList()

    selStock = None
    for s in stock_list:
        if s.getStockCode() == stockCode:
            selStock = s
    balance = 10000
    return {'price': selStock.getCurrentPrice(), 'lprice': selStock.getLastPrice()}

# This route interacts with buySell function in JavaScript to process user's transaction
@app.route('/buysell', methods=['POST'])
def stock_buyorsell():
    data = request.get_json()
    userAction = data['userAction']
    stockCode = data['stockCode']

    selStock = searchStock(stockSystem, stockCode)
    sprice = selStock.getCurrentPrice()
    sinv = stockSystem.getInventory()

    connection = sqlite3.connect("stock.db", timeout=60)
    cursor = connection.cursor()

    first_row = connection.execute("SELECT * FROM stock ORDER BY ROWID ASC LIMIT 1;")
    for row in first_row:
        balance = row[0]
    
    stockInInv = sinv.ifBought(selStock)
    removeFromInv = False
    if userAction == "Buy":
        balance, stock_inventory = sinv.buyStock(balance, selStock)
    elif userAction == "Sell":
        balance, stock_inventory, removeFromInv = sinv.sellStock(balance, selStock)


    if removeFromInv:
        cursor.execute("DELETE FROM stock WHERE stockCode = \'" + stockCode + "\'")
    else:
        if stockInInv:
            cursor.execute("UPDATE stock SET stockNum = " + str(sinv.getDict()[stockCode]) + " WHERE stockCode = \'" + stockCode + "\'")
        else:
            insert_list = ["0", "'" + stockCode + "'", "'"+selStock.getStockName()+"'", str(sprice), str((sinv.getDict())[stockCode])]
            cursor.execute("INSERT INTO stock (balance, stockCode, stockName, buyPrice, stockNum) VALUES (" + ", ".join(insert_list) + ")")
    cursor.execute("UPDATE stock SET balance = " + str(balance) + " WHERE stockName = 'init'")

    connection.commit() 
    connection.close()

    return jsonify(result=stock_inventory) # return the result to JavaScript 


# Sequential Search: Search for the target stock by its code in the stock list
def searchStock(stockSystem, stockCode):
    for s in stockSystem.getStockList():
        if s.getStockCode() == stockCode:
            return s

if __name__ == '__main__':
    app.debug = True
    app.run(port=8000)
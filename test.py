import requests
from bs4 import BeautifulSoup
import sqlite3

connection = sqlite3.connect("stock.db")
cursor = connection.cursor()


cursor.execute("INSERT INTO stock (balance, stockCode, stockName, buyPrice, stockNum) VALUES (0, 'testing', 'testing2', 123, 45)")

connection.commit() 
connection.close()
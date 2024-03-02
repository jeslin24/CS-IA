from StockInventory import StockInventory

class StockSystem():
    def __init__(self):
        # Store all stock nodes
        self.stockList = []
        self.inventory = StockInventory()
    
    def getStock(self, i):
        return self.stockList[i]

    def getStockList(self):
        return self.stockList

    def addStock(self, s):
        self.stockList.append(s)
    
    def removeStock(self, s):
        self.stockList.remove(s)
    
    def getInventory(self):
        return self.inventory


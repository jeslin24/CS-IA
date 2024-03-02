class StockNode():
    def __init__(self, name, code):
        self.name = name
        self.code = code
        self.currentPrice = 0
        self.lastPrice = 0
    
    def setCurrentPrice(self, cprice):
        self.currentPrice = cprice
    
    def setLastPrice(self, lprice):
        self.lastPrice = lprice

    def getStockName(self):
        return self.name
    
    def getStockCode(self):
        return self.code
    
    def getCurrentPrice(self):
        return self.currentPrice
    
    def getLastPrice(self):
        return self.lastPrice
    
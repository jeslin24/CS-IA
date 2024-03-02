class StockInventory():
    def __init__(self):
        # Dictionary: Key = stockCode, Value = number of stock hold
        self.stockDict = {}

    def buyStock(self, balance, selStock):
        scode = selStock.getStockCode()
        sprice = selStock.getCurrentPrice()
        if balance > sprice:
            balance -= sprice
            if self.ifBought(selStock):
                self.stockDict[scode] += 1
            else:
                self.stockDict[scode] = 1
        self.setBalance(balance)
        return balance, self.stockDict
    
    def sellStock(self, balance, selStock):
        removeFromInv = False
        scode = selStock.getStockCode()
        sprice = selStock.getCurrentPrice()
        if self.ifBought(selStock):
            balance += sprice
            self.stockDict[scode] -= 1
            if self.stockDict[scode] == 0:
                self.stockDict.pop(scode)
                removeFromInv = True
        self.setBalance(balance)
        return balance, self.stockDict, removeFromInv

    # Check if the selected stock is already in the inventory
    def ifBought(self, selStock):
        scode = selStock.getStockCode()
        if scode in list(self.stockDict.keys()):
            return True
        return False

    def getDict(self):
        return self.stockDict
    
    def setBalance(self, b):
        self.balance = b

    def getBalance(self):
        return self.balance

    def setDict(self, adict):
        self.stockDict = adict
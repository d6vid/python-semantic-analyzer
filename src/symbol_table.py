class SymbolTable:
    def __init__(self):
        self.table = dict()

    def add_entry(self, symbol, data):
        self.table[symbol] = data[symbol]

    def get_entry_by_symbol(self, symbol):
        return self.table.get(symbol) 
    
    def get_entry_by_function_symbol(self, symbol):
        entry = self.table.get(symbol)
        if entry is not None and entry["clasificacion"] == "function":
            return entry
        else:
            return None
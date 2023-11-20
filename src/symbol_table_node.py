from symbol_table import SymbolTable

class SymbolTableNode:
    def __init__(self, parent=None):
        self.table = SymbolTable()
        self.parent = parent
        self.children = []
    
    def add_child(self):
        new_child = SymbolTableNode(self)
        self.children.append(new_child)
        return new_child

    def get_father(self):
        return self.parent

    def get_children(self):
        return self.children

    def get_global_node(self):
        if self.parent is None:
            return self
        else:
            return self.parent.get_global_node()

    def add_entry_to_table(self, symbol, data):
        self.table.add_entry(symbol, data)

    def lookup_symbol_upwards(self, symbol):
        if self.__get_entry_by_symbol(symbol) != None:
            return self.__get_entry_by_symbol(symbol)
        elif self.parent != None and self.parent.lookup_symbol_upwards(symbol) != None:
            return self.parent.lookup_symbol_upwards(symbol)
        else:
            return None
        
    def lookup_function_symbol_upwards(self, symbol):
        if self.__get_entry_by_function_symbol(symbol) != None:
            return self.__get_entry_by_function_symbol(symbol)
        elif self.parent != None and self.parent.lookup_function_symbol_upwards(symbol) != None:
            return self.parent.lookup_function_symbol_upwards(symbol)
        else:
            return None

        
    def print_symtable(self):
        pass

    def __get_entry_by_symbol(self, symbol):
        return self.table.get_entry_by_symbol(symbol)
    
    def __get_entry_by_function_symbol(self, symbol):
        return self.table.get_entry_by_function_symbol(symbol)
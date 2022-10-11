# symbol_table.py
# Authors: Joel Figueiras (20809) & Nuno Araújo (20078)

class SymbolTable:
    def __init__(self):
        self._data = {}   # dicionario de arrays (para cada var, uma lista de valores)

    def re_set(self, key, value):
        if key in self._data:
            self._data[key].append(value)
        else:
            self[key] = value   # uses the setitem below

    # y = table["x"]
    def __getitem__(self, item):
        if item in self._data:
            return self._data[item][-1]
        else:
            raise Exception(f"Out of bounds: {item} not found")

    # table["x"] = 10
    def __setitem__(self, key, value):
        if key in self._data:
            self._data[key][-1] = value    # array existe, atualizar ultimo layer
        else:
            self._data[key] = [value]      # array nao existe, adicionar

    # del table["x"]
    def __delitem__(self, key):
        if key in self._data:    # chave existe
            if len(self._data[key]) == 1:   # so tem um valor
                del self._data[key]         # apaga completamente
            else:                       # tem mais que um valor
                self._data[key].pop()   # remove ultimo da stack
        else:
            raise Exception(f"Out of bounds: {key} not found")

    # x in table
    def __contains__(self, item):
        return item in self._data

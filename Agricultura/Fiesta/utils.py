def getPriceFormat(value):
    string = str(value)
    keys = [ string[::-1][i:i+3] for i in range(0, len(string), 3)]
    finalValue = '.'.join(keys)[::-1]
    return finalValue

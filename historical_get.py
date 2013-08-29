import urllib

base_url = "http://ichart.finance.yahoo.com/table.csv?s="
def make_url(ticker_symbol):
    return base_url + ticker_symbol

output_path = "/home/sawfish/py_stock_histori"
def make_filename(ticker_symbol, directory="TW"):
    return output_path + "/" + directory + "/" + ticker_symbol + ".csv"

def pull_historical_data(ticker_symbol, directory="TW"):
    try:
        urllib.urlretrieve(make_url(ticker_symbol), make_filename(ticker_symbol, directory))
    except urllib.ContentTooShortError as e:
        outfile = open(make_filename(ticker_symbol, directory), "w")
        outfile.write(e.content)
        outfile.close()


if __name__=='__main__':
	pull_historical_data('2330.tw')

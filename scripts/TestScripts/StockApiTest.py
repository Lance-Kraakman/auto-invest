from Classes.BusinessModel import StockApi, Quote, Bar, Trade
import time


def app():

    bitcoin_quote = Quote.LiveQuote(symbol="BTCUSD")
    bitcoin_quote.initQuoteData()

    bitcoin_bar = Bar.LiveBar(symbol="BTCUSD")
    bitcoin_bar.initBarData()

    bitcoin_trade = Trade.LiveTrade(symbol="BTCUSD")
    bitcoin_trade.initTradeData()

    # This must be called after all stock data objects have been initialized
    bitcoin_quote.startLiveDataService()


    while True:
        bitcoin_quote.updateData()
        bitcoin_bar.updateData()
        bitcoin_trade.updateData()

        if bitcoin_quote.isUpdated():
            print(bitcoin_quote.__str__())
        if bitcoin_bar.isUpdated():
            print(bitcoin_bar.__str__())
        if bitcoin_trade.isUpdated():
            print(bitcoin_trade.__str__())
        time.sleep(5)


if __name__ == "__main__":
    app()

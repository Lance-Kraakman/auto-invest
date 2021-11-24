import multiprocessing as mp, queue
from Classes.BusinessModel.StockApi import cryptoDataAPI
import json


class Account:
    """
    Class to declare a stock data object
    """

    def __init__(self, account_blocked=False, account_number=-1, accrued_fees=-1, buying_power=-1, cash=-1,
                 created_at="", crypto_status="ACTIVE", currency="USD", daytrade_count=-1, daytrading_buying_power=-1,
                 equity=-1,
                 id="", initial_margin=-1, last_equity=-1, last_maintenance_margin=-1, long_market_value=-1,
                 maintenance_margin=-1, multiplier=-1,
                 non_marginable_buying_power=-1, pattern_day_trader=False, pending_transfer_in=-1, portfolio_value=-1,
                 regt_buying_power=-1,
                 short_market_value=-1, shorting_enabled=True, sma=-1, status="ACTIVE", trade_suspended_by_user=False,
                 trading_blocked=False, transfers_blocked=False):

        self.account_blocked = account_blocked
        self.account_number = account_number
        self.accrued_fees = accrued_fees
        self.buying_power = buying_power
        self.cash = cash
        self.created_at = created_at
        self.crypto_status = crypto_status
        self.currency = currency
        self.daytrade_count = daytrade_count
        self.daytrading_buying_power = daytrading_buying_power
        self.equity = equity
        self.id = id
        self.initial_margin = initial_margin
        self.last_equity = last_equity
        self.last_maintenance_margin = last_maintenance_margin
        self.long_market_value = long_market_value
        self.maintenance_margin = maintenance_margin
        self.multiplier = multiplier
        self.non_marginable_buying_power = non_marginable_buying_power
        self.pattern_day_trader = pattern_day_trader
        self.pending_transfe_in = pending_transfer_in
        self.portfolio_value = portfolio_value
        self.regt_buying_power = regt_buying_power
        self.short_market_value = short_market_value
        self.shorting_enabled = shorting_enabled
        self.sma = sma
        self.status = status
        self.trade_suspended_by_user = trade_suspended_by_user
        self.trading_blocked = trading_blocked
        self.transfers_blocked = transfers_blocked

    def updateAccount(self, accountString):
        jsonString = self.rawAccountToJsonRaw(accountString)
        print(jsonString)
        quoteJson = json.loads(jsonString)

        self.account_blocked = quoteJson['account_blocked']
        self.account_number = quoteJson['account_number']
        self.accrued_fees = quoteJson['accrued_fees']
        self.buying_power = quoteJson['buying_power']
        self.cash = quoteJson['cash']
        self.created_at = quoteJson['created_at']
        self.crypto_status = quoteJson['crypto_status']
        self.currency = quoteJson['currency']
        self.daytrade_count = quoteJson['daytrade_count']
        self.daytrading_buying_power = quoteJson['daytrading_buying_power']
        self.equity = quoteJson['equity']
        self.id = quoteJson['id']
        self.initial_margin = quoteJson['initial_margin']
        self.last_equity = quoteJson['last_equity']
        self.last_maintenance_margin = quoteJson['last_maintenance_margin']
        self.long_market_value = quoteJson['long_market_value']
        self.maintenance_margin = quoteJson['maintenance_margin']
        self.multiplier = quoteJson['multiplier']
        self.non_marginable_buying_power = quoteJson['non_marginable_buying_power']
        self.pattern_day_trader = quoteJson['pattern_day_trader']
        self.pending_transfer_in = quoteJson['pending_transfer_in']
        self.portfolio_value = quoteJson['portfolio_value']
        self.regt_buying_power = quoteJson['regt_buying_power']
        self.short_market_value = quoteJson['short_market_value']
        self.shorting_enabled = quoteJson['shorting_enabled']
        self.sma = quoteJson['sma']
        self.status = quoteJson['status']
        self.trade_suspended_by_user = quoteJson['trade_suspended_by_user']
        self.trading_blocked = quoteJson['trading_blocked']
        self.transfers_blocked = quoteJson['transfers_blocked']

    def rawAccountToJsonRaw(self, raw_string):
        raw_string = raw_string[8:][:-1].replace("\'", "\"").replace("False", '"False"').replace("True", '"True"')
        print("RAW STRING",raw_string)
        return raw_string

    def __str__(self):
        return "----Account---- : Equity : " + self.equity.__str__() + ": cash : " + self.cash.__str__()

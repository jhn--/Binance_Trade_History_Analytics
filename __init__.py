import csv

class Binance_Trade_History_Analytics:
    def __init__(self, raw_data):
        self.data = raw_data
        self.__trades = None
        self.set_trades()

        self.__trade_days = None
        self.set_trade_days()
        
        self.__trade_overview = {}
        self.set_overview()
        
        self.__trade_details = {}
        self.set_trade_details()

    ## trades
    def set_trades(self):
        with open(self.data, newline='') as f:
            reader = csv.DictReader(f)
            self.__trades = list(reader)
    
    def get_trades(self):
        return self.__trades
    ## trades

    ## trade days
    def set_trade_days(self):
        if self.__trades:
            self.__trade_days = sorted(set([trade['Date(UTC)'].split()[0] for trade in self.__trades]))

    def get_trade_days(self):
        return self.__trade_days
    ## trade days

    ## trade details
    def set_trade_details(self):
        if self.__trade_days and self.__trades:
            for day in self.__trade_days:
                self.__trade_details[day] = {}

                self.__trade_details[day]['trades_in_date'] = [trade for trade in self.__trades if day in trade['Date(UTC)']]
                self.__trade_details[day]['num_trades_in_date'] = len(self.__trade_details[day]['trades_in_date'])
                self.__trade_details[day]['fees_in_date'] = -abs(sum([float(i['Fee']) for i in self.__trade_details[day]['trades_in_date']]))
                self.__trade_details[day]['pnl_in_date'] = sum([float(i['Realized Profit']) for i in self.__trade_details[day]['trades_in_date']])
                self.__trade_details[day]['total_pnl_per_date'] = self.__trade_details[day]['fees_in_date'] + self.__trade_details[day]['pnl_in_date']
                self.__trade_details[day]['pnl_per_trade'] = 0 if self.__trade_details[day]['num_trades_in_date'] == 0 else self.__trade_details[day]['total_pnl_per_date'] / self.__trade_details[day]['num_trades_in_date']

    def get_trade_details(self):
        return self.__trade_details
    ## trade details

    ## trade details overview
    def set_overview(self):
        if self.__trade_days and self.__trades:
            self.__trade_overview['total_trades'] = len(self.__trades)
            self.__trade_overview['total_days_traded'] = len(self.__trade_days)
            self.__trade_overview['total_fees'] = -abs(sum([float(trade['Fee']) for trade in self.__trades]))
            self.__trade_overview['total_pnl'] = sum([float(trade['Realized Profit']) for trade in self.__trades])
            self.__trade_overview['avg_pnl_fees_per_trade'] = (self.__trade_overview['total_fees'] + self.__trade_overview['total_pnl']) / len(self.__trades)
            self.__trade_overview['avg_trade_per_day'] = len(self.__trades) / len(self.__trade_days)
    
    def get_overview(self):
        header = '\t'.join(["Total Trades", "Total Days Traded", "Total Fees", "Total PnL", "Average PnL(incl fees) Per Trade", "Average Trades per Day"]).expandtabs(20)
        overview = [str(data) for data in self.__trade_overview.values()]
        overview_str = '\t'.join(overview).expandtabs(20)
        return '\n'.join([header, overview_str])

    ## trade details overview

    def __repr__(self):
        trade_all_analytics = []
        header = '\t'.join(['Date', 'Number of Trades', 'Fees', 'PnL', 'Total(Fees & PnL)', 'Average PnL per Trade (incl fees)']).expandtabs(20)
        trade_all_analytics.append(header)
        for date in self.__trade_days:
            trade_day_analytics = []
            trade_day_analytics.append(date)
            for k, v in self.__trade_details[date].items():
                if k is not 'trades_in_date':
                    trade_day_analytics.append(str(self.__trade_details[date][k]))
            trade_all_analytics.append('\t'.join(trade_day_analytics).expandtabs(20))
        return '\n'.join(trade_all_analytics)

from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
from tradingagents.argParser import parser

from google_sheet_op import *

#mine addition
import sys
import numpy as np
import pandas as pd
import yahoo_fin.stock_info as si

import os
import time
# sys.path.append("../") # go to parent dir
sys.path.insert(0, '/home/steven/lib/')


# Create a custom config
config = DEFAULT_CONFIG.copy()
config["deep_think_llm"] = "gpt-4o"  # Use a different model
config["quick_think_llm"] = "gpt-4o"  # Use a different model
config["max_debate_rounds"] = 1  # Increase debate rounds
config["online_tools"] = True  # Increase debate rounds


# Memorize mistakes and reflect
# ta.reflect_and_remember(1000) # parameter is the position returns

def do_research(qry_date, alist=['SPY'],  sheet_name="adhoc", batch=0):
    qry_date_cell="B1"
    update_google_sheet(
        json_keyfile_path='./tradingagent-467001-c50796e8bbc2.json',
        spreadsheet_id="1oam6NTvr1b-DUlNGayEP0a4Deg1o6vnKugeY49zt_OY",
        worksheet_name=f"{sheet_name}!",
        cell_range=qry_date_cell,
        values=[qry_date]
    )
    # print(list(DEFAULT_CONFIG.values()), len(DEFAULT_CONFIG))
    end_column_letter = chr(ord('A') + len(DEFAULT_CONFIG))
    CONFIG_cell = f"{'A'}2:{end_column_letter}2"
    # print(CONFIG_cell)
    update_google_sheet(
        json_keyfile_path='./tradingagent-467001-c50796e8bbc2.json',
        spreadsheet_id="1oam6NTvr1b-DUlNGayEP0a4Deg1o6vnKugeY49zt_OY",
        worksheet_name=f"{sheet_name}!",
        cell_range=CONFIG_cell,
        values=[list(DEFAULT_CONFIG.values())]
    )
    final_decisions = []
# Initialize with custom config
    # Assuming you want to update a range starting at A10,
    # and you have 5 rows and 3 columns of data to write

    start_row = 4
    start_column_letter = 'A'
    start_column_letter = chr(ord(start_column_letter) + (batch - 1)*2)
    num_rows_to_write = 0
    num_columns_to_write = 2

    start = time.perf_counter()

    ta = TradingAgentsGraph(debug=False, config=config)
    for ticker in alist:
        try:
        #   df_train, df_val, df_test = prepare_data(ticker)
          _, decision = ta.propagate(ticker, qry_date)
        except ValueError:
          print(f"{ticker} data error")
          continue
        final_decisions.append(decision)
        num_rows_to_write = num_rows_to_write + 1
    end = time.perf_counter()
    elapsed = end - start

    print("Update google sheet...")
    # Calculate the end row and column letter
    end_row = start_row + num_rows_to_write - 1
    end_column_letter = chr(ord(start_column_letter) + num_columns_to_write - 1)

    # Construct the A1 notation
    range_to_update = f"{start_column_letter}{start_row}:{end_column_letter}{end_row}"
    # print(range_to_update)
    # print(alist, final_decisions)
    update_google_sheet(
        json_keyfile_path='./tradingagent-467001-c50796e8bbc2.json',
        spreadsheet_id="1oam6NTvr1b-DUlNGayEP0a4Deg1o6vnKugeY49zt_OY",
        worksheet_name=f"{sheet_name}!",
        cell_range=range_to_update,
        values=[alist, final_decisions],
        range_body="COLUMNS",
        batch = batch
    )

    qry_date_cell="C1:F1"
    hours, remainder = divmod(elapsed.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)    
    update_google_sheet(
        json_keyfile_path='./tradingagent-467001-c50796e8bbc2.json',
        spreadsheet_id="1oam6NTvr1b-DUlNGayEP0a4Deg1o6vnKugeY49zt_OY",
        worksheet_name=f"{sheet_name}!",
        cell_range=qry_date_cell,
        values=[['COUNT:', str(int(num_columns_to_write)), 'RUNTIME:', f"Duration (HH:MM): {int(hours):02}:{int(minutes):02}"]]
    )

#earning bet
core = ["TSLA", "GOOG", "NVDA","MRNA","AAPL","COST","MSTR","COIN"]
energy = ["CF", "EQT","OXY","SEDG","OIH"]
semi = ["QCOM","LRCX","ASML","AMD","SOXL","TSM"]
index = ["SPY","QQQ","SQQQ"]
fin = ["MS","UNH","JPM","GS"]
hot = ["SHOP","FSLY","U","ZM","NFLX","PYPL"]
btc = ["BTC-USD","ETH-USD"]
software = ["GOOG","MSFT"]
base = ["HD","ROOT","U","PFE","UNH","DHI"]
bio = ["HIMS","TEM"]
cloud = ["NOW","DDOG","DASH","NOW"]
random = ["MU","DOG","SE","APP"]
tickers =  core + energy + semi + index
#fin + hot + btc + software + bio + base + cloud + random

def main():
    args = parser.parse_args()
    ticker = args.symbol
    qry_date = args.date
    batch = args.batch

    # global datadir

    update_google_sheet(
        json_keyfile_path='./tradingagent-467001-c50796e8bbc2.json',
        spreadsheet_id="1oam6NTvr1b-DUlNGayEP0a4Deg1o6vnKugeY49zt_OY",
        worksheet_name="adhoc!",
        cell_range="A1:B1",
        values=[["Update_Date:", str(qry_date)]]
    )

    sgroups = {"sp500":np.array(pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")[0]["Symbol"]),
        "qqq": si.tickers_dow(),
        "custom": tickers,
        "index": index,
        "semi": semi,
        "btc": btc,
        "test": ['tsla','coin','nvda']}
    
    # Initialize with custom config
    
    print(args.date)
    if args.list == 'all':
        print("analyze all list...\n")
        for l in sgroups:
            do_research(qry_date, l )
    if args.list == 'sp500':
        print("analyze sp500...\n")
        do_research(qry_date, sgroups['sp500'], sheet_name='spy')
    elif args.list == 'qqq':
        print("analyze qqq...\n")
        do_research(qry_date, sgroups['qqq'], sheet_name='qqq')
    elif args.list == 'custom':
        print("analyze custom...\n")
        do_research(qry_date, sgroups['custom'], sheet_name='adhoc')
    else:
        print("analyze test...\n")
        do_research(qry_date, sgroups['test'], sheet_name='adhoc')

if __name__ == '__main__':
    main()
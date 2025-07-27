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
from datetime import datetime
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

def do_research(TA, qry_date, alist=['SPY'],  sheet_name="adhoc", batch=0):
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

    start_row = 5
    start_column_letter = 'A'
    start_column_letter = chr(ord(start_column_letter) + (batch - 1)*2)
    num_rows_to_write = 0
    num_columns_to_write = 2

    start = datetime.now()

    for ticker in alist:
        try:
        #   df_train, df_val, df_test = prepare_data(ticker)
          _, decision = TA.propagate(ticker, qry_date)
        except ValueError:
          print(f"{ticker} data error")
          continue
        final_decisions.append(decision)
        num_rows_to_write = num_rows_to_write + 1
    end = datetime.now()
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
        range_body="COLUMNS"
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
core = ["TSLA", "GOOG", "NVDA","UNH","BLK","COST","MSTR","COIN"]
energy = ["CF", "EQT","OXY","SEDG","OIH"]
semi = ["QCOM","LRCX","ASML","AMD","SOXL","TSM"]
index = ["SPY","QQQ","SQQQ"]
fin = ["MS","JPM","GS","BLK","BX"]
hot = ["SHOP","FSLY","U","ZM","NFLX","PYPL"]
btc = ["BTC-USD","ETH-USD"]
software = ["GOOG","MSFT","META","AMZN"]
base = ["HD","ROOT","U","PFE","UNH","DHI"]
bio = ["HIMS","TEM"]
cloud = ["NOW","DDOG","DASH","NOW"]
random = ["MU","DOG","SE","APP","UPST"]

tickers =  core
#  + energy + semi + index
#fin + hot + btc + software + bio + base + cloud + random

def main():
    args = parser.parse_args()
    ticker = args.symbol
    qry_date = args.date
    batch = args.batch
    sheetname = args.sheetname

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
        "test": ['tsla']}
    groups = {
        # "core", 
        # "energy", 
        # "semi", 
        "index",
        "fin", 
        # "hot", 
        # "btc",
        # "software", 
        # "base",
        # "bio",
        # "cloud", 
        # "random"
        }
    
    # Initialize with custom config
    
    print(args.date)
    ta = TradingAgentsGraph(debug=False, config=config)

    # if args.list == 'all':
    #     print("analyze all list...\n")
    #     batch = 1
    #     for l in sgroups:
    #         do_research(Alist=l , batch=batch, sheet_name=l, TA=ta, qry_date=qry_date)
    #         batch = batch + 1
    if args.list == 'focus':
        print("analyze the list of my trading...\n")

        for l in groups:
            start_row = 3
            start_column_letter = 'A'
            start_column_letter = chr(ord(start_column_letter) + (batch - 1)*2)
            num_rows_to_write = 2
            num_columns_to_write = 2
            end_column_letter = chr(ord(start_column_letter) + num_columns_to_write - 1)
            end_row = start_row + num_rows_to_write - 1

            range_to_update = f"{start_column_letter}{start_row}:{end_column_letter}{end_row}"
            update_google_sheet(
                json_keyfile_path='./tradingagent-467001-c50796e8bbc2.json',
                spreadsheet_id="1oam6NTvr1b-DUlNGayEP0a4Deg1o6vnKugeY49zt_OY",
                worksheet_name=sheetname,
                cell_range=range_to_update,
                values=[[l,''],['ticker','decision']]
            )            
            do_research( alist=sgroups[l] , sheet_name=sheetname, batch=batch, TA=ta, qry_date=qry_date)
            batch = batch + 1            
    elif args.list == 'sp500':
        print("analyze sp500...\n")
        do_research(alist=sgroups['sp500'], sheet_name='spy', batch=batch,TA=ta, qry_date=qry_date)
    elif args.list == 'qqq':
        print("analyze qqq...\n")
        do_research( alist=sgroups['qqq'], sheet_name='qqq', batch=batch,TA=ta, qry_date=qry_date)
    elif args.list == 'custom':
        print("analyze custom...\n")
        start_row = 3
        start_column_letter = 'A'
        start_column_letter = chr(ord(start_column_letter) + (batch - 1)*2)
        num_rows_to_write = 2
        num_columns_to_write = 2
        end_column_letter = chr(ord(start_column_letter) + num_columns_to_write - 1)
        end_row = start_row + num_rows_to_write - 1

        range_to_update = f"{start_column_letter}{start_row}:{end_column_letter}{end_row}"
        update_google_sheet(
            json_keyfile_path='./tradingagent-467001-c50796e8bbc2.json',
            spreadsheet_id="1oam6NTvr1b-DUlNGayEP0a4Deg1o6vnKugeY49zt_OY",
            worksheet_name=sheetname,
            cell_range=range_to_update,
            values=[['custom',''],['ticker','decision']]
        )         
        do_research(alist=sgroups['custom'], sheet_name=sheetname, batch=batch, TA=ta, qry_date=qry_date)
    else:
        print("analyze test...\n")
        start_row = 3
        start_column_letter = 'A'
        start_column_letter = chr(ord(start_column_letter) + (batch - 1)*2)
        num_rows_to_write = 2
        num_columns_to_write = 2
        end_column_letter = chr(ord(start_column_letter) + num_columns_to_write - 1)
        end_row = start_row + num_rows_to_write - 1

        range_to_update = f"{start_column_letter}{start_row}:{end_column_letter}{end_row}"
        update_google_sheet(
            json_keyfile_path='./tradingagent-467001-c50796e8bbc2.json',
            spreadsheet_id="1oam6NTvr1b-DUlNGayEP0a4Deg1o6vnKugeY49zt_OY",
            worksheet_name=f"adhoc!",
            cell_range=range_to_update,
            values=[['test',''],['ticker','decision']]
        )

        do_research(alist=sgroups['test'], sheet_name=sheetname, batch=batch,TA=ta, qry_date=qry_date)

if __name__ == '__main__':
    main()
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.argParser import parser

from google_sheet_op import *

#mine addition
import sys
import numpy as np
import pandas as pd
import yahoo_fin.stock_info as si

import os
from datetime import datetime
import csv
# sys.path.append("../") # go to parent dir
sys.path.insert(0, '/home/steven/lib/')

# Memorize mistakes and reflect
# ta.reflect_and_remember(1000) # parameter is the position returns
core = ["COIN", "TSLA", "MSTR","UNH","COST","GOOG", "NVDA","META"]
energy = ["GUSH", "CF", "EQT","OXY","SEDG","VST","CEG","LEU"]
semi = ["QCOM","LRCX","ASML","AMD","SOXL","TSM","SMCI","AVGO","MRVL"]
index = ["SPY","QQQ","TQQQ", "SQQQ","IWM"]
fin = ["BLK","BX","TLT","JPM","GS","CRCL","HOOD","SOFI","FUTU"]
hot = ["SHOP","CRCL","U","UPST"]
btc = ["BTC-USD","MSTR","ETH-USD"]
software = ["MSFT","PLTR"]
base = ["HD","KO","MCD","PFE"]
bio = ["XBI","TMDX","HIMS","TEM"]
cloud = ["OKTA","DDOG","DASH","NOW","CRWV"]
robot=["SERV"]
dron=["AVAV","ONDS","RCAT","UNMC"]
ai=["APP","BBAI","FIG"]
neuk=["SMR","LTBR","OKLO","NNE"]
quantum = ["ionq","rgti","qbts"]

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
        "core": core,
        "fin": fin,
        "semi": semi,
        "energy": energy,
        "bio": bio,
        "neuk": neuk,
        "ai": ai,
        "dron":dron,
        "quantum":quantum,
        "software": software,
        "hot": hot,
        "cloud": cloud,
        "base": base,
        "btc": btc,
        "benchmark": ['spy','msft','tsla']}
    groups = {
        "core", 
        "energy", 
        "semi", 
        "index",
        "fin", 
        "hot", 
        "btc",
        "software", 
        "base",
        "bio",
        "dron",
        "ai",
        "neuk",
        "quantum",
        "cloud"
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
    start = datetime.now()
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
            # print(sheetname, l, range_to_update)
            update_google_sheet(
                json_keyfile_path='./tradingagent-467001-c50796e8bbc2.json',
                spreadsheet_id="1oam6NTvr1b-DUlNGayEP0a4Deg1o6vnKugeY49zt_OY",
                worksheet_name=f"{sheetname}!",
                cell_range=range_to_update,
                values=[[l,''],['ticker','decision']]
            )            
            print(f"{l} group...")
            do_research( alist=sgroups[l] , sheet_name=sheetname, batch=batch, TA=ta, qry_date=qry_date)
            batch = batch + 1            
    elif args.list == 'preprocess':
        print(f"preprocess training data with the model {args.llmprovider, args.llmdeep, args.llmquick}...\n")
        start_date = args.startdate
        end_date = args.enddate
        config["llm_provider"]=args.llmprovider
        config["deep_think_llm"]=args.llmdeep
        config["quick_think_llm"]=args.llmquick
        results = dict()
        for single_date in daterange(start_date, end_date):
            groupdata = dict()
            print(f"{single_date}...")
            item = dict()
            for l in groups:
                print(f"    {l} group...")
                decisions = preprocess(alist=sgroups[l], TA=ta, qry_date=single_date)
                # groupdata.append(f"{l}:{sgroups[l], decisions}")
                item["tickers"] = sgroups[l]
                item["decision"] = decisions
                groupdata[l] = item
            results[str(single_date)] = groupdata
        df = pd.DataFrame(results)

        #write to the file
        trainingfile = preprocess_data_location(
            startdate=str(start_date), 
            enddate=str(end_date))
        print(trainingfile)

        df.to_json(trainingfile, index=False)        
        end = datetime.now()
        elapsed = end - start
        qry_date_cell="C1:F1"
        hours, remainder = divmod(elapsed.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)    
        print(f"Processing time {int(hours):02}:{int(minutes):02}")

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
            worksheet_name=f"{sheetname}!",
            cell_range=range_to_update,
            values=[['custom',''],['ticker','decision']]
        )        
        do_research(alist=sgroups['custom'], sheet_name=sheetname, batch=batch, TA=ta, qry_date=qry_date)
    else:
        print("analyze index...\n")
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
            worksheet_name=f"{sheetname}!",
            cell_range=range_to_update,
            values=[['index',''],['ticker','decision']]
        )

        do_research(alist=sgroups['index'], sheet_name=sheetname, batch=batch,TA=ta, qry_date=qry_date)
    if (not args.list == 'preprocess'):
        end = datetime.now()
        elapsed = end - start
        qry_date_cell="C1:F1"
        hours, remainder = divmod(elapsed.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)    
        update_google_sheet(
            json_keyfile_path='./tradingagent-467001-c50796e8bbc2.json',
            spreadsheet_id="1oam6NTvr1b-DUlNGayEP0a4Deg1o6vnKugeY49zt_OY",
            worksheet_name=f"{sheetname}!",
            cell_range=qry_date_cell,
            values=[['COUNT:', str(int(num_columns_to_write)), 'RUNTIME(HH:MM):', f"{int(hours):02}:{int(minutes):02}"]]
        )
if __name__ == '__main__':
    main()
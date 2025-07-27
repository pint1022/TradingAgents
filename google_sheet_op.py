# google sheet handler
# import sys
# sys.path.append('/home/steven/dev/TradingAgents/')
from tradingagents.default_config import DEFAULT_CONFIG

import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from datetime import date, timedelta
import os
# Create a custom config
config = DEFAULT_CONFIG.copy()
config["deep_think_llm"] = "gpt-4o"  # Use a different model
config["quick_think_llm"] = "gpt-4o"  # Use a different model
config["max_debate_rounds"] = 1  # Increase debate rounds
config["online_tools"] = True  # Increase debate rounds

#earning bet
core = ["TSLA", "GOOG", "NVDA","UNH","BLK","COST","MSTR","NFLX","COIN"]
energy = ["CF", "EQT","OXY","SEDG","OIH"]
neuk=["oklo", "smr","ltbr","nne"]
ai=["pltr","bbai","soun","rddt","duol"]
dron=["achr", "joby","avav","onds"]
quantum=["ionq","qbts"]
semi = ["QCOM","LRCX","ASML","AMD","SOXL","TSM"]
index = ["SPY","QQQ","SQQQ"]
fin = ["MS","GS","JPM","BLK","BX"]
hot = ["SHOP","RR","U","ZM","PYPL"]
btc = ["BTC-USD","ETH-USD"]
software = ["GOOG","MSFT","META","AMZN"]
base = ["HD","ROOT","U","PFE","DHI"]
bio = ["HIMS","TEM"]
cloud = ["NOW","DDOG","DASH","NOW"]
random = ["MU","DOG","SE","APP","UPST"]

tickers =  core
#  + energy + semi + index
#fin + hot + btc + software + bio + base + cloud + random


def preprocess_data_location(startdate, enddate):
    csv_file = f'{config["deep_think_llm"]}_{config["quick_think_llm"]}_period_{startdate}_{enddate}.json'
    if not os.path.exists(config["data_dir"]):
        os.mkdir(config["data_dir"])
    if not os.path.exists(config["training_dir"]):
        os.mkdir(config["training_dir"])
    csv_folder = f'{os.path.join(config["training_dir"], config["llm_provider"])}'
    if not os.path.exists(csv_folder):
        os.mkdir(csv_folder)
    full_path =os.path.join(csv_folder, csv_file)
    if os.path.exists(full_path):
        return "stop"
    else:
      return full_path

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
        values=[list(config.values())]
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

    for ticker in alist:
        try:
        #   df_train, df_val, df_test = prepare_data(ticker)
          _, decision = TA.propagate(ticker, qry_date)
        except ValueError:
          print(f"{ticker} data error")
          continue
        final_decisions.append(decision)
        num_rows_to_write = num_rows_to_write + 1


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

def read_google_sheet(json_keyfile_path, spreadsheet_id, worksheet_name, cell_range, range_body='ROWS'):
        creds = Credentials.from_service_account_file(json_keyfile_path)
        # client = gspread.authorize(creds)
        # print(client.openall())

        # The ID and range of a sample spreadsheet.
        # SAMPLE_RANGE_NAME = "trade!A2:E5"
        value_range_body = { 'majorDimension':  range_body        }

        service = build("sheets", "v4", credentials=creds)
        returns = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=worksheet_name + cell_range
        ).execute()

        data = returns.get('values',[])
        # Print the data
        for row in data:
            print(row)

def update_google_sheet(json_keyfile_path, spreadsheet_id, worksheet_name, cell_range, values, range_body= 'ROWS'):
    """
    Updates a range of cells in a Google Sheet.

    Args:
        json_keyfile_path (str): Path to the service account JSON key file.
        spreadsheet_name (str): Name of the spreadsheet.
        worksheet_name (str): Name of the specific worksheet (tab).
        cell_range (str): A1 notation for the range (e.g., "A1:B2").
        values (list of lists): 2D list of values to insert.

    Returns:
        str: Success message or error message.
    """
    try:
        creds = Credentials.from_service_account_file(json_keyfile_path)
        # client = gspread.authorize(creds)
        # print(client.openall())

        # The ID and range of a sample spreadsheet.
        # SAMPLE_RANGE_NAME = "trade!A2:E5"
        value_range_body = {
            'majorDimension': range_body,
            'values': values
        }

        service = build("sheets", "v4", credentials=creds)
        service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            valueInputOption='USER_ENTERED',
            range=worksheet_name + cell_range,
            body=value_range_body
        ).execute()

        # sheet = client.open(spreadsheet_name).worksheet(worksheet_name)
        # sheet.update(cell_range, values)
        return "Sheet updated successfully."
    except Exception as e:
        return f"Failed to update sheet: {e}"

def preprocess(TA, qry_date, alist=['SPY']):
    final_decisions = []
# Initialize with custom config
    # Assuming you want to update a range starting at A10,
    # and you have 5 rows and 3 columns of data to write

    for ticker in alist:
        try:
        #   df_train, df_val, df_test = prepare_data(ticker)
          _, decision = TA.propagate(ticker, qry_date)
        except ValueError:
          print(f"{ticker} data error")
          continue
        final_decisions.append(decision)
    return final_decisions

def daterange(start_date: date, end_date: date):
    days = int((end_date - start_date).days)
    for n in range(days):
        yield start_date + timedelta(n)

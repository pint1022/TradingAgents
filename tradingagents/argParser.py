import argparse
from datetime import datetime, date

def valid_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        msg = f"Not a valid date: '{s}'. Expected format: YYYY-MM-DD."
        raise argparse.ArgumentTypeError(msg)

# def mkdate(datestr):
#     return datetime.strptime(datestr, '%Y-%m-%d')
# parser.add_argument('--date', '-dt', metavar='DATE', type=mkdate, default=datetime.now(),
#                     help='which date is to retrieve')  

parser = argparse.ArgumentParser()

parser.add_argument('--symbol', type=str, default='tsla',
                    help='a ticker to analyze(default: tsla)')
parser.add_argument("--date", type=valid_date, default=date.today(), 
                    help="Date in YYYY-MM-DD format")      
parser.add_argument('--list', '-l', metavar='LIST', default='test',
                        help='list of stock groups: sp500, dow or all')
parser.add_argument('--batch', type=int, default=1, choices=range(1, 11),
                    help='start column (default: 1)')
parser.add_argument('--sheetname', type=str, default='adhoc',
                    help='the sheet to store the data')
parser.add_argument('--llmprovider', type=str, default='openai',
                    help='the model provider')
parser.add_argument('--llmdeep', type=str, default='gpt-4.1-mini',
                    help='the model used in deep think')
parser.add_argument('--llmquick', type=str, default='gpt-4.1-mini',
                    help='the model used in quick think')
parser.add_argument("--startdate", type=valid_date, default=date.today(), 
                    help="Date in YYYY-MM-DD format") 
parser.add_argument("--enddate", type=valid_date, default=date.today(), 
                    help="Date in YYYY-MM-DD format") 

                        
import argparse
from datetime import datetime, date

def valid_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        msg = f"Not a valid date: '{s}'. Expected format: YYYY-MM-DD."
        raise argparse.ArgumentTypeError(msg)
    
parser = argparse.ArgumentParser()

parser.add_argument('--symbol', type=str, default='tsla',
                    help='a ticker to analyze(default: tsla)')
parser.add_argument("--date", type=valid_date, default=date.today(), 
                    help="Date in YYYY-MM-DD format")

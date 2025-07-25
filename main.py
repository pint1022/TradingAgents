from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
from tradingagents.argParser import parser

# Create a custom config
config = DEFAULT_CONFIG.copy()
config["deep_think_llm"] = "gpt-4o"  # Use a different model
config["quick_think_llm"] = "gpt-4o"  # Use a different model
config["max_debate_rounds"] = 1  # Increase debate rounds
config["online_tools"] = True  # Increase debate rounds

# Initialize with custom config
ta = TradingAgentsGraph(debug=True, config=config)

# forward propagate
args = parser.parse_args()
ticker = args.symbol
qry_date = args.date
_, decision = ta.propagate(ticker, qry_date)
print(decision)
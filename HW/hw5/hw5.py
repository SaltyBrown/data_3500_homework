
import json

# Try to import yfinance for automatic data download
try:
    import yfinance as yf
    HAS_YFINANCE = True
except ImportError:
    HAS_YFINANCE = False
    print("Note: yfinance not found. Install with: pip install yfinance")
    print("      Or manually place <TICKER>.txt files in this folder.\n")

# The 10 stock tickers
tickers = ["AAPL", "GOOG", "ADBE", "TSLA", "MSFT", "AMZN", "META", "NVDA", "JPM", "V"]


def downloadStockData():
    """
    Download 1 year of closing prices for all tickers using yfinance
    and save each as a <TICKER>.txt file with one price per line.
    """
    if not HAS_YFINANCE:
        print("Skipping download — yfinance not available.")
        return

    for ticker in tickers:
        print(f"Downloading {ticker}...")
        stock = yf.download(ticker, period="1y", progress=False)

        # Extract Close prices — yfinance already returns oldest-first
        prices = [round(float(p), 2) for p in stock["Close"].squeeze()]

        # Write one price per line to <TICKER>.txt
        with open(f"{ticker}.txt", "w") as f:
            for price in prices:
                f.write(f"{price}\n")

        print(f"  Saved {len(prices)} prices to {ticker}.txt")


def loadPrices(ticker):
    """
    Load stock closing prices from a <TICKER>.txt file.
    Returns a list of floats rounded to 2 decimal places.
    """
    file = open(f"{ticker}.txt")
    lines = file.readlines()
    prices = [round(float(line), 2) for line in lines]
    return prices


def meanReversionStrategy(prices):
    """
    Prints each buy, sell, and trade profit.
    Returns: (total_profit, percent_return)
    """
    holding = False    # Whether we currently own the stock
    buy_price = 0      # Price we paid when we last bought
    total_profit = 0   # Running total of completed trade profits
    first_buy = None   # First buy price, used to calculate % return

    # Start at index 4 so we always have a full 5-day window
    for i in range(4, len(prices)):
        avg = sum(prices[i - 4:i + 1]) / 5   # 5-day moving average
        price = prices[i]

        # Buy signal: price dropped below 98% of the moving average
        if not holding and price < avg * 0.98:
            buy_price = price
            holding = True
            if first_buy is None:
                first_buy = buy_price
            print(f"buying at: {round(price, 2)}")

        # Sell signal: price rose above 102% of the moving average
        elif holding and price > avg * 1.02:
            trade_profit = price - buy_price
            total_profit += trade_profit
            holding = False
            print(f"selling at: {round(price, 2)}")
            print(f"trade profit: {round(trade_profit, 2)}")

    # Summary output
    total_profit_rounded = round(total_profit, 2)
    returns_pct = round((total_profit / first_buy) * 100, 2) if first_buy else 0.0

    print("-----------------------")
    print(f"Total profit: {total_profit_rounded}")
    print(f"First buy: {first_buy}")
    print(f"Percent return: {returns_pct}%")

    return total_profit, returns_pct


def simpleMovingAverageStrategy(prices):
    """
    Prints each buy, sell, and trade profit.
    Returns: (total_profit, percent_return)
    """
    holding = False    # Whether we currently own the stock
    buy_price = 0      # Price we paid when we last bought
    total_profit = 0   # Running total of completed trade profits
    first_buy = None   # First buy price, used to calculate % return

    # Start at index 4 so we always have a full 5-day window
    for i in range(4, len(prices)):
        avg = sum(prices[i - 4:i + 1]) / 5   # 5-day moving average
        price = prices[i]

        # Buy signal: price crossed above the moving average
        if not holding and price > avg:
            buy_price = price
            holding = True
            if first_buy is None:
                first_buy = buy_price
            print(f"buying at: {round(price, 2)}")

        # Sell signal: price crossed below the moving average
        elif holding and price < avg:
            trade_profit = price - buy_price
            total_profit += trade_profit
            holding = False
            print(f"selling at: {round(price, 2)}")
            print(f"trade profit: {round(trade_profit, 2)}")

    # Summary output
    total_profit_rounded = round(total_profit, 2)
    returns_pct = round((total_profit / first_buy) * 100, 2) if first_buy else 0.0

    print("-----------------------")
    print(f"Total profit: {total_profit_rounded}")
    print(f"First buy: {first_buy}")
    print(f"Percent return: {returns_pct}%")

    return total_profit, returns_pct


def saveResults(results):
    """
    Save the results dictionary to a JSON file called results.json.
    """
    with open("results.json", "w") as f:
        json.dump(results, f, indent=4)
    print("\nResults saved to results.json")


# ── Main Program ─────────────────────────────────────────────────────────────

# Step 1: Download 1 year of stock data and save to .txt files
downloadStockData()

# Step 2: Create results dictionary to store prices, profits, and return %
results = {}

# Step 3: Loop through all 10 tickers and run both strategies
for ticker in tickers:

    # Load closing prices from the ticker's .txt file
    prices = loadPrices(ticker)

    # Store price list in results dictionary
    results[f"{ticker}_prices"] = prices

    # Run Simple Moving Average strategy and store results
    print(f"\n{ticker} Simple Moving Average Strategy Output:")
    sma_profit, sma_returns = simpleMovingAverageStrategy(prices)
    results[f"{ticker}_sma_profit"] = sma_profit
    results[f"{ticker}_sma_returns"] = sma_returns

    # Run Mean Reversion strategy and store results
    print(f"\n{ticker} Mean Reversion Strategy Output:")
    mr_profit, mr_returns = meanReversionStrategy(prices)
    results[f"{ticker}_mr_profit"] = mr_profit
    results[f"{ticker}_mr_returns"] = mr_returns

# Step 4: Save all results to results.json (outside the loop)
saveResults(results)

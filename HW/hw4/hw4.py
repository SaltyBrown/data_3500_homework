# Open the TSLA price data file (one closing price per line,
# oldest date first, dollar sign already removed)
# Use __file__ so the path works regardless of where the script is run from
import os
file = open(os.path.join(os.path.dirname(__file__), "TSLA.txt"))
lines = file.readlines()
file.close()

# Read every line into a list as a rounded float
prices = []
for line in lines:
    price = float(line)
    price = round(price, 2)
    prices.append(price)


buy_price   = 0       # price at which we most recently bought
first_buy   = 0       # price of the very first purchase (for % return calc)
total_profit = 0.0    # running total of profits across all trades
holding     = False   # True when we currently own a share

print("TSLA Mean Reversion Strategy Output: 2025 - 2026 Data")
print()


# We need at least 5 previous days to calculate the moving average,
# so we start at index 5 (the 6th price in the list).
for i in range(5, len(prices)):
    current_price = prices[i]

    # 5-day moving average: average of the 5 days immediately before today
    avg_price = round(sum(prices[i - 5 : i]) / 5, 2)

    if current_price < avg_price * 0.98:
        # Price dropped more than 2% below average -- BUY signal
        # Only buy if we are not already holding a position
        if not holding:
            buy_price = current_price
            holding   = True

            # Record the very first buy for the final % return calculation
            if first_buy == 0:
                first_buy = buy_price

            print(f"buying at:       {buy_price}")

    elif current_price > avg_price * 1.02:
        # Price rose more than 2% above average -- SELL signal
        # Only sell if we are currently holding a position
        if holding:
            trade_profit  = round(current_price - buy_price, 2)
            total_profit  = round(total_profit + trade_profit, 2)
            holding       = False

            print(f"    selling at:      {current_price}")
            print(f"    trade profit:    {trade_profit}")
            print()

    else:
        # Price is within the normal band -- hold, do nothing
        pass


# Percentage return relative to what we first paid
final_profit_pct = round((total_profit / first_buy) * 100, 2)

print("-----------------------")
print(f"Total profit:    {total_profit}")
print(f"First buy:       {first_buy}")
print(f"% return:        {final_profit_pct}%")

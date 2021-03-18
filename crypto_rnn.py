# pip install pandas
import pandas as pd
import os

# last 60 minutes of price data to predict, how long of a preceeding sequence to collect for RNN
SEQ_LEN = 60

# how far into the future are we trying to predict
# period is 1 minute, here we set it to 3 minutes
FUTURE_PERIOD_PREDICT = 3

RATIO_TO_PREDICT = "LTC-USD"


def classify(current, future):
    if float(future) > float(current):
        return 1
    else:
        return 0


main_df = pd.DataFrame()

ratios = ["BTC-USD", "LTC-USD", "ETH-USD", "BCH-USD"]

for ratio in ratios:
    dataset = f"crypto_data/{ratio}.csv"

    df = pd.read_csv(
        dataset, names=["time", "low", "high", "open", "close", "volume"])
    # print(df.head())
    # inplace=True -> so that we do not have to redefine dataframe everytime
    df.rename(columns={"close": f"{ratio}_close",
              "volume": f"{ratio}_volume"}, inplace=True)
    df.set_index("time", inplace=True)
    df = df[[f"{ratio}_close", f"{ratio}_close"]]

    # print(df.head())

    # merge all columns
    if len(main_df) == 0:  # if main_df is empty
        main_df = df
    else:
        main_df = main_df.join(df)


main_df['future'] = main_df[f'{RATIO_TO_PREDICT}_close'].shift(
    -FUTURE_PERIOD_PREDICT)

main_df['target'] = list(
    map(classify, main_df[f"{RATIO_TO_PREDICT}_close"], main_df["future"]))

print(main_df[[f"{RATIO_TO_PREDICT}_close", "future", "target"]].head())

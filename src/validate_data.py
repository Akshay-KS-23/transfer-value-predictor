#import pandas to load and examine the player valuation dataset
import pandas as pd

#import Path to locate the dataset relative to the project root
from pathlib import Path

market_value_path = Path(
    "data/raw/global_transfer_market/player_market_values.csv"
)

transfer_path = Path(
    "data/raw/global_transfer_market/transfers_history.csv"
)

#load both csv into dataframes
market_value = pd.read_csv(market_value_path)
transfer = pd.read_csv(transfer_path)

#display a sample of player valuation for manual authenticity checks
print("PLAYER MARKET VALUE SAMPLE")
print(market_value.sample(min(10, len(market_value)),random_state=42).to_string(index=False))

#show the years and numbers of records available for each year.
print("\nVALUATION PER YEAR")
print(market_value.groupby("year").size().to_string())

#show the most frequent player names to spot suspicious repetitions
print("\nMOST FREQUENT VALUATION NAMES")
print(market_value["player_name"].value_counts().head(5).to_string())

#display a sample of transfer records for authenticity checks
print("\nTRANSFER HISTORY SAMPLE")
print(transfer.sample(min(10, len(transfer)), random_state=42).to_string(index=False))

#summarize the available transfer-fee values
print("\nTRASNFER FEE SUMMARY")
print(transfer["fee_eur_m"].describe().to_string())

#check how many transfer records are explicitly marked as free transfers
print("\nFREE TRANSFER COUNTS")
print(transfer["is_free_transfer"].value_counts(dropna=False).to_string())
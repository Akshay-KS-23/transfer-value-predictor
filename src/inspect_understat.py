#import pandas to load and analyse the player stats
import pandas as pd
#import path to locate the dataset from the project root
from pathlib import Path

#define the location of the downloaded Understat dataset
file_path = Path("data/raw/understat/understat_players_2014_2024.csv")

#load the csv file into pandas dataframe
df = pd.read_csv(file_path)

#display the dataset dimensions : number of rows n cols
print("\nDataset Shape")
print(df.shape)

#display every column name so we know which features are available
print("\nColumns")
print(df.columns.tolist())

#count how many records belong to each league
print("\nLeague Counts")
print(df["league"].value_counts(dropna=False))

# Count the number of records for each season.
print("\nSEASON COUNTS")
print(df["season"].value_counts(dropna=False).sort_index())

# Show the number of missing values in each column.
print("\nMISSING VALUES")
print(df.isnull().sum().sort_values(ascending=False))

# Filter for Premier League records only.
pl_df = df[df["league"] == "EPL"].copy()

#from 24-25 season
pl_2024_25 = pl_df[pl_df["season"] == "2024/25"].copy()
# Display the number of player records in the selected season.
print("2024–25 player records:", len(pl_2024_25))

# Show the first 10 players and their performance statistics.
print(
    pl_2024_25[
        ["player_name", "team_title", "season", "games", "time",
         "goals", "assists", "xG", "xA"]
    ].head(10).to_string(index=False)
)

# Summarise the filtered Premier League dataset.
print("\nPREMIER LEAGUE SUMMARY")
print("Rows:", len(pl_df))
print("Unique players:", pl_df["player_name"].nunique())
print("Unique clubs:", pl_df["team_title"].nunique())
print("Seasons:", sorted(pl_df["season"].dropna().unique()))

# Display a few Premier League records for a final sanity check.
print("\nPREMIER LEAGUE SAMPLE")
print(
    pl_df[
        ["player_name", "team_title", "season", "games", "time",
         "goals", "assists", "xG", "xA"]
    ].head(10).to_string(index=False)
)
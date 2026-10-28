
# Import DuckDB to query the historical valuation database.
import duckdb

# Import pandas to inspect the Understat CSV.
import pandas as pd

# Import Path to locate project files.
from pathlib import Path

# Define the paths to both datasets.
database_path = Path(
    "data/raw/transfermarkt/transfermarkt-datasets.duckdb"
)
understat_path = Path(
    "data/raw/understat/understat_players_2014_2024.csv"
)

# Load the Understat player statistics.
understat = pd.read_csv(understat_path)

# Keep only Premier League records from the 2014/15–2024/25 seasons.
pl_understat = understat[
    (understat["league"] == "EPL")
    & (understat["season"].isin([
        "2014/15", "2015/16", "2016/17", "2017/18",
        "2018/19", "2019/20", "2020/21", "2021/22",
        "2022/23", "2023/24", "2024/25"
    ]))
].copy()

# Open the Transfermarkt database in read-only mode.
connection = duckdb.connect(str(database_path), read_only=True)

try:
    # Count distinct players with GB1 valuations within each season window.
    # These dates are provisional season boundaries for coverage checking,
    # not yet the final rule for choosing a valuation.
    valuation_coverage = connection.execute("""
        WITH seasons AS (
            SELECT '2014/15' AS season, DATE '2014-08-01' AS start_date, DATE '2015-07-31' AS end_date
            UNION ALL SELECT '2015/16', DATE '2015-08-01', DATE '2016-07-31'
            UNION ALL SELECT '2016/17', DATE '2016-08-01', DATE '2017-07-31'
            UNION ALL SELECT '2017/18', DATE '2017-08-01', DATE '2018-07-31'
            UNION ALL SELECT '2018/19', DATE '2018-08-01', DATE '2019-07-31'
            UNION ALL SELECT '2019/20', DATE '2019-08-01', DATE '2020-07-31'
            UNION ALL SELECT '2020/21', DATE '2020-08-01', DATE '2021-07-31'
            UNION ALL SELECT '2021/22', DATE '2021-08-01', DATE '2022-07-31'
            UNION ALL SELECT '2022/23', DATE '2022-08-01', DATE '2023-07-31'
            UNION ALL SELECT '2023/24', DATE '2023-08-01', DATE '2024-07-31'
            UNION ALL SELECT '2024/25', DATE '2024-08-01', DATE '2025-07-31'
        )
        SELECT
            s.season,
            COUNT(*) AS valuation_records,
            COUNT(DISTINCT v.player_id) AS unique_players
        FROM seasons s
        LEFT JOIN player_valuations v
            ON v.player_club_domestic_competition_id = 'GB1'
            AND v.date BETWEEN s.start_date AND s.end_date
        GROUP BY s.season
        ORDER BY s.season
    """).fetchdf()

    # Display the valuation coverage by football season.
    print("\nVALUATION COVERAGE BY SEASON")
    print(valuation_coverage.to_string(index=False))

    # Display the number of Understat records and players in each season.
    print("\nUNDERSTAT COVERAGE BY SEASON")
    print(
        pl_understat.groupby("season").agg(
            player_records=("player_name", "size"),
            unique_players=("player_name", "nunique")
        ).reset_index().to_string(index=False)
    )

finally:
    # Close the database connection after the queries finish.
    connection.close()

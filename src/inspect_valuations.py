import duckdb

from pathlib import Path

database_path = Path(
    "data/raw/transfermarkt/transfermarkt-datasets.duckdb"
)

connection = duckdb.connect(str(database_path), read_only = False)

try:
     # Count valuation records and inspect their date range.
    print("\nVALUATION DATA SUMMARY")
    print(
        connection.execute("""
            SELECT
                COUNT(*) AS total_records,
                COUNT(DISTINCT player_id) AS unique_players,
                MIN(date) AS earliest_valuation,
                MAX(date) AS latest_valuation
            FROM player_valuations
        """).fetchdf().to_string(index=False)
    )

    # Count valuations by domestic competition identifier.
    print("\nVALUATIONS BY COMPETITION")
    print(
        connection.execute("""
            SELECT
                player_club_domestic_competition_id AS competition_id,
                COUNT(*) AS valuation_records,
                COUNT(DISTINCT player_id) AS unique_players
            FROM player_valuations
            GROUP BY competition_id
            ORDER BY valuation_records DESC
            LIMIT 20
        """).fetchdf().to_string(index=False)
    )

    # Inspect the Premier League competition identifier in the competitions table.
    print("\nPOSSIBLE PREMIER LEAGUE COMPETITION IDS")
    print(
        connection.execute("""
            SELECT competition_id, name, country_name
            FROM competitions
            WHERE LOWER(name) LIKE '%premier league%'
               OR LOWER(competition_code) LIKE '%premier%'
        """).fetchdf().to_string(index=False)
    )

    # Show a few valuation records for a quick sanity check.
    print("\nVALUATION SAMPLE")
    print(
        connection.execute("""
            SELECT
                player_id,
                date,
                market_value_in_eur,
                current_club_name,
                player_club_domestic_competition_id
            FROM player_valuations
            ORDER BY date DESC
            LIMIT 10
        """).fetchdf().to_string(index=False)
    )

finally:
    # Close the connection after the inspection is complete.
    connection.close()

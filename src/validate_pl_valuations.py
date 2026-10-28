
# Import DuckDB to query the Transfermarkt database.
import duckdb

# Import Path to locate the database file.
from pathlib import Path

# Define the database path relative to the project root.
database_path = Path(
    "data/raw/transfermarkt/transfermarkt-datasets.duckdb"
)

# Open the database in read-only mode.
connection = duckdb.connect(str(database_path), read_only=True)

try:
    # Count English Premier League valuation records by calendar year.
    print("\nPREMIER LEAGUE VALUATIONS BY YEAR")
    print(
        connection.execute("""
            SELECT
                EXTRACT(YEAR FROM date) AS valuation_year,
                COUNT(*) AS valuation_records,
                COUNT(DISTINCT player_id) AS unique_players
            FROM player_valuations
            WHERE player_club_domestic_competition_id = 'GB1'
            GROUP BY valuation_year
            ORDER BY valuation_year
        """).fetchdf().to_string(index=False)
    )

    # Check how many player valuations exist in each season-year grouping.
    print("\nVALUATION RECORDS PER PLAYER AND YEAR")
    print(
        connection.execute("""
            WITH yearly_valuations AS (
                SELECT
                    player_id,
                    EXTRACT(YEAR FROM date) AS valuation_year,
                    COUNT(*) AS records_in_year
                FROM player_valuations
                WHERE player_club_domestic_competition_id = 'GB1'
                GROUP BY player_id, valuation_year
            )
            SELECT
                records_in_year,
                COUNT(*) AS player_year_groups
            FROM yearly_valuations
            GROUP BY records_in_year
            ORDER BY records_in_year
        """).fetchdf().to_string(index=False)
    )

    # Inspect Premier League player metadata for several well-known players.
    print("\nPLAYER METADATA SAMPLE")
    print(
        connection.execute("""
            SELECT
                player_id,
                name,
                date_of_birth,
                position,
                sub_position,
                current_club_name,
                market_value_in_eur
            FROM players
            WHERE LOWER(name) IN (
                'bukayo saka',
                'mohamed salah',
                'erling haaland',
                'cole palmer'
            )
            ORDER BY name
        """).fetchdf().to_string(index=False)
    )

finally:
    # Close the database connection after the queries finish.
    connection.close()


# Import DuckDB to query the Transfermarkt database.
import duckdb

# Import Path to locate the database file.
from pathlib import Path

# Define the path to the downloaded database.
database_path = Path(
    "data/raw/transfermarkt/transfermarkt-datasets.duckdb"
)

# Open the database in read-only mode.
connections = duckdb.connect(str(database_path), read_only=True)

try:
    # Find players using partial name matching.
    print("\nPLAYER IDENTITIES")

    players = connections.execute("""
        SELECT
            player_id,
            name,
            date_of_birth,
            position,
            current_club_name
        FROM players
        WHERE LOWER(name) LIKE '%bukayo%saka%'
           OR LOWER(name) LIKE '%mo%salah%'
           OR LOWER(name) LIKE '%erling%haaland%'
           OR LOWER(name) LIKE '%cole%palmer%'
        ORDER BY name
    """).fetchdf()

    # Display the matching player records.
    print(players.to_string(index=False))

    # Retrieve historical valuations for the player IDs we found.
    print("\nHISTORICAL VALUATIONS")

    # Skip the valuation query if the name search returned no matches.
    if not players.empty:
        # Extract the player IDs returned by the first query.
        player_ids = players["player_id"].tolist()

        # Create one SQL placeholder per player ID.
        placeholders = ", ".join("?" for _ in player_ids)

        # Query valuation history using the matched player IDs.
        valuations = connections.execute(f"""
            SELECT
                p.player_id,
                p.name,
                v.date,
                v.market_value_in_eur,
                v.current_club_name,
                v.player_club_domestic_competition_id
            FROM player_valuations AS v
            JOIN players AS p
                ON p.player_id = v.player_id
            WHERE p.player_id IN ({placeholders})
            ORDER BY p.name, v.date
        """, player_ids).fetchdf()

        # Display the historical valuation records.
        print(valuations.to_string(index=False))
    else:
        # Explain why no valuation records were displayed.
        print("No matching players were found.")

finally:
    # Close the database connection even if an error occurs.
    connections.close()

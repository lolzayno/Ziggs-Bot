import database
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
#fetch all champion averages
def fetch_champions(player_id):
    engine = database.establish_connection()
    sql = """
    SELECT * FROM champions
    WHERE player_id = :id
    """
    with engine.connect() as connection:
        result = connection.execute(text(sql), {
            "id": player_id
        })
        row = result.fetchall()
        return row
#fetch champion averages
def fetch_champ_averages(player_id, champion):
    engine = database.establish_connection()
    sql = """
    SELECT * FROM champions
    WHERE player_id = :id
    AND champ_name = :champ
    """
    with engine.connect() as connection:
        result = connection.execute(text(sql), {
            "id": player_id,
            "champ": champion
        })
        row = result.fetchall()
        return row[0]

#fetches all the runes
def fetch_rune_averages(player_id, champion):
    engine = database.establish_connection()
    sql = """
    SELECT * FROM runes
    WHERE player_id = :id
    AND champ_name = :champ
    """
    with engine.connect() as connection:
        result = connection.execute(text(sql), {
            "id": player_id,
            "champ": champion
        })
        row = result.fetchall()
        return row

#fetches individual rune
def fetch_individual_rune(player_id, champion, rune):
    engine = database.establish_connection()
    sql = """
    SELECT * FROM runes
    WHERE player_id = :id
    AND champ_name = :champ
    AND rune_name = :rune
    """
    with engine.connect() as connection:
        result = connection.execute(text(sql), {
            "id": player_id,
            "champ": champion,
            "rune": rune
        })
        row = result.fetchone()
        return row

#fetches all matchups in a lane
def fetch_matchups(player_id, champion, lane):
    engine = database.establish_connection()
    sql = """
    SELECT * FROM matchups
    WHERE player_id = :id
    AND champ_name = :champ
    AND lane = :lane
    """
    with engine.connect() as connection:
        result = connection.execute(text(sql), {
            "id": player_id,
            "champ": champion,
            "lane": lane
        })
        row = result.fetchall()
        return row
#Fetches matchup of a specific opponent and lane
def fetch_champ_matchup(player_id, champion, lane, opponent):
    engine = database.establish_connection()
    sql = """
    SELECT * FROM matchups
    WHERE player_id = :id
    AND champ_name = :champ
    AND opponent_name = :opponent
    AND lane = :lane
    """
    with engine.connect() as connection:
        result = connection.execute(text(sql), {
            "id": player_id,
            "champ": champion,
            "opponent": opponent,
            "lane": lane
        })
        row = result.fetchone()
        return row

def fetch_unique_champions(player_id):
    engine = database.establish_connection()
    sql = """
    SELECT DISTINCT championName FROM matches
    WHERE player_id = :id
    """
    with engine.connect() as connection:
        result = connection.execute(text(sql), {
            "id": player_id
        })
        rows = result.fetchall()

        champions = [row[0] for row in rows]
        return champions
def fetch_unique_opponents(player_id):
    engine = database.establish_connection()
    sql = """
    SELECT DISTINCT opponent FROM matches
    WHERE player_id = :id
    """
    with engine.connect() as connection:
        result = connection.execute(text(sql), {
            "id": player_id
        })
        rows = result.fetchall()

        champions = [row[0] for row in rows]
        return champions

from sqlalchemy import text

def fetch_unique_items(player_id):
    engine = database.establish_connection()
    sql = """
    SELECT DISTINCT item0 AS item FROM matches WHERE player_id = :id
    UNION
    SELECT DISTINCT item1 AS item FROM matches WHERE player_id = :id
    UNION
    SELECT DISTINCT item2 AS item FROM matches WHERE player_id = :id
    UNION
    SELECT DISTINCT item3 AS item FROM matches WHERE player_id = :id
    UNION
    SELECT DISTINCT item4 AS item FROM matches WHERE player_id = :id
    UNION
    SELECT DISTINCT item5 AS item FROM matches WHERE player_id = :id
    UNION
    SELECT DISTINCT item6 AS item FROM matches WHERE player_id = :id
    """
    with engine.connect() as connection:
        result = connection.execute(text(sql), {
            "id": player_id
        })
        rows = result.fetchall()

        items = [row[0] for row in rows]
        return items


#fetches all matches
def fetch_matches_all(player_id):
    engine = database.establish_connection()
    sql = """
    SELECT * FROM matches
    WHERE player_id = :id
    """
    with engine.connect() as connection:
        result = connection.execute(text(sql), {
            "id": player_id
        })
        row = result.fetchall()
        return row

#fetch single match details
def fetch_match_single(player_id, match_code):
    engine = database.establish_connection()
    sql = """
    SELECT * FROM matches
    WHERE player_id = :id
    AND match_code = :match
    """
    with engine.connect() as connection:
        result = connection.execute(text(sql), {
            "id": player_id,
            "match": match_code
        })
        row = result.fetchone()
        return row
    
def fetch_item_all(player_id, champion):
    engine = database.establish_connection()
    sql = """
    SELECT * FROM items
    WHERE player_id = :id
    AND champ_name = :champ
    """
    with engine.connect() as connection:
        result = connection.execute(text(sql), {
            "id": player_id,
            "champ": champion
        })
        row = result.fetchall()
        return row

def fetch_item_single(player_id, champion, item):
    engine = database.establish_connection()
    sql = """
    SELECT * FROM items
    WHERE player_id = :id
    AND champ_name = :champ
    AND item_name = :item
    """
    with engine.connect() as connection:
        result = connection.execute(text(sql), {
            "id": player_id,
            "champ": champion,
            "item": item
        })
        row = result.fetchone()
        return row
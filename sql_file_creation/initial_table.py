import sqlite3

conn = sqlite3.connect("football.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS league (
    league_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    league_name TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS team (
    team_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    league_ID INTEGER,
    team_name TEXT NOT NULL,
    FOREIGN KEY (league_ID) REFERENCES league(league_ID),
    UNIQUE (league_ID, team_name)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS season (
    season_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    league_ID INTEGER,
    year INTEGER NOT NULL,
    FOREIGN KEY (league_ID) REFERENCES league(league_ID),
    UNIQUE (league_ID, year)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS game (
    game_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    season_ID INTEGER,
    week INTEGER NOT NULL,
    away_team_ID INTEGER,
    home_team_ID INTEGER,
    away_team_score INTEGER,
    home_team_score INTEGER,
    overtime BOOLEAN,
    home_power_change REAL,
    away_power_change REAL,
    bonus INTEGER,
    FOREIGN KEY (season_ID) REFERENCES season(season_ID),
    FOREIGN KEY (away_team_ID) REFERENCES team(team_ID),
    FOREIGN KEY (home_team_ID) REFERENCES team(team_ID)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS weekly_power_score (
    power_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    team_ID INTEGER,
    season_ID INTEGER,
    week INTEGER,
    power_score REAL,
    wins INTEGER,
    losses INTEGER,
    ties INTEGER,
    ranking INTEGER,
    FOREIGN KEY (team_ID) REFERENCES team(team_ID),
    FOREIGN KEY (season_ID) REFERENCES season(season_ID)
)
""")

conn.commit()
conn.close()

import sqlite3 as sql

def connection(name = "data.db"):
    conn = sql.connect(name)
    return conn

def create_tables(conn):
    curs = conn.cursor()
    curs.execute("CREATE TABLE IF NOT EXISTS archive(name TEXT, description TEXT, date TEXT, id INT PRIMARY KEY)")
    curs.execute("CREATE TABLE IF NOT EXISTS countries(user_id INT PRIMARY KEY, country_name TEXT, leader_name TEXT, ideology, second_ideology TEXT, government TEXT, gdp INT, territories TEXT, s INT, population INT)")
    curs.execute(f"CREATE TABLE IF NOT EXISTS servers(id INT PRIMARY KEY, bud INT, crzp INT, population INT, well INT, sanctions INT)")

    conn.commit()
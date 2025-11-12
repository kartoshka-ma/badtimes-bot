import asyncpg
import asyncio
import json


class AsyncpgErrors:
    PostgresError = asyncpg.PostgresError
    UniqueViolationError = asyncpg.UniqueViolationError
    InterfaceError = asyncpg.InterfaceError
    ConnectionDoesNotExistError = asyncpg.ConnectionDoesNotExistError


async def connection(database_url="postgresql://neondb_owner:npg_NmLJvBV9p6iY@ep-winter-wave-a88x4pg2-pooler.eastus2.azure.neon.tech/neondb?sslmode=require&channel_binding=require"):
    """
    Создает соединение с PostgreSQL.
    database_url пример: postgresql://username:password@localhost/dbname
    """
    conn = await asyncpg.connect(dsn=database_url)
    return conn

async def create_tables(conn):
    """
    Создает таблицы в PostgreSQL.
    """
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS archive (
            id SERIAL PRIMARY KEY,
            name TEXT,
            description TEXT,
            date TEXT
        )
    """)

    await conn.execute("""
        CREATE TABLE IF NOT EXISTS countries (
            user_id BIGSERIAL PRIMARY KEY,
            country_name TEXT,
            leader_name TEXT,
            ideology TEXT,
            second_ideology TEXT,
            government TEXT,
            gdp BIGINT,
            territories TEXT,
            s INT,
            population BIGINT
        )
    """)

    await conn.execute("""
        CREATE TABLE IF NOT EXISTS servers (
            id BIGSERIAL PRIMARY KEY,
            bud BIGINT,
            crzp BIGINT,
            population BIGINT,
            well INT,
            sanctions INT
        )
    """)

async def main():
    conn = await connection()
    await create_tables(conn)
    await conn.close()

if __name__ == "__main__":
    asyncio.run(main())

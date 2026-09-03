from sqlalchemy import create_engine, text

DATABASE_URL = (
    "postgresql+psycopg2://"
    "analyst:analyst_password@localhost:5432/analytics"
)

engine = create_engine(DATABASE_URL)


def execute_sql(query: str)->list[dict]:
    """Execute a read-only SQL query and return the results."""

    with engine.connect() as connection:
        result = connection.execute(text(query))

        return [dict(row._mapping) for row in result]
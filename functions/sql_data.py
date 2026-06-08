import sqlalchemy
from typing import Union
from urllib.parse import quote_plus
import pandas as pd
import pyodbc

INCO_BISQL_USR: Union[str, None] = (
    "sa_EnvironmentalProducts"  # os.getenv("INCO_BISQL_USR")
)
assert not (INCO_BISQL_USR is None)

INCO_BISQL_PWD: Union[str, None] = (
    "ULk8W4tSjJrbzqTtYXbxa3Qoxcutkeqh7BwGlNFzUj8guLLYuM"  # os.getenv("INCO_BISQL_PWD")
)
assert not (INCO_BISQL_PWD is None)

def incobisql_connection(servername = "inco-bisql") -> "sqlalchemy.engine.base.Engine":
    """Create a SQLAlchemy engine for the InCo SQL Server database.

    Args:
        servername: Server prefix used to build ``{servername}.database.windows.net``.

    Returns:
        sqlalchemy.engine.base.Engine: Connected SQLAlchemy engine.
    """
    server = f"{servername}.database.windows.net"
    database = "InCo"
    username = INCO_BISQL_USR
    password = INCO_BISQL_PWD
    driver = "{ODBC Driver 18 for SQL Server}"

    connection_string = (   
        f"DRIVER={driver};"
        f"SERVER=tcp:{server};"
        f"PORT=1433;"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password};"
        "App=Author: NDI, Team: EP, Platform: Python, Solution: EP.Fundamental.Framework;"
    )

    # URL-encode the connection string
    encoded_conn_str = quote_plus(connection_string)

    # Create the SQLAlchemy engine
    engine = sqlalchemy.create_engine(
        f"mssql+pyodbc:///?odbc_connect={encoded_conn_str}"
    )
    return engine


def get_sql_query(query: str, servername: str = "inco-bisql") -> pd.DataFrame:
    """Execute a SQL query against InCo and return the result set.

    Args:
        query (str): SQL text to execute.
        servername (str): SQL Server prefix for connection.

    Returns:
        pd.DataFrame: Query result as a DataFrame.
    """

    engine = incobisql_connection(servername)

    df = pd.read_sql(query, engine.connect())

    return df

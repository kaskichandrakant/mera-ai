import requests as requests
from langchain.agents import tool
from pydantic import BaseModel, Field
from typing import Optional

CH_HOST = 'http://localhost:8123'  # default address


def get_clickhouse_data(query, host=CH_HOST, connection_timeout=1500):
    r = requests.post(host, params={'query': query},
                      timeout=connection_timeout)

    return r.text


class SQLQuery(BaseModel):
    query: str = Field(description="SQL query to execute")


@tool(args_schema=SQLQuery)
def execute_sql(query: str) -> str:
    """Returns the result of SQL query execution"""
    return get_clickhouse_data(query)


class SQLTable(BaseModel):
    database: str = Field(description="Database name")
    table: str = Field(description="Table name")


@tool(args_schema=SQLTable)
def get_table_columns(database: str, table: str) -> str:
    """Returns list of table column names and types in JSON"""

    q = '''
    select name, type
    from system.columns 
    where database = '{database}'
        and table = '{table}'
    format TabSeparatedWithNames
    '''.format(database=database, table=table)

    return str(get_clickhouse_data(q).to_dict('records'))


class SQLTableColumn(BaseModel):
    database: str = Field(description="Database name")
    table: str = Field(description="Table name")
    column: str = Field(description="Column name")
    n: Optional[int] = Field(description="Number of rows, default limit 10")


@tool(args_schema=SQLTableColumn)
def get_table_column_distr(database: str, table: str, column: str, n: int = 10) -> str:
    """Returns top n values for the column in JSON"""

    q = '''
    select {column}, count(1) as count
    from {database}.{table} 
    group by 1
    order by 2 desc 
    limit {n}
    format TabSeparatedWithNames
    '''.format(database=database, table=table, column=column, n=n)

    return str(list(get_clickhouse_data(q)[column].values))

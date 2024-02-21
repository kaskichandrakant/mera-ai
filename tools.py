from langchain.tools.render import format_tool_to_openai_function

from data_query import execute_sql, get_table_columns, get_table_column_distr

# converting tools into OpenAI functions
sql_functions = list(map(format_tool_to_openai_function,
                         [execute_sql, get_table_columns, get_table_column_distr]))

# saving tools into a dictionary for the future
sql_tools = {
    'execute_sql': execute_sql,
    'get_table_columns': get_table_columns,
    'get_table_column_distr': get_table_column_distr
}

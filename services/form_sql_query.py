from lexicon.lexicon import LEXICON


def form_sql_query(p_dict) -> str:
    if not any(p_dict.values()):
        return LEXICON['nothing_picked_message']

    sql_query = "SELECT name, app_scope, converting, tasks, describtion, link FROM neural_networks WHERE "

    for column_name, substrings in p_dict.items():
        for substring in substrings:
            sql_query += f"{column_name} LIKE '%{substring}%' AND "

    sql_query = sql_query.rstrip(' AND ')

    return sql_query

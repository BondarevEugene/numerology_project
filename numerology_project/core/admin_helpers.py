from flask import request


def get_search_query():

    return request.args.get(
        'q',
        ''
    ).strip()
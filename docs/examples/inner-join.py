# (kommiBo) Synthetic SQLite documentation example; no persistent database.
from contextlib import closing
from _fixture import connect
with closing(connect()) as db:
    rows = db.execute("""
        SELECT p.INTERNAL_NUM, j.JOIN_NAME
        FROM REGISTER AS p INNER JOIN REGISTER_JOIN AS j
          ON j.INTERNAL_NUM = p.INTERNAL_NUM
        ORDER BY p.INTERNAL_NUM, j.INTERNAL_REG_NUM
    """).fetchall()
    assert rows == [(7, 'JOIN'), (7, 'INNER JOIN'), (8, 'LEFT JOIN')]
    print(rows)

# (kommiBo) Synthetic SQLite documentation example; no persistent database.
from contextlib import closing
from _fixture import connect
with closing(connect()) as db:
    rows = db.execute("""
        SELECT p.INTERNAL_NUM,
          (SELECT j.JOIN_NAME FROM REGISTER_JOIN AS j
           WHERE j.INTERNAL_NUM = p.INTERNAL_NUM
           ORDER BY j.DATE_TIME_STAMP DESC, j.INTERNAL_REG_NUM DESC LIMIT 1)
        FROM REGISTER AS p ORDER BY p.INTERNAL_NUM
    """).fetchall()
    assert rows == [(7, 'INNER JOIN'), (8, 'LEFT JOIN'), (9, None)]
    print(rows)

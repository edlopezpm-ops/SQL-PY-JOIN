# (kommiBo) Synthetic SQLite documentation example; no persistent database.
from contextlib import closing
from _fixture import connect
with closing(connect()) as db:
    rows = db.execute("""
        SELECT p.INTERNAL_NUM, j.INTERNAL_REG_NUM
        FROM REGISTER_JOIN AS j LEFT JOIN REGISTER AS p
          ON p.INTERNAL_NUM = j.INTERNAL_NUM AND p.ACTIVE = 'Y'
        ORDER BY j.INTERNAL_REG_NUM
    """).fetchall()
    assert rows == [(7, 1), (7, 2), (None, 3)]
    print(rows)

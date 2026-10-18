# (kommiBo) Synthetic SQLite documentation example; no persistent database.
from contextlib import closing
from _fixture import connect
with closing(connect()) as db:
    rows = db.execute("""
        SELECT a.JOIN_NAME, b.JOIN_NAME
        FROM REGISTER_JOIN AS a INNER JOIN REGISTER_JOIN AS b
          ON a.JOIN_DIRECTION = b.JOIN_DIRECTION
         AND a.INTERNAL_REG_NUM < b.INTERNAL_REG_NUM
        ORDER BY a.INTERNAL_REG_NUM, b.INTERNAL_REG_NUM
    """).fetchall()
    assert rows == [('JOIN', 'INNER JOIN')]
    print(rows)

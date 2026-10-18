# (kommiBo) Synthetic SQLite documentation example; no persistent database.
from contextlib import closing
from _fixture import connect
with closing(connect()) as db:
    rows = db.execute("""
        WITH active_parent AS (SELECT * FROM REGISTER WHERE ACTIVE = 'Y')
        SELECT p.INTERNAL_NUM AS parent_id, j.INTERNAL_REG_NUM AS child_id
        FROM active_parent AS p LEFT JOIN REGISTER_JOIN AS j
          ON j.INTERNAL_NUM = p.INTERNAL_NUM
        UNION ALL
        SELECT p.INTERNAL_NUM, j.INTERNAL_REG_NUM
        FROM REGISTER_JOIN AS j LEFT JOIN active_parent AS p
          ON p.INTERNAL_NUM = j.INTERNAL_NUM
        WHERE p.INTERNAL_NUM IS NULL
        ORDER BY child_id, parent_id
    """).fetchall()
    assert rows == [(9, None), (7, 1), (7, 2), (None, 3)]
    print(rows)

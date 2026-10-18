# (kommiBo) Synthetic SQLite documentation example; no persistent database.
from contextlib import closing
from _fixture import connect
with closing(connect()) as db:
    rows = db.execute("""
        SELECT p.INTERNAL_NUM, COUNT(*) AS output_rows,
               COUNT(j.INTERNAL_REG_NUM) AS actual_children
        FROM REGISTER p LEFT JOIN REGISTER_JOIN j ON j.INTERNAL_NUM=p.INTERNAL_NUM
        GROUP BY p.INTERNAL_NUM ORDER BY p.INTERNAL_NUM
    """).fetchall()
    assert rows == [(7, 2, 2), (8, 1, 1), (9, 1, 0)]
    assert sum(row[2] for row in rows) == 3
    print(rows)

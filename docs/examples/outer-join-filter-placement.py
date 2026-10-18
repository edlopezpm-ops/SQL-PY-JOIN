# (kommiBo) Synthetic SQLite documentation example; no persistent database.
from contextlib import closing
from _fixture import connect
with closing(connect()) as db:
    on_rows = db.execute("""
        SELECT p.INTERNAL_NUM, j.INTERNAL_REG_NUM FROM REGISTER p
        LEFT JOIN REGISTER_JOIN j ON j.INTERNAL_NUM=p.INTERNAL_NUM AND j.ACTIVE='Y'
        ORDER BY p.INTERNAL_NUM
    """).fetchall()
    where_rows = db.execute("""
        SELECT p.INTERNAL_NUM, j.INTERNAL_REG_NUM FROM REGISTER p
        LEFT JOIN REGISTER_JOIN j ON j.INTERNAL_NUM=p.INTERNAL_NUM
        WHERE j.ACTIVE='Y' ORDER BY p.INTERNAL_NUM
    """).fetchall()
    assert on_rows == [(7, 1), (8, 3), (9, None)]
    assert where_rows == [(7, 1), (8, 3)]
    print('ON:', on_rows)
    print('WHERE:', where_rows)

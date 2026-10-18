# (kommiBo) Synthetic SQLite documentation example; no persistent database.
from contextlib import closing
from _fixture import connect
with closing(connect()) as db:
    parent_count = db.execute('SELECT COUNT(*) FROM REGISTER').fetchone()[0]
    child_count = db.execute('SELECT COUNT(*) FROM REGISTER_JOIN').fetchone()[0]
    rows = db.execute("""
        SELECT p.INTERNAL_NUM, j.INTERNAL_REG_NUM
        FROM REGISTER AS p CROSS JOIN REGISTER_JOIN AS j
        ORDER BY p.INTERNAL_NUM, j.INTERNAL_REG_NUM
    """).fetchall()
    assert len(rows) == parent_count * child_count == 9
    assert rows[0] == (7, 1) and rows[-1] == (9, 3)
    print('3 parents x 3 children = 9 combinations; endpoints:', rows[0], rows[-1])

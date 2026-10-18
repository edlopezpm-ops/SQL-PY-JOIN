# (kommiBo) Synthetic SQLite documentation example; no persistent database.
from contextlib import closing
from _fixture import connect
with closing(connect()) as db:
    rows = db.execute("""
        SELECT INTERNAL_REG_NUM, DATE_TIME_STAMP FROM REGISTER_JOIN
        WHERE DATE_TIME_STAMP >= ? AND DATE_TIME_STAMP < ?
        ORDER BY DATE_TIME_STAMP, INTERNAL_REG_NUM
    """, ('2026-01-01T00:00:00', '2026-01-02T00:00:00')).fetchall()
    assert [row[0] for row in rows] == [1, 2]
    assert db.execute('SELECT DATE_TIME_STAMP FROM REGISTER_JOIN WHERE INTERNAL_REG_NUM=3').fetchone()[0] == '2026-01-02T00:00:00'
    print('January 1 includes child IDs 1 and 2; exact January 2 boundary excluded')

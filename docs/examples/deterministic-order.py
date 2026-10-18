# (kommiBo) Synthetic SQLite documentation example; no persistent database.
from contextlib import closing
from _fixture import connect
with closing(connect()) as db:
    db.execute("UPDATE REGISTER_JOIN SET DATE_TIME_STAMP='2026-01-01T09:00:00' WHERE INTERNAL_NUM=7")
    rows = db.execute("""
        SELECT INTERNAL_REG_NUM FROM REGISTER_JOIN WHERE INTERNAL_NUM=7
        ORDER BY DATE_TIME_STAMP DESC, INTERNAL_REG_NUM DESC
    """).fetchall()
    assert rows == [(2,), (1,)]
    latest = db.execute("""
        SELECT INTERNAL_REG_NUM FROM REGISTER_JOIN WHERE INTERNAL_NUM=7
        ORDER BY DATE_TIME_STAMP DESC, INTERNAL_REG_NUM DESC LIMIT 1
    """).fetchone()[0]
    assert latest == 2
    print('equal timestamps ordered by unique ID descending: 2 then 1; latest=2')

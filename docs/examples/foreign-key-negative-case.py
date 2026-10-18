# (kommiBo) Synthetic SQLite documentation example; no persistent database.
from contextlib import closing
import sqlite3
from _fixture import connect
with closing(connect()) as db:
    assert db.execute('PRAGMA foreign_keys').fetchone()[0] == 1
    try:
        db.execute("""INSERT INTO REGISTER_JOIN
            (INTERNAL_NUM, JOIN_NAME, JOIN_DIRECTION, ACTIVE, DATE_TIME_STAMP)
            VALUES (?, ?, ?, ?, ?)""", (999, 'SYNTHETIC', 'none', 'Y', '2026-01-01T00:00:00'))
    except sqlite3.IntegrityError:
        pass
    else:
        raise AssertionError('Missing parent accepted')
    assert db.execute('SELECT COUNT(*) FROM REGISTER_JOIN').fetchone()[0] == 3
    assert db.execute('PRAGMA foreign_key_check').fetchall() == []
    print('orphan rejected; three original children remain; foreign_key_check empty')

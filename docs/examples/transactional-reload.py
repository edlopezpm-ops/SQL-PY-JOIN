# (kommiBo) Synthetic SQLite documentation example; no persistent database.
from contextlib import closing
from _fixture import connect, source_join_names
names = source_join_names()
assert len(names) == len(set(names)) == 9
with closing(connect()) as db:
    snapshots = []
    first_ids = []
    for _ in range(2):
        db.execute('BEGIN')
        try:
            db.execute('DELETE FROM REGISTER_JOIN')
            db.executemany("""INSERT INTO REGISTER_JOIN
                (INTERNAL_NUM, JOIN_NAME, JOIN_DIRECTION, ACTIVE, DATE_TIME_STAMP)
                VALUES (7, ?, 'synthetic', 'Y', '2026-01-01T00:00:00')""", [(name,) for name in names])
            db.execute('COMMIT')
        except Exception:
            db.execute('ROLLBACK')
            raise
        snapshots.append(db.execute('SELECT JOIN_NAME FROM REGISTER_JOIN ORDER BY JOIN_NAME').fetchall())
        first_ids.append(db.execute('SELECT MIN(INTERNAL_REG_NUM) FROM REGISTER_JOIN').fetchone()[0])
    assert snapshots[0] == snapshots[1] and len(snapshots[1]) == 9
    assert first_ids[1] > first_ids[0]
    print('two committed loads; nine equal logical rows each; generated identities advanced')

# (kommiBo) Synthetic SQLite documentation example; no persistent database.
from contextlib import closing
from _fixture import connect
with closing(connect()) as db:
    before = db.execute('SELECT INTERNAL_REG_NUM, JOIN_NAME FROM REGISTER_JOIN ORDER BY INTERNAL_REG_NUM').fetchall()
    db.execute('BEGIN')
    db.execute('DELETE FROM REGISTER_JOIN')
    assert db.execute('SELECT COUNT(*) FROM REGISTER_JOIN').fetchone()[0] == 0
    db.execute('ROLLBACK')
    after = db.execute('SELECT INTERNAL_REG_NUM, JOIN_NAME FROM REGISTER_JOIN ORDER BY INTERNAL_REG_NUM').fetchall()
    assert after == before
    assert not db.in_transaction
    print('inside transaction=0 rows; after rollback=3 rows; original keys preserved')

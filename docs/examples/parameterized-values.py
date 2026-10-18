# (kommiBo) Synthetic SQLite documentation example; no persistent database.
from contextlib import closing
from _fixture import connect
with closing(connect()) as db:
    def lookup(name):
        return db.execute('SELECT JOIN_NAME FROM REGISTER_JOIN WHERE JOIN_NAME = ?', (name,)).fetchall()
    assert lookup('INNER JOIN') == [('INNER JOIN',)]
    assert lookup("' OR 1=1 --") == []
    assert db.execute('SELECT COUNT(*) FROM REGISTER_JOIN').fetchone()[0] == 3
    print('known value matched once; SQL-looking value treated as data; three rows remain')

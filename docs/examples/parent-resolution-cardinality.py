# (kommiBo) Synthetic SQLite documentation example; no persistent database.
from contextlib import closing
from _fixture import connect
with closing(connect()) as db:
    def resolve(name):
        rows = db.execute('SELECT INTERNAL_NUM FROM REGISTER WHERE SCRIPT_NAME = ?', (name,)).fetchall()
        if len(rows) != 1:
            raise ValueError(f'Expected one parent, found {len(rows)}')
        return rows[0][0]
    assert resolve('SP_CreateTables') == 7
    db.execute("INSERT INTO REGISTER VALUES (10, 'SP_CreateTables', 'Y')")
    try:
        resolve('SP_CreateTables')
    except ValueError as error:
        assert 'found 2' in str(error)
    else:
        raise AssertionError('Ambiguous name accepted')
    duplicates = db.execute('SELECT SCRIPT_NAME, COUNT(*) FROM REGISTER GROUP BY SCRIPT_NAME HAVING COUNT(*) > 1').fetchall()
    assert duplicates == [('SP_CreateTables', 2)]
    print('unique name resolves to 7; duplicate name detected before scalar use')

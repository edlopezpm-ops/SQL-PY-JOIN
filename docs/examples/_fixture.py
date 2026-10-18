# (kommiBo) Synthetic in-memory teaching schema; not the SQL Server schema validator.
from pathlib import Path
import re
import sqlite3

def connect():
    db = sqlite3.connect(':memory:', isolation_level=None)
    db.execute('PRAGMA foreign_keys=ON')
    db.executescript("""
        CREATE TABLE REGISTER (
            INTERNAL_NUM INTEGER PRIMARY KEY,
            SCRIPT_NAME TEXT NOT NULL,
            ACTIVE TEXT NOT NULL
        );
        CREATE TABLE REGISTER_JOIN (
            INTERNAL_REG_NUM INTEGER PRIMARY KEY AUTOINCREMENT,
            INTERNAL_NUM INTEGER NOT NULL REFERENCES REGISTER(INTERNAL_NUM),
            JOIN_NAME TEXT NOT NULL,
            JOIN_DIRECTION TEXT NOT NULL,
            JOIN_NOTES TEXT,
            ACTIVE TEXT NOT NULL,
            DATE_TIME_STAMP TEXT NOT NULL
        );
        INSERT INTO REGISTER VALUES
            (7, 'SP_CreateTables', 'Y'), (8, 'SyntheticOther', 'N'), (9, 'SyntheticEmpty', 'Y');
        INSERT INTO REGISTER_JOIN
            (INTERNAL_NUM, JOIN_NAME, JOIN_DIRECTION, JOIN_NOTES, ACTIVE, DATE_TIME_STAMP)
        VALUES
            (7, 'JOIN', 'matching', NULL, 'Y', '2026-01-01T09:00:00'),
            (7, 'INNER JOIN', 'matching', 'synthetic', 'N', '2026-01-01T17:00:00'),
            (8, 'LEFT JOIN', 'left', NULL, 'Y', '2026-01-02T00:00:00');
    """)
    return db

def source_join_names():
    source = Path(__file__).resolve().parents[2] / 'SP_CreateTables.sql'
    return re.findall(r"\(@InternalNum,'([^']+)'", source.read_text(encoding='utf-8'))

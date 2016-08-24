DROP TABLE IF EXISTS dmpd_cdma_thjwq_inf_201606;
CREATE TABLE dmpd_cdma_thjwq_inf_201606 (
	op_time        INTEGER,
	acc_nbr        TEXT,
	dir_type       TEXT,
    called_nbr     TEXT,
    prove_seg      TEXT,
    call_duration  INTEGER,
    call_cnt       INTEGER,
    last_call_date INTEGER,
	latn_id        TEXT
);
.separator ","
.import L1-CDMA_THJWQ_201606.csv dmpd_cdma_thjwq_inf_201606

DROP TABLE IF EXISTS blacklist;
CREATE TABLE blacklist (
    id       INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    op_time  TEXT,
    acc_nbr  TEXT UNIQUE
);
.separator "|"
.import BLACKLIST_201606.csv blacklist

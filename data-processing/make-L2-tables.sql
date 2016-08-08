DROP TABLE IF EXISTS cdma_thjwq_summary_201606;
CREATE TABLE cdma_thjwq_summary_201606 (
	id             INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    op_time        TEXT,
	acc_nbr        TEXT,
    called_nbr     TEXT,
    call_duration  INTEGER,
    call_cnt       INTEGER,
    last_call_date INTEGER
);

INSERT INTO cdma_thjwq_summary_201606(op_time, acc_nbr, called_nbr, 
  call_duration, call_cnt, last_call_date)
SELECT op_time, acc_nbr, called_nbr, sum(call_duration) AS call_duration, 
       sum(call_cnt) AS call_cnt, max(last_call_date) AS last_call_date
FROM dmpd_cdma_thjwq_inf_201606
GROUP BY op_time, acc_nbr, called_nbr
ORDER BY op_time, acc_nbr, called_nbr;

DROP TABLE IF EXISTS blacklist;
CREATE TABLE blacklist (
  id       INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  op_time  TEXT, 
  acc_nbr  TEXT UNIQUE
);

INSERT INTO blacklist (op_time, acc_nbr)
SELECT op_time, called_nbr
FROM cdma_thjwq_summary_201606
GROUP BY op_time, called_nbr
ORDER BY count(*) DESC
LIMIT 10;

INSERT INTO blacklist (op_time, acc_nbr)
SELECT op_time, acc_nbr
FROM cdma_thjwq_summary_201606
GROUP BY op_time, acc_nbr
LIMIT 2;

-- Drop dmpd_cdma_thjwq_inf_201606 because it does not contain an 'id' field which is required
-- by Django model
DROP TABLE dmpd_cdma_thjwq_inf_201606;

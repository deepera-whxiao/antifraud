L0_TBL1=L0-DMPD_CDMA_THJWQ_INF_201606_sample.csv.gz
L1_TBL1=L1-CDMA_THJWQ_201606.csv.gz
BLACKLIST_FILE=BLACKLIST_201606.csv.gz
L1_SQLITE3_LOAD_SCRIPT=load-L1-thjwq.sql
L2_SQLITE3_PROCESS_SCRIPT=make-L2-tables.sql
#MD5_HASH_AWK=md5-hash-column.awk
#L0_TBL1=L0-temp_28w_integ_oth_cdr_m_md5-sample-msisdn_1k.csv.gz
#L0_TBL1=L0-temp_28w_integ_oth_cdr_m_md5-sample-msisdn_3.csv.gz
#L1_TBL1=L1-oth_cdr.csv.gz
#L1_TBL1_ENCRYPT_COL=6
#L1_SQLITE3_LOAD_SCRIPT=load-L1-oth_cdr.sql
#L2_SQLITE3_PROCESS_SCRIPT=make-L2-tables.sql

HAWK_DB=hawk.db


.PHONY: all clean


all: $(HAWK_DB)

$(L1_TBL1): $(L0_TBL1)
	gunzip -c $(L0_TBL1) \
        | sed '1d' \
        | gzip -c > $(L1_TBL1)	

#$(L1_TBL1): $(L0_TBL1) $(MD5_HASH_AWK)
#	# NOTICE: We intentionally replace \t\t twice to insert "NA" between all
#	# consecutive tabs. Please do NOT remove any one of them!
#	gunzip -c $(L0_TBL1) \
#		| sed $$'s/\t\t/\tNA\t/g; s/\t\t/\tNA\t/g; s/^\t/NA\t/; s/\t$$/\tNA/' \
#		| awk -v ENCRYPT_COL=$(L1_TBL1_ENCRYPT_COL) -f $(MD5_HASH_AWK) \
#		| gzip -c > $(L1_TBL1)


$(HAWK_DB): $(L1_TBL1)
	gunzip -c $(L1_TBL1) > $(basename $(L1_TBL1))
	gunzip -c $(BLACKLIST_FILE) > $(basename $(BLACKLIST_FILE))
	sqlite3 $(HAWK_DB) < $(L1_SQLITE3_LOAD_SCRIPT)
	rm -rf $(basename $(L1_TBL1))
	rm -rf $(basename $(BLACKLIST_FILE))
	sqlite3 $(HAWK_DB) < $(L2_SQLITE3_PROCESS_SCRIPT)


clean:
	rm -rf $(L1_TBL1) $(basename $(L1_TBL1)) 
	rm -rf $(basename $(BLACKLIST_FILE)) $(HAWK_DB)

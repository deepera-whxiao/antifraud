HAWK_REST_API_DIR=hawk_rest_api
HAWK_DB_SRC=../data-processing/hawk.db
HAWK_DB_DST=$(HAWK_REST_API_DIR)/db/legacy.sqlite3


.PHONY: all clean inspectdb test


all: inspectdb


$(HAWK_DB_DST): $(HAWK_DB_SRC)
	mkdir -p $$(dirname $(HAWK_DB_DST))
	cp $(HAWK_DB_SRC) $(HAWK_DB_DST)


inspectdb: $(HAWK_DB_DST)
	cd $(HAWK_REST_API_DIR) && python3 manage.py inspectdb \
		--database=legacy >anti_fraud/models.py
	cd $(HAWK_REST_API_DIR) && python3 manage.py makemigrations
	cd $(HAWK_REST_API_DIR) && python3 manage.py migrate


clean:
	rm -rf $(HAWK_REST_API_DIR)/anti_fraud/models.py


test: $(HAWK_DB_DST)
	cd $(HAWK_REST_API_DIR) && python3 manage.py test anti_fraud


# WARNING: The following file is tightly coupled with the unittest codes.
# Please do NOT re-make it unless you know exactly what you are doing!
INIT_LEGACY_TEST_DB_SQL=$(HAWK_REST_API_DIR)/hawk_rest_api/legacy.sqlite3.sql
$(INIT_LEGACY_TEST_DB_SQL): $(HAWK_DB_DST)
	sqlite3 $(HAWK_DB_DST) .dump >$(INIT_LEGACY_TEST_DB_SQL)    

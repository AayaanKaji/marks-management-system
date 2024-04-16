PYTHON = python3
DB_DIR = database
DB_SETUP_DIR = database_setup
DB1 = college_data.py
DB2 = students_data.py
DB3 = teachers_data.py

.PHONY: delete run

run:
	mkdir -p $(DB_DIR)
	$(PYTHON) $(DB_SETUP_DIR)/$(DB1)
	$(PYTHON) $(DB_SETUP_DIR)/$(DB2)
	$(PYTHON) $(DB_SETUP_DIR)/$(DB3)

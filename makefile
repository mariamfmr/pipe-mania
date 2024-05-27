# Directories
SRC_DIR := src
TEST_DIR := tests

# Python script
SCRIPT := $(SRC_DIR)/pipe.py

# Find all .txt files in the tests directory
TXT_FILES := $(wildcard $(TEST_DIR)/*.txt)
# Corresponding .outhyp files
OUTHYP_FILES := $(TXT_FILES:.txt=.outhyp)
# Corresponding expected output files
OUT_FILES := $(TXT_FILES:.txt=.out)

# ANSI color codes
GREEN := \033[0;32m
RED := \033[0;31m
NC := \033[0m  # No Color

# Default target
all: compare

# Rule to generate .outhyp from .txt
%.outhyp: %.txt $(SCRIPT)
	python3 $(SCRIPT) < $< > $@

# Rule to compare .outhyp and .out
compare: $(OUTHYP_FILES)
	@for file in $(TXT_FILES); do \
		base=$$(basename $$file .txt); \
		if diff $(TEST_DIR)/$$base.out $(TEST_DIR)/$$base.outhyp > /dev/null; then \
			echo -e "$(GREEN)Test $$base passed$(NC)"; \
		else \
			echo -e "$(RED)Test $$base failed$(NC)"; \
		fi \
	done

# Clean generated files
clean:
	rm -f $(TEST_DIR)/*.outhyp

.PHONY: all compare clean

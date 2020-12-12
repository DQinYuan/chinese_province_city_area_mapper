sync:
	pipenv run python sync.py

# make local-sync ADCODE_DIR=/adcode/data/adcode(本地存放 adcode csv 文件的目录)
local-sync:
	pipenv run python local-sync.py $(ADCODE_DIR)

test:
	pipenv run python setup.py test

.PHONY: sync local-sync

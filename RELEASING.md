# Releasing eWAVE

check out the latest release of cldf-datasets/ewave
```shell
git clone --branch v3.0.1 --depth 1 https://github.com/cldf-datasets/ewave ewave-cldf
git clone https://github.com/clld/ewave
cd ewave
pip install -e .[test]
```
run
```shell
clld initdb --cldf ../ewave-cldf/cldf/StructureDataset-metadata.json development.ini
```
run the tests
```shell
pytest
```
release the app software
deploy
Store the tested requirements:
```shell
pip freeze > requirements.txt
```

Store a db dump:
```shell
pg_dump -xO --compress gzip:9 ewave > ewave.sql.gz
```


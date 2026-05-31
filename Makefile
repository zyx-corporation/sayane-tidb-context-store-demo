.PHONY: install test init ingest ingest-embed search-text search-vector search-hybrid logs

install:
	python -m pip install -e .

test:
	pytest

init:
	sayane-tidb-demo init

ingest:
	sayane-tidb-demo ingest data/sample_docs

ingest-embed:
	sayane-tidb-demo ingest data/sample_docs --embed

search-text:
	sayane-tidb-demo search "TiDB" --mode text

search-vector:
	sayane-tidb-demo search "Context Store Interface" --mode vector

search-hybrid:
	sayane-tidb-demo search "enterprise backend" --mode hybrid

logs:
	sayane-tidb-demo logs

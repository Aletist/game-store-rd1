admin:
	PYTHONPATH=".:${PYTHONPATH}" python -m game_store.admin.app --config configs/admin-dev.yml

test:
	PYTHONPATH=".:${PYTHONPATH}" pytest tests/

test-cov:
	PYTHONPATH=".:${PYTHONPATH}" pytest -v --cov-report term --cov=game_store tests/

test-junit:
	PYTHONPATH=".:${PYTHONPATH}" pytest --cov-report xml --junitxml junit/report.xml tests/

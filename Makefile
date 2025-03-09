compile:
	pip-compile --extra=local

run-server:
	fastapi dev SWADemo/api/api.py

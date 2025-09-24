load_auth:
	python src/manage.py loaddata initial_auth_data
load_lib:
	python src/manage.py loaddata initial_library_data
build:
	docker build -t api:latest .
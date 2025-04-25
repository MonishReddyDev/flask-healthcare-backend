run:
	flask run --host=0.0.0.0 --port=3000

dev:
	FLASK_ENV=development flask run --host=0.0.0.0 --port=5050

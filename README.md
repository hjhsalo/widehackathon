# widehackathon

## dependencies

python >=3.5

## installation

	git clone https://github.com/hjhsalo/widehackathon
	cd widehackathon
	python3 -m venv venv
	source venv/bin/activate
	pip install -r requirements.txt
	cp src/wide_app/secrets_template.py src/wide_app/secrets.py
	# see secrets.py, and replace any temp values with proper values

## running django dev server

In repository root:

	source venv/bin/activate # if not already activated
	cd src/
	python manage.py runserver

Direct web browser to localhost:8000


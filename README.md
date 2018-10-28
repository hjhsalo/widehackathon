# Scrape-O-Matic
## Introduction

A software to run Annif on various texts to produce relevant keywords
and do a database search base on them.
Input can be a text, audio file or a link to a YouTube video.
The speech from audio/video is transribed to text.
A plugin to scrape texts from websites is also provided.
User can also do a recursive search based on obtained article abstracts .

Check provided presentation.pdf for further information.

## Dependencies

python >=3.5

## Installation

	git clone https://github.com/hjhsalo/widehackathon
	cd widehackathon
	python3 -m venv venv
	source venv/bin/activate
	pip install -r requirements.txt
	cp src/wide_app/secrets_template.py src/wide_app/secrets.py
	# see secrets.py, and replace any temp values with proper values


## Running django dev server

In repository root:

	source venv/bin/activate # if not already activated
	cd src/
	python manage.py runserver

Direct web browser to localhost:8000


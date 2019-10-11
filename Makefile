SHELL := /bin/bash

all: feed_db export_start_flask

feed_db: create_db
	python db_feeder.py

create_db:
	python models.py

export_start_flask:
	source export_flask.sh && flask run
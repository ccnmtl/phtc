MANAGE=./manage.py
APP=phtc
FLAKE8=./ve/bin/flake8

jenkins: ./ve/bin/python validate flake8 jshint test

./ve/bin/python: requirements.txt bootstrap.py virtualenv.py
	./bootstrap.py

test: ./ve/bin/python
	$(MANAGE) jenkins

flake8: ./ve/bin/python
	$(FLAKE8) $(APP) --max-complexity=10

jshint: node_modules/jshint/bin/jshint
	./node_modules/jshint/bin/jshint media/js/dashboard.js \
	media/js/checkbox_activity media/js/data_collection_methods.js \
	media/js/design-notation.js media/js/edit_profile.js \
	media/js/feedback.js media/js/matching.js \
	media/js/modalpage.js media/js/nylearns_test_user.js \
	media/js/phtc_chart.js media/js/post_test.js media/js/pre_test.js \
	media/js/profile.js media/js/quizshow.js media/js/reading_exercise.js \
	media/js/registration.js media/js/required_answers.js \
	media/js/special_question.js

node_modules/jshint/bin/jshint:
	npm install jshint --prefix .

runserver: ./ve/bin/python validate
	$(MANAGE) runserver

migrate: ./ve/bin/python validate jenkins
	$(MANAGE) migrate

validate: ./ve/bin/python
	$(MANAGE) validate

shell: ./ve/bin/python
	$(MANAGE) shell_plus

clean:
	rm -rf ve
	rm -rf media/CACHE
	rm -rf reports
	rm celerybeat-schedule
	rm .coverage
	find . -name '*.pyc' -exec rm {} \;

pull:
	git pull
	make validate
	make test
	make migrate
	make flake8

rebase:
	git pull --rebase
	make validate
	make test
	make migrate
	make flake8

# run this one the very first time you check
# this out on a new machine to set up dev
# database, etc. You probably *DON'T* want
# to run it after that, though.
install: ./ve/bin/python validate jenkins
	createdb $(APP)
	$(MANAGE) syncdb --noinput
	make migrate

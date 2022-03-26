maint:
	pre-commit autoupdate && pre-commit run --all-files
	pip-compile -U requirements/lint.in
	pip-compile -U requirements/dev.in

lint:
	mypy flake8_scream --strict
	flake8 .

upload:
	make clean
	python setup.py sdist bdist_wheel && twine upload dist/*

clean:
	python setup.py clean --all
	pyclean .
	rm -rf *.pyc build dist tests/reports docs/build .pytest_cache .tox .coverage html/

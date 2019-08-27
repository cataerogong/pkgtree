rebuild: clean build

build:
	python setup.py bdist_wheel --universal

clean:
	if exist __pycache__ rd /s /q __pycache__
	if exist build rd /s /q build
	if exist dist rd /s /q dist
	if exist pkgtree.egg-info rd /s /q pkgtree.egg-info

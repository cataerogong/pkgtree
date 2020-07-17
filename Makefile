.PHONY: build rebuild clean

build: pkgtree.py setup.py
	python setup.py bdist_wheel --universal

rebuild: clean build

clean:
	-rd /s /q __pycache__
	-rd /s /q build
	-rd /s /q dist
	-rd /s /q pkgtree.egg-info

wheel:
	python setup.py bdist_wheel --universal

clean:
	rd /s /q __pycache__ build dist pkgtree.egg-info

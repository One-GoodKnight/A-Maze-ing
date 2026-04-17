NAME		:= a_maze_ing.py
CONFIG		:= config.txt
MYPY_FLAGS	:= 				\
	--warn-return-any		\
	--warn-unused-ignores	\
	--ignore-missing-imports\
	--disallow-untyped-defs	\
	--check-untyped-defs

install:
	pip install deps/opencv_python-4.13.0.92-cp37-abi3-manylinux_2_28_x86_64.whl
	pip install deps/mlx-2.2-py3-none-any.whl
	pip install pydantic

run:
	python3 $(NAME) $(CONFIG)

debug:
	python3 -m pdb $(NAME)

clean:
	rm -rf __pycache__ */__pycache__ */*/__pycache__
	rm -rf .mypy_cache */.mypy_cache */*/.mypy_cache

lint:
	python3 -m flake8 .
	python3 -m mypy . $(MYPY_FLAGS)

lint-strict:
	python3 -m flake8 .
	python3 -m mypy . $(MYPY_FLAGS) --strict

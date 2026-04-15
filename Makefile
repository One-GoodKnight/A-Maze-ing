NAME	:= a_maze_ing.py

install:
	pip install deps/opencv_python-4.13.0.92-cp37-abi3-manylinux_2_28_x86_64.whl
	pip install deps/mlx-2.2-py3-none-any.whl
	pip install pydantic

run:
	@if [ -z "$(CONF)" ]; then \
		echo "(Makefile) You can set the config file with make run CONF='name'"; \
	fi
	python3 $(NAME) $(CONF)

debug:
	python3 -m pdb $(NAME)

clean:
	rm -rf __pycache__ */__pycache__ */*/__pycache__
	rm -rf .mypy_cache */.mypy_cache */*/.mypy_cache

lint:
	python3 -m flake8 .
	python3 -m mypy .  --warn-return-any		\
--warn-unused-ignores --ignore-missing-imports 	\
--disallow-untyped-defs --check-untyped-defs

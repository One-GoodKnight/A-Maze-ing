NAME	:= a_maze_ing.py

install:
	pip install mlx-2.2-py3-none-any.whl

run:
	@if [ -z "$(CONF)" ]; then \
		echo "(Makefile) You can set the config file with make run CONF='name'"; \
	fi
	python3 $(NAME) $(CONF)

debug:
	python3 -m pdb $(NAME)

clean:
	rm -rf __pycache__
	rm -rf .mypy_cache

lint:
	python3 -m flake8 .
	python3 -m mypy .  --warn-return-any		\
--warn-unused-ignores --ignore-missing-imports 	\
--disallow-untyped-defs --check-untyped-defs

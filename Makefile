NAME=mail_sender

all: build run

build:
	@docker build -t $(NAME) .

run:
	@docker run --rm -v .:/app $(NAME) src/main.py run

test:
	@docker run --rm -v .:/app $(NAME) src/main.py test

.PHONY: all build run test

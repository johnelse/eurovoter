ADDRESS?=127.0.0.1
PORT?=8080

.PHONY: build run

build:
	@docker build -t ${USER}/eurovoter docker

run: build
	docker run -it --rm \
		--name eurovoter \
		-p $(ADDRESS):8080:8080 \
		-v ${PWD}:/eurovoter \
		${USER}/eurovoter \
		/usr/local/bin/init_container.sh

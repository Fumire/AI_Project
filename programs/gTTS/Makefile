IMAGE_NAME = gtts
CONTAINER_NAME = gTTS
RANDOM := $(shell bash -c 'echo $$RANDOM')

all:

build: Dockerfile
	docker build --rm --tag $(IMAGE_NAME) .

delete:
	docker rmi $(IMAGE_NAME)

start:
	docker run --name $(CONTAINER_NAME) --rm --detach --restart "always" --volume /home/fumiremo/public_html/made/speech/TTS:/data --volume $(abspath .):/script --publish $(RANDOM):3306 $(IMAGE_NAME)

interact:
	docker run --name $(CONTAINER_NAME) --rm --interactive --tty --volume /home/fumiremo/public_html/made/speech/TTS:/data --volume $(abspath .):/script --publish $(RANDOM):3306 $(IMAGE_NAME)

stop:
	docker stop $(CONTAINER_NAME)
	docker rm $(CONTAINER_NAME)

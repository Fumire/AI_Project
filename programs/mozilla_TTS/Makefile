IMAGE_NAME = mozilla_tts
CONTAINER_NAME = MozillaTTS

all:

build: Dockerfile
	docker build --rm --tag $(IMAGE_NAME) .

delete:
	docker rmi $(IMAGE_NAME)

start:
	docker run --name $(CONTAINER_NAME) --detach --restart "always" --volume /home/fumiremo/public_html/made/speech/TTS:/data --volume $(abspath .):/script --publish-all $(IMAGE_NAME)

interact:
	docker run --name $(CONTAINER_NAME) --rm --interactive --tty --volume /home/fumiremo/public_html/made/speech/TTS:/data --volume $(abspath .):/script --publish-all $(IMAGE_NAME)

stop:
	docker stop $(CONTAINER_NAME)
	docker rm $(CONTAINER_NAME)

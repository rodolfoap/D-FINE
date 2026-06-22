case "$1" in
e)	vi -p .x
	;;
s)	docker run -ti --rm -v $(pwd):/app/ --hostname dfine --name dfine --gpus all --entrypoint=/bin/bash dfine
	;;
f)	docker-compose logs -f
	;;
"")	docker-compose up -d
	docker-compose logs -f
	;;
esac

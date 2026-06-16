case "$1" in
e)	vi -p .x
	;;
b)	docker build -t dfine:latest .
	;;
s)	docker run -ti --rm -v $(pwd):/app/ -w /app/ --hostname dfine --name dfine --gpus all --entrypoint=/bin/bash dfine
	;;
"")	docker run --gpus all dfine:latest
	;;
esac

docker stop kuna-analyser && docker image rm kuna-analyser

docker build -t kuna-analyser . --no-cache

docker run -it -d --name kuna --hostname kuna-an --rm kuna-analyser
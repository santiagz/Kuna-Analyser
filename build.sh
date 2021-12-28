docker stop kuna && docker image rm kuna-analyser

docker build -t kuna-analyser .

docker run -it -d --name kuna --hostname kuna-an --rm kuna-analyser
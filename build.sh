docker stop kuna && docker image rm kuna

docker build -t kuna-analyser .

docker run -it -d --name kuna --hostname kuna-an --rm kuna-analyser
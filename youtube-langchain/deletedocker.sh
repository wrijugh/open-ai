docker rm $(docker ps -qa) --force 
docker rmi $(docker images -a)

docker kill $(cat .containers.list)
docker rm   $(cat .containers.list)
/usr/bin/sudo /bin/chown -R $(/usr/bin/id -un): .
git clean -xdf -e temp/
docker ps -aq | xargs -r docker rm 2> /dev/null;
docker images -f dangling=true -q | xargs -r docker rmi 2> /dev/null;
docker images --digests | awk '{if($2=="<none>") print $1"@"$3;}' | xargs -r docker rmi 2> /dev/null;
docker volume ls -qf dangling=true | xargs -r docker volume rm 2> /dev/null;
docker network ls --filter driver=bridge -q | xargs -r docker network rm 2> /dev/null;
docker builder prune -f 2> /dev/null;
docker system prune -f 2> /dev/null;

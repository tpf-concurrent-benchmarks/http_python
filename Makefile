
create_directories:
	mkdir -p graphite

init:
	docker swarm init || true

setup: init create_directories

build:
	docker rmi http_python -f || true
	docker build -t http_python .

remove:
	if docker stack ls | grep -q http_python; then \
		docker stack rm http_python; \
	fi

deploy: remove build
	until \
	docker stack deploy \
	-c docker/docker-compose.yaml \
	http_python; \
	do sleep 1; \
	done

dev_build:
	docker rmi http_python_dev -f || true
	docker build -t http_python_dev -f Dockerfile-dev .

dev_deploy: remove dev_build
	until \
	docker stack deploy \
	-c docker/docker-compose-dev.yaml \
	http_python; \
	do sleep 1; \
	done


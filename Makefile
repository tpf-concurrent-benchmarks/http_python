create_directories:
	mkdir -p graphite
	mkdir -p data

copy_env:
	if [ ! -f .env ]; then \
		cp .env.example .env; \
	fi

init:
	docker swarm init || true

setup: init create_directories copy_env

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

logs:
	docker service logs http_python_app -f

run_local_dev:
	uvicorn src.main:app --host 0.0.0.0 --port 8080 --reload-dir src --reload

run_local_prod:
	uvicorn src.main:app --host 0.0.0.0 --port 8080

node_modules:
	cd artillery && npm install

test_load_local:
	./artillery/run_scenario.sh load local

test_load_prod:
	./artillery/run_scenario.sh load prod

purge-bdd:
	docker volume rm $(docker volume ls -q | grep postgres_data || true) || true

purge-all:
	docker-compose down --rmi all -v --remove-orphans

up:
	docker-compose up -d --build

down:
	docker-compose down

all:
	docker compose up --build

clean:
	docker compose down

fclean:
	docker compose down --rmi all

re: fclean all

purge:
	docker compose down
	docker volume rm exo2_data || true

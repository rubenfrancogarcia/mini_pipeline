run app: 
	docker compose --env-file .env -f docker_compose.yml up -d
	docker compose -f docker_compose.yml logs -f db
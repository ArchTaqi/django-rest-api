MANAGE_SCRIPT	:= manage.py

run-docker:
	@sudo docker-compose up -d

run-local:
	@sudo docker-compose -f docker-compose-local.yaml up -d
	@python -m envdir env/local/ python manage.py runserver 0.0.0.0:8000

perms:
    @sudo chown -R ${USER}:${USER} .
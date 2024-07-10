.PHONY: docker venv

docker:
	docker build -f docker/Dockerfile -t web-demo:latest .

run:
	docker-compose -f docker-compose/docker-compose.yml up

run-services-only:
	docker-compose -f docker-compose/docker-compose.yml up keycloak keycloak-db ldap

stop:
	docker-compose -f docker-compose/docker-compose.yml down

venv:
	rm -rf venv
	python3 -m venv venv
	. venv/bin/activate && pip install --upgrade pip
	. venv/bin/activate && pip install -r requirements.txt

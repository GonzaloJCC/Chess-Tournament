export DJANGOPORT := 8000
export DEBUG := True
PSQL = psql
CMD = python3 manage.py
APP = chess_models
export DATABASE_URL = postgresql://alumnodb:alumnodb@localhost:5432/chess

## delete and create a new empty database
#clear_db:
#	@echo Clear Database
#	dropdb --if-exists $(PGDATABASE)
#	createdb

# create alumnodb super user
create_super_user:
	@$(CMD) shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('alumnodb', 'admin@myproject.com', 'alumnodb')"

runserver:
	@$(CMD) runserver $(DJANGOPORT)

update_models:
	@$(CMD) makemigrations $(APP)
	@$(CMD) migrate

shell:
	@echo manage.py  shell
	@$(CMD) shell

dbshell:
	@echo manage.py dbshell
	@$(CMD) dbshell

static:
	@echo manage.py collectstatic
	@$(CMD) collectstatic

fully_update_db:
	@echo del migrations and make migrations and migrate
	rm -rf */migrations
	@$(CMD) makemigrations $(APP) 
	@$(CMD) migrate

test_model:
	@$(CMD) test models.test_models --keepdb

cache:
	@rm -rf $(shell find . -type d -name "__pycache__")

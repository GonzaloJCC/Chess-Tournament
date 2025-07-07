# Chess Tournament
Web application for creating and displaying chess tournaments, allowing the use of Lichess games (via its API).
#TODO: links


## Environment files
There must be at least two environment files in the project:
- `.env`: API configuration file, must be located in chesstournament. It must contain the variables as the example:
	```bash
	# Django secret key. Should be generated
	SECRET_KEY = 'django-insecure-b%m#qjh(149=wr*s_qct30$ckkcz+gdb1sysr&%0zo!0s(e$q0'

	# Hosts
	ALLOWED_HOSTS = '*'

	# CORS settings.
	CORS_ORIGIN_ALLOW_ALL = True
	CORS_ORIGIN_WHITELIST = http://localhost:8000 http://127.0.1:8000 http://localhost:5173 http://127.0.1:5173
	
	# Indicates if the production database is the one being used or not
	PROD_DATABASE = False

	# Local database connection
	LOCAL_DATABASE_URL = 'postgresql://alumnodb:alumnodb@localhost:5432/chess'

	# Production database connection
	PROD_DATABASE_URL = 'AAA://XXX:YYY/ZZZ'
	```
- `.env.development / .env.production`: web server (client) configuration file, must be located in chesstournament-client. It must contain the variables as the example:
	```bash
	# API base URL
	VITE_DJANGOURL = http://localhost:8000/api/v1/
	```

## Installing and running the project
First, you need to clone the repository:
```bash
git clone https://github.com/GonzaloJCC/Chess-Tournament.git
```

Next, you need to get both the API and the web server up and running.

### Run the API
> Note: All the following commands must be performed in the chesstournament folder
> ```bash
> cd chesstournament
> ```

1. Install the dependencies. We recommend creating a virtual environment to avoid conflicts.
```bash
# Create the virtual environment
python3 -m venv venv

# Enter the venv
source venv/bin/activate

#Install the dependencies
python3 -m pip install -r requirements.txt
```

2. Performing Django migrations to create the database. #TODO
```bash
# Generate the migrations
python3 manage.py makemigrations

# Apply the migrations
python3 manage.py migrate
```

3. Additionally, the option to add sample data is given.
```bash
python3 manage.py populate
```

4. Run the django system
```bash
python3 manage.py runserver <Optional port>
```

### Levantar la app web
> Note: All the following commands must be performed in the chesstournament-client folder
> ```bash
> cd chesstournament-client
> ```

1. Install the dependencies
```bash
npm install
```

2. Run the web server
```bash
npm run dev
```

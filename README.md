C2S - Cars to Sale


## API

This API most use Python 3.12

To execute, run the following commands:

```bash
cd api

# install libraries
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create the `.env` file including the environment variables for the backend. To do this, run the following commands:

```bash
cp .env.example .env
```

Edit the `.env` file with the values for all the variables related to the database and the `OPEN_AI_API_KEY`  variable.

To get an OpenAI API key, you can get it from https://platform.openai.com/account/api-keys.

Then, create the containers for the PostgreSQL database with the following command:

```bash
# create postgres docker container
sudo docker compose up

# Populate fake records from cars.csv
python seed.py

# run tests
pytest -vv

# run api
fastapi dev main.py
```

## Prompt

The agent used to filter cars with the OpenAI API is in the `api/prompt.py` module.

You must need to run the API (follow the previous step) before executing the prompt.

Then, in another terminal tab, run the following commands also:

```bash
cd api
source venv/bin/activate

# run prompt
python prompt.py
```


## Mobile

This mobile app most use Node 20

To execute, run the following commands:

```bash
cd mobile

# install dependencies
npm install --save

# run
npm run web
```
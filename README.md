C2S - Cars to Sell


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

# run api
fastapi dev main.py
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
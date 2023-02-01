# this script is only for linux based systems

echo "creating backup directory and .env file..."
mkdir backup
echo "
BOT_TOKEN=my_token
MYSQL_USER=my_user
MYSQL_PASSWORD=my_pass
" >> .env

echo "creating virtual environment..."
python3 -m venv ./venv

source ./venv/bin/activate

echo "installing all requirements..."
pip3 install -r requirements.txt

echo "running server..."
python3 ./src/bot.py

# backup files
Backup your files using telegram bot

Next features have been learnt during the project:

* API requests and particularly interaction with Telegram's API.
* Python scripting
* Basic usage of MySQL

Future developing:
* complete authorization
* support all type of telegram files
* introducing a payment method
* deployment

# installation 

you need mysql and python3 to install backup server 

instructions:
* clone the project
* give execute permission to install.sh file and run. this script creates virtual environment and install requirement automatically for you
* add your environment variables into .env file
* run ``python3 src/migrate.py`` to initialize database

and now you are ready to run your server. 
give execute permission and simply call ``./runserver``

use ``nohup ./runserver.sh > /dev/null 2>&1 &`` if you want to run in background


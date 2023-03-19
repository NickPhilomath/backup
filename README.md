# backup programm
!this programm is under developement 

This application automaticaly detects your files, file changes, new files and backup them automatically.
You can access your files from anywhere, using your phone, laptop, pc or whatever.
Program is designed to back up files in every platform (window, mac, linux, android) and also Telegram bot to manage backed up files.
Backing up system is very similar to how git works.

# backup files in windows 

i dont know what to write here, case it is not ready yet

# backup files using Telegram bot

I have created telegram bot to acces backup files.
Program is very simple for now and more features will be after completing backup programm in window OS

## installation 

you need mysql and python3 to install backup server 

instructions:
* clone the project
* change directory ``cd telegram-bot``
* give execute permission to install.sh file and run. this script creates virtual environment and install requirement automatically for you
* add your environment variables into .env file
* run ``python3 src/migrate.py`` to initialize database

and now you are ready to run your server. 
give execute permission and simply call ``./runserver``

use ``nohup ./runserver.sh > /dev/null 2>&1 &`` if you want to run in background


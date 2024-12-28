#!/bin/bash

   # Перейти в директорию проекта Django
cd /home/sergey/Projects/Python/learning/Dev/yatube_project/yatube

   #Активировать виртуальное окружение, если оно используется
source /home/sergey/Projects/Python/learning/Dev/yatube_project/venv_yatube/bin/activate

   # Запустить сервер Django
python3 manage.py runserver

   # Если скрипт должен запускаться в фоновом режиме, используйте:
   # nohup python3 manage.py runserver &> server.log &
   

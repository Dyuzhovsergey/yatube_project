### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com:Dyuzhovsergey/yatube_project.git
```

```
cd yatube_project
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env_yatube
```

```
source env_yatube/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip setuptools
```

```
pip install -r requirements.txt
```
Обновите пакет pip

```
pip install --upgrade pip setuptools
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

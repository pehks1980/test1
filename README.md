# Test_note

Тестовое задание для вакансии в ИДАГРУПП

## Installation

1 Клонирование репозитория.

    mkdir test_note
    
    git clone https://github.com/pehks1980/test1.git test_note

2 Установка виртуальной среды.

    virtualenv -p python3 env
    . env/bin/activate

3 Установка пакетов для работы ПО.
    
    cd test_note

    pip install -r requirements.txt

4 Миграции.

    python manage.py makemigrations mainapp
    
    python manage.py migrate


## Run (in testing mode)

    python manage.py runserver

    open browser and put http://127.0.0.1:8000 to open index page


## Test (smoketest)
    
    python manage.py test 
    

## e-mail: pehks1980@gmail.com

## github: http://github.com/pehks1980

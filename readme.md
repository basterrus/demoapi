# Тестовое задание для backend разработчика
___
### Функционал проекта

1. Регистрация и авторизация 
2. Поиск музыки с использованием API Last.fm
3. Добавление мероприятия
4. Добавление плейлиста с привязкой к мероприятию
5. Реализована global пагинация
6. Рейтинг треков
7. Авто документирование при помощи swagger

___
## Запуск проекта
1. `Командой docker-compose up`   
Предварительно нужно создать файл `.env` и заполнить его в соответствии
с файлом шаблона `.env.sample`. Будет создан суперпользователь `admin|admin`
Список всех адресов доступен по адресу: `http://127.0.0.1/api/v1/all/`
2. Склонируйте репозиторий с помощью git: `https://github.com/basterrus/demoapi.git`         
   Перейдите (при необходимости) в папку demoapi: `cd demoapi`
   Предварительно нужно создать файл `.env` и заполнить его в соответствии с файлом шаблона `.env.sample`.   
   Выполните команды:         
     `python manage.py makemigrations`               
     `python manage.py migrate`           
     `python manage.py create_su`                        
     `python manage.py runserver`         
   Список всех адресов доступен по адресу: `http://127.0.0.1/api/v1/all/`
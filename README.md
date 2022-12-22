# AskApp

## Описание
Это сервис вопросов и ответов, в котором пользователи могут задавать друг другу вопросы и получать ответы.

### Стек
- Бэкенд Django
- База данных MySQL
- nginx для отдачи статических файлов
- Фронтенд: JS, Django Templates, TwitterBootstrap


### Скриншоты
![Главный экран](screenshots/Screenshot%202022-12-22%20at%2005.00.51.png)

![Обсуждение вопроса](screenshots/Screenshot%202022-12-22%20at%2005.01.11.png)

![Создание вопроса](screenshots/Screenshot%202022-12-22%20at%2005.01.26.png)


## Запуск

### Установка зависимостей
```
pip install -r requirements.txt
npm install
```

### Подготовка базы данных
```
docker pull mysql

docker run --name askdb -e MYSQL_ROOT_PASSWORD=rootpw -e MYSQL_DATABASE=askdb -e MYSQL_USER=askuser -e MYSQL_PASSWORD=askpw -p3306:3306 -d mysql

python manage.py migrate

python manage.py filldb --all 10
```


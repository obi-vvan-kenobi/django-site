1. Клонируем репозиторий
2. docker-compose up:
     - поднимется контейнер с MySql и контейнер с django
     - выполнятся миграции
     - поднимется сервер, доступен по localhost:12333
3. Как поднимутся оба контейнера (первый старт MySql не быстрый), для парсинга книг необходимо выполнить:
     - docker exec -it web /bin/bash -c 'cd utils && python books_data.py'
     - Будет произведено добавление всех данных в БД и сохранение обложек книг в media/.
4. Для доступа в админ-панель нужно создать superuser:
     - docker exec -it web /bin/bash -c 'python manage.py createsuperuser'
5. В django_env.env перечислены переменные окружения, необходимо указать почту (EMAIL) для получения сообщений с формы обратной связи
   и пароль приложения с почты(EMAIL_APP_PASSWORD). Для Yandex: https://id.yandex.ru/security/app-passwords.
   PER_PAGE - для пагинации книг, SOURCE_DATA_FILE - .json для парсинга книг (должен находится в /book_site).

Форма обратной связи доступна для авторизованных пользователей. Установлена валидация полей форм и recaptcha.

Было принято решение считать подкатегориями категорий элементы списка categories, которые стоят на 2 позиции и далее.

В качестве улучшения при парсинге книг: изменял формат изображений обложок в webp, чтобы 'гонять' меньше трафика.

Из нереализованного:
   1. Категории в которой находится книга (кликабельны) - данный пункт был не понят (куда ведет ссылка).
   2. Поиск по статусу

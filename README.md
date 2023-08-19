**Парсинг курса валют (USD, EUR, CNY) с сайта ЦБ (https://www.cbr.ru/scripts/XML_daily.asp?date_req=ДД/ММ/ГГГГ)**

Проект написан на fastAPI (python). БД - PostgreSQL. 

---

Приложение получает данные из XML, сохраняет в базе и выводит их в JSON. Можно вывести все данные, либо только актуальные.

---

<p>
Описание файлов:

.env - данные для подключения к БД.
  
alembic.ini - файл конфигурации alembic
  
main.py - основной скрипт приложения. Содержит эндпоинты
  
models.py - содержит структуру БД и функцию, триггер, представления для миграции
  
parsing.py - производит парсинг сайта
  
schema.py - структура данных для валидации pydantic
  
config/config.py - конфигурация бд
  
config/database.py - подключение к бд
  
migrations/env.py - настройки миграции
</p>

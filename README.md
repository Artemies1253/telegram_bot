# Telegram_bot
python version 3.9
Копируем проект себе в директорию.
Устанавливаем виртуальное окружение.

Устанавливаем необходимые пакеты 
python pip install -r requirements.txt

В директории config cоздаём файл conf.py и заполняем по примеру conf_example

Создаём и применяем миграции к бд если пользуемся локальной бд 
python manage.py makemigrations
python manage.py migrate

Для запуска бота используем команду python manage.py run_bot

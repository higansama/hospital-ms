# hospital-ms

## 1. install mysql
    Make sure username and password of mysql is valid in settings.py
## 2. install the req.text
    As install the req.txt by pip install -r req.txt 
## 3. makemigrations
    run python manage.py makemigrations user_management
    run python manage.py makemigrations admission_rawat_jalan
    run python manage.py migrate user_management
    run python manage.py migrate admission_rawat_jalan

## 4. run the apps
    run python manage.py runserver
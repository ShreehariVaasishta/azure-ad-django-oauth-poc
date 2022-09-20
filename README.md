# azure-ad-django-oauth-poc

## Usage
1. Clone this repo
```
git clone https://github.com/ShreehariVaasishta/azure-ad-django-oauth-poc.git
```
2. `cd azure-ad-django-oauth-poc.git`
3. Rename app_config_example.py to app_config.py(`mv app_config_example.py app_config.py`)
4. Set the App clientId and client Secret([reference docs](https://learn.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app))
5. Install requirements
```
pip install requirements.txt
```
6. start django server
```
python manage.py runserver
```
7. Go to http://localhost:8000

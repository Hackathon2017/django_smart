# specialist smart search

c'est une application de recherche du bon spécialiste dans chaque domaine (Restauration, hôtellerie, médecine, textile, bricolage…) recommandé par les employés de Sofrecom à travers un système de classement "ranking" selon un score et l'avis (avec des photos).

# Installation & run

### Application tree
This application is based on "django framework":

```
│   .gitignore
│   db.sqlite3
│   manage.py
│   README.md
│   requirements.txt
│     
├───smartsearch
│   │   admin.py
│   │   forms.py
│   │   models.py
│   │   serializers.py
│   │   tests.py
│   │   urls.py
│   │   views.py
│   │  
│   ├───migrations
│   │  
│   ├───templates
│   │   ├───includes
│   │   └───smartsearch
│   ├───templatetags
│   │  
│   └───utils
│     
│  
├───smartsearchproject
│  
├───static
│   └───assets
│       ├───css
│       ├───fonts
│       ├───icons
│       ├───images
│       └───js
└───tests
```

Here is a quick description of structure:
* templates - a folder to store html templates.
* static - a folder to store static files (javascript, pictures, css, etc).
* manage.py - a file to run various Django command (we will make some).
* smartsearch/urls.py - url router, maps requests' urls to the corresponding views.
* tests - unit tests (API rest)

### How to install dependancies ?
This application is developped on windows (virtualenv isn't supported)
All dependencies are found in requirements.txt.

```
python -m pip install -r requirements.txt
```


Dependencies:
```
Django==1.10.1
django-disqus==0.5
django-import-export==0.5.0
django-nocaptcha-recaptcha==0.0.19
django-suit==0.2.21
django-wysiwyg-redactor==0.4.9.1
mock==2.0.0
pbr==1.10.0
Pillow==3.3.1
psycopg2==2.6.2
pytz==2016.6.1
six==1.10.0
tablib==0.11.2
django-picklefield==1.0.0 
djangorestframework==3.6.4
pyyaml==3.12
```

### How to migrate databases ?

1- perform the model migrations:
```
python manage.py makemigrations
```

2- migrate the database to the new model:
```
python manage.py migrate
```


### How to run the application ?

get the address from this command:
```
ifconfig
```

launch the server with the found address:"172.16.3.223"
```
python manage.py runserver 172.16.3.223:8000
```


# API REST testing
This application exposes REST API (GET, POST) through "REST django framework":

### GET specialists of speciality=2
```
http://172.16.3.223:8000/specialists?speciality=2

```


### GET all specialists
```
http://172.16.3.223:8000/specialities/all
```

### POST using python
```
#!/usr/bin/env python
import os
import sys
 
import requests, json  

datas = json.dumps({
        "name": "Hechmi hamdi",
        "geocode": "36.808314, 10.183735",
        "about_website": "no web site",
        "phone": "71 455233",
        "speciality": 2 
        })
 
headers = {'content-type': 'application/json'}
response = requests.post("http://172.16.3.223:8000/specialists/", data=datas, headers=headers)
print("response: ", response.text)
```

### GET specialities of domain=2
```
http://172.16.3.223:8000/specialities/?domain=2
```
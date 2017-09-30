# specialist smart search

c'est une application de recherche du bon spécialiste dans chaque domaine (Restauration, hôtellerie, médecine, textile, bricolage…) recommandé par les employés de Sofrecom à travers un système de classement "ranking" selon un score et l'avis (avec des photos).


### Install modules

```
python -m pip install -r requirements.txt
```



### Migration

do the model migrations:
```
python manage.py makemigrations
```

migrate the database to the new model:
```
python manage.py migrate
```


### run the backend

get the address from this command:
```
ifconfig
```

launch the server address:"172.16.3.223"
```
python manage.py runserver 172.16.3.223:8000
```


# API REST


### GET specialists of speciality=2
```
http://172.16.3.223:8000/specialists?speciality=2

```

### POST using python
```
#!/usr/bin/env python
import os
import sys
 
import requests, json  

datas = json.dumps({
        "id": 3,
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
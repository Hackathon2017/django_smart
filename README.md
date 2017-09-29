# specialist smart search

c'est une application de recherche du bon spécialiste dans chaque domaine (Restauration, hôtellerie, médecine, textile, bricolage…) recommandé par les employés de Sofrecom à travers un système de classement "ranking" selon un score et l'avis (avec des photos).

### Migration

do the model migrations:
```
python manage.py makemirations
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


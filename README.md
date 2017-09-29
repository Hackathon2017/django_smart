# specialist smart search

c'est une application de recherche du bon sp�cialiste dans chaque domaine (Restauration, h�tellerie, m�decine, textile, bricolage�) recommand� par les employ�s de Sofrecom � travers un syst�me de classement "ranking" selon un score et l'avis (avec des photos).

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


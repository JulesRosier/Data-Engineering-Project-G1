# Data-Engineering-Project-G1

## Dev setup

### Setup venv

```
python -m venv venv
pip install -r .\requirements.txt
```

### Activeer venv

```
.\venv\Scripts\activate
```

### Adding dependency

```
pip freeze > .\requirements.txt
```
### Port forward voor DB

```
ssh -N -L 3333:127.0.0.1:3306 vicuser@vichogent.be -p 40059

```

### VIC server SSH inloggen en pw opvragen
```
ssh vicuser@vichogent.be -p 40059
cd Data-Engineering-Project-G1/
cat .env
```

### Na vic login: containers builden (eerste keer duurt het iets langer)
```
docker-compose up -d --build
```
### Connectie databank Port Forward (running indien lege tab)
```
ssh -N -L 3333:127.0.0.1:3306 vicuser@vichogent.be -p 40059
```
### MySQL verbinding
```
localhost / 127.0.0.1
port 3333
naam = root
password = toor
```
### Updaten indien dockerfile niet aangepast
```
git pull
docker-compose stop
docker-compose rm (verwijdert niet DB, DB zit in aparte docker volume)
docker-compose up -d --build
```
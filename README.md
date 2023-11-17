# Fridge simulator
Sovelluksessa voi listata, mitä kaikkia aineksia jääkaapista löytyy ja sovellus ehdottaa käyttäjälle reseptejä, joihin käyttäjällä on kotona ainekset. Jokainen käyttäjä on peruskäyttäjä tai ylläpitäjä.

**Sovelluksen ominaisuuksia**
* Käyttäjä voi rekisteröityä sekä kirjautua sisään ja ulos.
* Käyttäjä voi valita listasta mitä kaikkia aineksia häneltä löytyy.
* Käyttäjä voi poistaa omalta listaltaan aineksia, mitä häneltä ei enää löydy.
* Sovellus ehdottaa käyttäjälle reseptejä mihin käyttäjältä löytyy ainekset.
* Käyttäjä voi tykätä reseptistä, jolloin se näytetään käyttäjän tykätyissä resepteissä.
* Käyttäjä voi poistaa reseptiltä tykkäyksen.
* Ylläpitäjä voi lisätä sovellukseen puuttuvia valittavia aineksia ja uusia reseptejä.
  

**Käynnistysohjeet**

Kloonaa ensin repositorio koneellesi.

Luo repositorion juurikansioon tiedosto .env ja lisää sinne seuraavat:

```
DATABASE_URL = <tietokannan paikallinen osoite>
SECRET_KEY = <salainen avain>
```
Siirry seuraavaksi virtuaaliympäristöön komennolla:
```
source venv/bin/activate

```

Lataa riippuvuudet komennolla:
```
pip install -r requirements.txt
```
Luo tietokannat seuraavalla komennolla:
```
psql < schema.sql
```
Nyt sovelluksen voi käynnistää komennolla:
```
flask run
```

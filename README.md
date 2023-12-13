# Fridge simulator
Sovelluksessa voi listata, mitä kaikkia aineksia kotoa löytyy ja sovellus ehdottaa käyttäjälle reseptejä, joihin käyttäjällä on ainekset. Jokainen käyttäjä on peruskäyttäjä tai ylläpitäjä.

**Sovelluksen ominaisudet**
* Käyttäjä voi rekisteröityä sekä kirjautua sisään ja ulos.
* Käyttäjä voi valita listasta mitä kaikkia aineksia häneltä löytyy.
* Käyttäjä voi poistaa omalta listaltaan aineksia, mitä häneltä ei enää löydy.
* Sovellus ehdottaa käyttäjälle reseptejä mihin käyttäjältä löytyy ainekset.
* Käyttäjä voi tykätä reseptistä, jolloin se näytetään käyttäjän tykätyissä resepteissä.
* Käyttäjä voi poistaa reseptiltä tykkäyksen.
* Ylläpitäjä voi lisätä sovellukseen puuttuvia valittavia aineksia ja uusia reseptejä.
  
**Testausta helpottamaan** 

Reseptejä löytyy valitsemalla esimerkiksi seuraavat ainesosat: 

*Chicken Breast, Rice, Olive Oil* 

*Broccoli, Cheese, Pasta*

Sovellus luo automaattisesti ylläpitäjän:

käyttäjänimi: *admin*

salasana: *admin123*



**Käynnistysohjeet**

Lataa ensin repositorio koneellesi.

Luo repositorion juurikansioon tiedosto .env ja lisää sinne seuraavat:

```
DATABASE_URL = <tietokannan paikallinen osoite>
SECRET_KEY = <salainen avain>
```

Luo hakemistoon Pythonin virtuaaliympäristö komennolla:
```
python3 -m venv venv

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


**Laajojen kielimallien käyttö**

[ingredients.json](https://github.com/alannesanni/fridge_simulator/blob/main/ingredients.json) ja [recipes.json](https://github.com/alannesanni/fridge_simulator/blob/main/recipes.json) tiedostojen sisällöt on luotu ChatGPT:n avulla.

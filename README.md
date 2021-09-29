# Projektmunka 2. Discord "SZEHelp" bot

**Hallgatói csoport adatai:**

- Horváth Bálint, DCPWFB
- Unger Márton, BG4HZ2
- Sótonyi Áron, JNNXY1
- Hajas Gábor, CV3Y0B
- Szabó Bence, EAA56F

**Konzulens:** Ősz Olivér

**A projekt tárgyát képező probléma és a projektcél rövid felvázolása:**

Discord bot fejlesztése Python programozási nyelvben, amihez egy weboldalt készítünk. A bot alapötletét az egyetemünkön tanuló hallgatók segítése adta. Bizonyos információkat ad a tanulóknak. Hogy milyen témával kapcsolatos segítséget nyújt, valamint hogy kinek, azt a weboldal felületén lehet beállítani. Programozói tudás nélkül egy legördülő listából lehet a botnak “ha X akkor Y” típusú előre definiált szabályokat adni. A paramétereit az egyes szabályoknak még pluszba meg lehet adni ezen a weboldalon keresztül. Példa egy lehetséges lefutásra: a szabály X részét a legördülő listából kiválasztom, hogy ha valaki üzenetet küld, paraméternek megadom hogy melyik user, majd az Y részét beállítom, akkor küldjön üzenetet a bot és megadom paraméterben hogy milyen fajta üzenetet küldjön.

**A projektterv részletesebb kidolgozása:**

# SZE Help Bot

Projektünk témájaként egy Discord chatbotot fogunk fejleszteni, aminek célja az lesz, hogy segítse a Széchenyi István Egyetemen tanuló hallgatókat.

A bot feladatai közé fog tartozni például különféle tájékozódásban segítő térképek, elérhetőségek megosztása, ügyintézéssel kapcsolatos fontosabb információk nyújtása stb.

Ehhez a bothoz létrehoztunk egy webes REST API-t Flask keretrendszerben, amiben különféle parancsokat lehet létrehozni, törölni, módosítani és listázni.

Tehát botunk célja egyfajta alap információ nyújtás, de ezt folyamatosan bővíteni szeretnénk és rugalmassá tenni, hogy mindig naprakész lehessen a rendszer.

### Chatbot

A botot a Discord Developer Portal segítségével készítjük el Pythonban a Discord modul felhasználásával.

Feladatai lesznek például:

- ügyintézéssel kapcsolatos információk nyújtása pl.: TO ügyintézők elérhetősége
- tájékozódásban segítő térképek nyújtása pl.: a bot képes lesz megmondani egyes nagyobb termek helyeit és bejelölni a térképen számunkra, elmagyarázva, hogy hogyan érjük el azt
- linkgyűjtemény megosztása pl.: működő neptun linkek, tárgyfelvételi mátrix stb.
- fontosabb dátumok megosztása pl.: tárgyfelvétel, tanszünet
- sportolási lehetőségekről tájékoztatás

Ezeket a feladatokat pedig bővítenénk a későbbiekben a webes felületen kisebb parancsokkal, amiket programozási tudás nélkül meg tudunk adni.

Ehhez már készítettünk egy kisebb prototípust kisebb funkciókkal, ami megfelelően működik.

### Adatbázis

A parancsok listáját egy MySQL adatbázisba fogjuk tárolni. Az adatbázisból pedig a bot és a weboldal fogja kiolvasni a megfelelő adatokat. A weboldalon keresztül fogjuk az adatbázis tábláit frissíteni, törölni és létrehozni. A bot pedig a mindig aktuális, beállított paraméterek alapján kiválasztott táblát fogja olvasni.

### Webes felület

Flask segítségével egy minimális REST API-t szeretnénk létrehozni az alábbi végpontokkal, ezzel létrehozva a rugalmasságát a chatbotnak:

Get: parancsok listájának lekérdezése
Post: új parancs hozzáadása a parancsok listájához
Delete: Adott parancs törlése a listából, egy azonosító megadásával

Ezt szeretnénk úgy megoldani, hogy a felhasználó programozási tudás nélkül tudjon commandokat megadni a botnak, egy interfészen keresztül.

Ehhez létrehozunk egy Frontend felületet HTML-ben megfelelően stilizálva CSS-el.

## Eredménytermék

Az eredménytermékünk egy olyan Discord chatbot, amely az SZE-n tanuló hallgatókat friss és kielégítő információkkal ellátja és segíti. Könnyen használható parancsokkal és parancsok hozzáadására alkalmas, programozási tudás nélkül használható webes interfésszel.

## Mérföldkövek

### Alap discord bot létrehozása

A Discord dokumentáció alapján egy alap funkciókkal rendelkező bot létrehozása, amit discord szerverhez lehet rendelni és pár egyszerűbb command végrehajtására képes. Például itt programoznánk le a text outputos funkciókat, és tesztelnénk egy arra létrehozott szerveren.

A parancsokat úgy definiálhatjuk, hogy egy Python függvényhez csatoljuk. A parancsokat ezután a felhasználó a Python függvényhez hasonló módon hívhatja meg. A command egy olyan objektum, amely beburkolja azt a függvényt, amelyet egy szövegparancs hív meg a Discordban. A szöveges parancsnak előtaggal (command_prefix) kell kezdődnie, ami egy általunk előre definiált karakter lehet (pl.: “!”)

### Frontend

Ennél a mérföldkőnél készítjük el az interfész weboldalas részének frontendjét. Ehhez HTML-t és CSS fogunk felhasználni, ahhoz hogy barátságos és könnyen használható, átlátható weboldalt hozzunk létre.

### Adatbázis

A mérföldkő lényege a bot összekötése egy MySQL adatbázissal. Az adatbázisban tároljuk el a parancsokat, amit a maga a bot és az oldal is elér. A webes interfészen keresztül hozzáadni, szerkeszteni és kitörölni is lehet majd az eltárolt parancsokat.

### Backend

Ennél a mérföldkőnél a feladat backend részét készítjük el, amelyet a Flask keretrendszerrel fogunk megvalósítani. Ennek segítségével kerülnek feldolgozásra a parancsok, amelyeket a felhasználó megadott.

### REST API végpontok

Ennek a mérföldkőnek az eredményterméke egy funkcionáló weboldal lesz, minimális REST végpontokkal. A hívások eredményét egy json formátumú üzenet fogja megjeleníteni. A hívások majd az adatbázist fogják manipulálni.

### További commandok leprogramozás

Itt fejlesztenénk le a bot további funkcióit a feljebb felsoroltak közül, amiket az 1. mérföldkőnél még nem tettünk meg.

## Projektszervezet

Discord bot létrehozása, alap funkciókkal
Horváth Bálint

Flask weboldal létrehozása
Hajas Gábor

Frontend elkészítése
Horváth Bálint

REST API végpontok elkészítése
Sótonyi Áron

Adatbázis létrehozása
Unger Márton

További commandok leprogramozása
Szabó Bence

# MORSE (Municipal Office Resource System for its Effectivity)
MORSE je nástroj pro správu agend malých městských úřadů, samospráv a městských částí. Cílem projektu je zjednodušit každodenní provoz úřadu, zvýšit efektivitu a nabídnout moderní systém pro evidenci a správu procesů.

# Vývojářský tým
- Kamil Dvořák
- Martin Kaprál

# Technologie
- Python
- Django
- SQLite3
- Celery

# Instalace
1. Naklonujeme si repozitář v terminálu pomocí ```
   git clone https://github.com/kapr323/KamilAdmin.git```,
2. přejdeme do složky pomocí ```cd KamilAdmin```, pokud v ní ještě nejsme,
3. aktivujeme virtuální prostředí a nainstalujeme požadavky:
```
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
```
4. Spustíme vývojový server:
```
  python manage.py migrate
  python manage.py runserver
```

# Plánované moduly a featury
- [ ] Personalistika
  - [x] Evidence zaměstnanců
  - [x] Organizační struktura úřadu
  - [ ] Automatizace nástupu/odchodu zaměstnance
  - [ ] Upozornění na školení, lékařské prohlídky, platnost smluv
- [x] Interní směrnice a předpisy
  - [x] Archiv a přehled dokumentů
  - [x] Potvrzení seznámení ze strany zaměstnanců
- [ ] Provozní deníky a správa budov
  - [x] Evidence nemovitostí
  - [x] Evidence vozidel
  - [ ] Evidence místností
- [ ] Rezervace
  - [ ] Rezervace nemovitostí
  - [ ] Rezervace vozidel
  - [ ] Rezervace nemovitostí
- [ ] Autorizace
  - [ ] Uživatelské účty
  - [ ] Uživatelská oprávnění
- [ ] E-mailová služba
  - [ ] Posílání notifikací
    - [ ] Pracovní výročí
    - [ ] Životní výročí
    - [ ] Konce smluv
    - [ ] Školení a certifikáty

# Provedení testů
Testy lze provést příkazem ```coverage run -m pytest```
Následně si lze vytvořit v HTML report pomocí ```coverage html```, který zobrazí přehledně pokrytí testů.

# Licence
MIT Licence

# Podrobnější popis a poznámky pro vývoj
- Personalistika
  - Osobní spis na kartě zaměstnance, tedy přehled informací k zaměstnanci se 
snadnou a intuitivní editací jeho osobních údajů, informací a smluv.
  - Hlídání narozenin a pracovních výročí a zasílání upozornění.
  - Hlídání postupů zaměstnanců v platových stupních dle započitatelné praxe
  - Evidence zaměstnanců na DPP a DPČ, hlídání platnosti smluv, evidence 
odpracované doby v rámci dohod a čerpání dovolené.
  - Automatizace procesů a úkolů v rámci nástupu a výstupu zaměstnance.
  - Zasílání upozornění na blížící se termín lékařských prohlídek, povinného 
školení (BOZP, řidiči, vedoucí pracovníci, ...) i různých certifikátů 
jednotlivých zaměstnanců.
  - Evidence uchazečů (?).
- Přehled interních směrnic a předpisů
  - Všichni lidi v organizaci mají k dispozici přehled všech platných směrnic, 
pracovních postupů a dalších dokumentů, kterými se musí řídit.
  - Každý zaměstnanec pak vidí všechny dokumenty, směrnice, pracovní postupy 
nebo manuály, u kterých musí potvrdit přečtení, srozumění nebo seznámení.
  - Každý zaměstnanec pak vidí všechny dokumenty, směrnice, pracovní postupy 
nebo manuály, které již potvrdil
- Provozní deníky nemovitostí
  - Ke každé budově, místnosti nebo jiné nemovitosti vedení záznamů o 
provedené údržbě nebo jiných aktivitách
  - Evidence budov, areálů, nebytových prostor a nemovitostí v přehledné 
struktuře včetně možnosti evidence vnitřního vybavení (nábytek, zařízení, 
technologie, přístroje). Popisné údaje, technické parametry i veškerou 
dokumentaci k budovám.
  - Revizi kotlů, spalinových cest, elektroměrů, jističů, výtahu, hasicích přístrojů 
nebo dalších zařízení.
  - Hlášení závad na budovách, majetku a vybavení.
  - Evidence nájemních či podnájemních smluv.
- Rezervace budov a společenských/reprezentačních místností
  - Seznam zasedacích místností a sálů (vč. kapacity).
  - Rezervační systém zasedacích místností a společenských sálů.
- Správa a rezervace služebních vozidel
  - Provozní karty vozidel.
  - Rezervační systém vozidel.
  - Plán údržby a pravidelných technických kontrol vozidel.
- Plán údržby pro vybavení, zařízení a přístroje
  - Plán údržby, revizí nebo kontrol k plánování pravidelné údržby majetku.
  - Ročnímu plán revizí.
  - Ke každému stroji, přístroji nebo zařízení vedení kompletní dokumentace dle 
  zákon 250/2021 Sb.
- Uživatelská struktura účtů
  - Přihlašovací údaje
  - Heslo
  - Uživatelské jméno
  - Pracovní pozice a uživatelská oprávnění
  - Datum vytvoření účtu
  - Logtype/náhled/avatar
# Funkcionality
- Obsah hlavní stránky
  - Zobrazení oblastí a základních údajů o obsahu
  - Zobrazení přihlašovacího okna
- Personalistika
  - Seznam kategorií
  - Organizační struktura úřadu
  - Osobní karty zaměstnanců
  - Souhrny (absolvovaná školení, kurzy, plán vzdělávání)
  - Evidence DPP a DPČ
  - Automatický proces při nástupu/odchodu zaměstnance (s úkolovníkem)
  - Evidence uchazečů o zaměstnání (výběrová řízení – postupy a archiv)
- Přehled interních směrnic a předpisů
  - Archiv interních směrnic a nařízení.
  - Každý zaměstnanec pak vidí všechny dokumenty, směrnice, pracovní postupy 
nebo manuály určené pro něj. U nich musí potvrdit přečtení, srozumění nebo 
seznámení.
- Přehled nemovité infrastruktury
  - Základní karty nemovité infrastruktury
  - Informace o pronájmech – smlouvy, hlídání ukončení platnosti nájemních 
smluv
  - Aktualizace stavu revizí – emailová notifikace ukončení platnosti revize
- Rezervační systémy pro budovy/místnosti a služební vozidla
  - Zobrazení kalendáře a výběr pro zadání rezervace
- Správa uživatelských účtů
  - Založení účtu – tajemník
  - Nastavení přístupových oprávnění do jednotlivých oblastí podle pracovního 
zařazení (viz. Organizační struktura)
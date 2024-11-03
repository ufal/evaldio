# Uživatelská příručka

Základní funkce databáze zahrnuje prohlížení záznamů s různymi způsoby jejich zobrazení, filtrování záznamů přes různe kategorie a komplexní vyhledávaní v obsahu databáze.
Databáze umožňuje korpus stáhnout vcelku i po vybraných záznamech.

## Prohlížení záznamů
Po vstupu do korpusu se v přehledné tabulce zobrazí všechny záznamy (tj. soubory transkriptů), které jsou v databázi uloženy.
Pro každý soubor s transkriptem, tabulka kromě názvu souboru zobrazuje v dalších sloupcech úroveň a identifikátor zkoušky, čislo úlohy, zdroj předběžné anotace, kód anotátora a jestli je přepis pro danou nahrávku kanonický.
Soubory v tabulce je možné setřídit podle hodnot vybraného sloupce.
Záznamy v tabulce je možné i filtrovat na základě libovolného podřetězce v jméně souboru po zadání tohoto podřetězce do textového pole "Search:" vpravo nad tabulkou.
Kliknutím na konkrétní soubor se tento soubor zobrazí.

## Zobrazení souboru
Umožňuje prohlížet přepisy jednotlivých replik spolu s anotací a metadaty a poslouchat příslušné zvukové nahrávky.
Charakter zobrazených informací se liší od zvoleného režimu zobrazení, mezi kterými lze přepínat v dolní části stránky pod samotným přepisem.

### Režim Text view
Základní režim zobrazení, který se objeví po otevření souboru.
V horní části obrazovky se zobrazuje hlavička s názvem přepisu a několika zvolenými metadaty.
V spodní části se zobrazuje samotný přepis po replikách.
Každá replika je uvozena označením mluvčího (EXAM_1 pro zkoušejícího a CAND_1 pro kandidáta).

Tento režim umožňuje zobrazit automatickou morfologickou anotaci a lemmatizaci.
Pro konkrétní token se tato anotace kontextově zobrazi po najetí kurzorem nad daný token.
Je však možné zobrazit vybraný atribut i pro všechny tokeny v přepisu.
Pro tento účel slouží ovládací prvky nahoře pod hlavičkou, které obsahují naseldující tlačítka:
- PoS: Zobrazí slovní druhy.
- Tag: Ukáže morfologické tagy.
- Features: Poskytne podrobné morfologické informace.
- Lemma: Zobrazí základní tvary slov.

### Režim Waveform view
V horní části obrazovky se zobrazí rozšířený ovládací prvek pro přehrávání nahrávky, který ukazuje i graf signálu (tzv. waveform).
Pod ním se zobrazují přepisy jednotlivých replik.
Kliknutím na repliku se zvolená replika přehraje.

### Režim Dependencies
Zobrazuje syntaktickou anotaci.
Kliknutím na konkrétní repliku se zobrazí automaticky vytvořený závislostní strom s možností zobrazení detailů pomocí myši.
Napravo nahoře od stromu se nachází tlačítko ≡ pro další možnosti zobrazení stromu.
Je tak možné uzly uspořádat podle slovosledu, zobrazit interpunkci nebo obrázek stromu uložit ve formátu SVG.

## Filtrování záznamů přes kategorie
Po kliknutí na tlačítko _Kategorie_ v levém hlavním menu je možné filtrovat přepisy na základě hodnot jednotlivých kategorií.
Je tak možné si např. zobrazit seznam jenom kanonických přepisů nebo přepisů od konkrétní anotátora. 

## Vyhledávání
Vyhledávání v korpusu lze provádět na stránce, která se zobrazí po klinutí na tlačítko _Hledat_ v levém hlavním menu.
Stránka umožňuje zadávat dotazy ve formátu CQL (Corpus Query Language). Např.

> `[upos = "NUM.*"] [lemma = "otázka"]`
>
> pro nalezení tvarů slova _otázka_, jimž předchází číslovka
    
Query builder: Umožňuje vyhledávat podle slovních druhů, lemmat nebo konkrétních slovních tvarů či jejich částí.

V základním nastavení vyhledáváme v celém korpusu, který může obsahovat k jedné nahrávce vícečetné přepisy. Chcete-li vyhledávat pouze v části korpusu s jedním přepisem ke každé nahrávce, je třeba hledání omezit na tzv. kanonický korpus. 

    Příklad dotazu pro kanonický korpus: [lemma = "situace"] :: match.text_canonical = "1" vyhledává lemma _situace_ v kanonickém korpusu.


## Stahování
Celý korpus, či jeho části, je možné stáhnout ve formátu XML pro offline práci a podrobnější analýzu.


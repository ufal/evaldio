# Uživatelská příručka

Základní funkce databáze zahrnuje prohlížení záznamů s různymi způsoby jejich zobrazení, filtrování záznamů přes různe kategorie a komplexní vyhledávaní v obsahu databáze.
Databáze umožňuje korpus stáhnout vcelku i po vybraných záznamech.

## Prohlížení záznamů
Umožňuje prohlížet přepisy jednotlivých replik, poslech příslušných zvukových nahrávek a jejich vizualizaci (Waveform view).

**Zobrazení záznamů:** 

Po kliknutí na _Zobraz položky_ se objeví seznam souborů. Kliknutím na konkrétní soubor se tento soubor otevře v režimu **Waveform view**, v němž je možné přehrávat jednotlivé repliky (kliknutím na repliku). Pro přepnutí do **Text view** klikněte na tlačítko v dolní části stránky. Tento režim umožňuje zobrazit automatickou morfologickou anotaci a lemmatizaci. Tlačítka pro zobrazení těchto anotací se nacházejí nahoře a obsahují:

PoS: Zobrazí slovní druhy.
    
Tag: Ukáže morfologické tagy.
    
Features: Poskytne podrobné morfologické informace.
    
Lemma: Zobrazí základní tvary slov.

Každá replika obsahuje časovou značku a označení mluvčího (EXAM_1 pro zkoušejícího a CAND_1 pro kandidáta).

**Zobrazení syntaktické anotace:** Klikněte na tlačítko _Dependencies_ v dolní části stránky. Kliknutím na repliky se zobrazí automaticky vytvořené závislostní stromy s možností zobrazení detailů pomocí myši.

## Filtrování záznamů


## Vyhledávání
Vyhledávání v korpusu lze provádět pomocí tlačítka _Hledat_, které umožňuje zadávat dotazy ve formátu CQL (Corpus Query Language).

    Příklad dotazu: [upos = "NUM.*"] [lemma = "otázka"] hledá tvary slova _otázka_, jimž předchází číslovka.
    
Query builder: Umožňuje vyhledávat podle slovních druhů, lemmat nebo konkrétních slovních tvarů či jejich částí.

V základním nastavení vyhledáváme v celém korpusu, který může obsahovat k jedné nahrávce vícečetné přepisy. Chcete-li vyhledávat pouze v části korpusu s jedním přepisem ke každé nahrávce, je třeba hledání omezit na tzv. kanonický korpus. 

    Příklad dotazu pro kanonický korpus: [lemma = "situace"] :: match.text_canonical = "1" vyhledává lemma _situace_ v kanonickém korpusu.


## Stahování
Celý korpus, či jeho části, je možné stáhnout ve formátu XML pro offline práci a podrobnější analýzu.


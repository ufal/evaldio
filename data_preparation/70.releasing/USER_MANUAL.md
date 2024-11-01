# Uživatelská příručka

## Databáze mluvených projevů v češtině jako cizím jazyce (trvalý pobyt v ČR)


## Úvod

Databáze byla vytvořena v Ústavu formální a aplikované lingvistiky Matematicko-fyzikální fakulty Univerzity Karlovy za účelem podpory výuky, výzkumu a hodnocení jazykové kompetence nerodilých mluvčích češtiny, kteří usilují o trvalý pobyt v České republice. Cílem je poskytnout strukturovaný a snadno přístupný zdroj autentických mluvených dat pro lingvisty, pedagogy, studenty, veřejnost a vědeckou komunitu. Audionahrávky pro databázi poskytl [Ústav jazykové a odborné přípravy Univerzity Karlovy](https://ujop.cuni.cz/) (ujop.cuni.cz).

## Základní funkce databáze

**1. Prohlížení záznamů:** Databáze umožňuje prohlížet přepisy replik a poslech zvukových nahrávek.

**Zobrazení záznamů:** 

Po kliknutí na _zobraz položky_ se objeví seznam souborů. Kliknutím na konkrétní soubor se tento soubor otevře v režimu **waveform view**, v němž je možné přehrávat jednotlivé repliky. Pro přepnutí do **text view** klikněte na tlačítko v dolní části stránky. Tento režim umožňuje zobrazit automatickou morfologickou anotaci a lemmatizaci. Tlačítka pro zobrazení těchto anotací se nacházejí nahoře a obsahují:

    PoS: Zobrazí slovní druhy.
    
    Tag: Ukáže morfologické tagy.
    
    Features: Poskytne podrobné morfologické informace.
    
    Lemma: Zobrazí základní tvary slov.


Každá replika obsahuje časovou značku a označení mluvčího (EXAM_1 pro zkoušejícího a CAND_1 pro kandidáta).

**Zobrazení syntaktické anotace:** Klikněte na tlačítko _dependencies_ v dolní části stránky. Kliknutím na repliky se zobrazí automaticky vytvořené závislostní stromy s možností zobrazení detailů pomocí myši.


**2. Vyhledávání:** Vyhledávání v korpusu lze provádět pomocí tlačítka _hledat_, které umožňuje zadávat dotazy ve formátu CQL (Corpus Query Language).

    Příklad dotazu: [upos = "NUM.*"] [lemma = "otázka"] hledá tvary slova _otázka_, jimž předchází číslovka.
    
    Query builder: Umožňuje vyhledávat podle slovních druhů, lemmat nebo konkrétních slovních tvarů či jejich částí.

V základním nastavení vyhledáváme v celém korpusu, který může obsahovat k jedné nahrávce vícečetné přepisy. Chcete-li vyhledávat pouze v části korpusu s jedním přepisem ke každé nahrávce, je třeba hledání omezit na tzv. kanonický korpus. 

    Příklad pro kanonický korpus: [lemma = "situace"] :: match.text_canonical = "1" vyhledává lemma _situace_ v kanonickém korpusu.


**3. Stahování:** Celý korpus, či jeho části, je možné stáhnout ve formátu XML pro offline práci a podrobnější analýzu.


## Financování:

Vznik databáze byl financován z prostředků Programu na podporu aplikovaného výzkumu v oblasti národní a kulturní identity na léta 2023 až 2030 (NAKI III) Ministerstva kultury ČR v rámci projektu Automatické hodnocení mluveného projevu v češtině (DH23P03OVV037).

## Jak citovat:

Rysová Kateřina, Novák Michal, Rysová Magdaléna, Polák Peter, Bojar Ondřej: Databáze mluvených projevů v češtině jako cizím jazyce (trvalý pobyt v ČR). Ústav formální a aplikované lingvistiky MFF UK, Praha 2024. Dostupná z WWW [https://lindat.mff.cuni.cz/services/teitok-live/evaldio/cs/index.php?action=db_residency](https://lindat.mff.cuni.cz/services/teitok-live/evaldio/cs/index.php?action=db_residency).

Rysová Kateřina, Novák Michal, Rysová Magdaléna, Polák Peter, Bojar Ondřej: Czech as Second Language Speech Dataset (Permanent Residency Applicants). Institute of Formal and Applied Linguistics MFF UK, Prague 2024. Available from WWW [https://lindat.mff.cuni.cz/services/teitok-live/evaldio/en/index.php?action=db_residency](https://lindat.mff.cuni.cz/services/teitok-live/evaldio/en/index.php?action=db_residency).

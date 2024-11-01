# Technická dokumentace
**Databáze mluvených projevů v češtině jako cizím jazyce (trvalý pobyt v ČR)**

========

Databáze je integrována do systému TEITOK (CITE).

## TEITOK

TEITOK je framework pro vytváření, správu a zveřejňování anotovaných korpusů. 
Jeho webové rozhraní je implementováno v kombinaci jazyků PHP a JavaScript.

### Příprava a uložení dat
Korpus v TEITOKu sestává z kolekce souborů ve formátu TEITOK, které obsahují veškeré přepisy a anotace včetně metadat. 
Kromě toho obsahuje i nahrávky ve formátu MP3, které jsou provázány s jednotlivými soubory s přepisy. 
Formát TEITOK je XML formát, který plně odpovídá standardu Text Encoding Initiative (TEI, CITE), s mírně odlišným přístupem k tokenizaci.

### Struktura souborů TEITOK

#### Hlavička s metadaty `<teiHeader>`
1. **`<fileDesc>`** – Popis souboru
    - **`<titleStmt>`**: Obsahuje název souboru a informace o autorech a anotátorech.
    - **`<editionStmt>`**: Obsahuje číslo verze.
    - **`<publicationStmt>`**: Publikační detaily, jako je vydavatel, datum vydání a licence.
    - **`<sourceDesc>`**: Popis zdrojové nahrávky a odkaz na ni.

2. **`<encodingDesc>`** – Popis kódování
    - **`<projectDesc>`**: Stručný popis projektu, v rámci něhož data vznikla.
    - **`<annotationDecl>`**: Detaily o jednotlivých krocích anotace (primární, revize, lingvistická anotace).

3. **`<profileDesc>`** – Profil textu
    - **`<langUsage>`**: Použitý jazyk (čeština).
    - **`<textClass>`**: Metadata dokumentu:
       - `database`: Název databáze.
       - `exam-id`: Identifikátor zkoušky.
       - `cefr-level`: Úroveň podle SERR. Tato databáze obsahuje výhradně nahrávky zkoušek úrovně A2.
       - `task-number`: Číslo úlohy.
       - `preannot-source`: Zdroj předběžné anotace.
       - `annotator`: Kód anotátora.
       - `canonical`: Hodnota `1` značí kanonický přepis.

#### Hlavní obsah `<text>`
Sekce `<text>` obsahuje jednotlivé úseky mluveného projevu strukturované pomocí elementů `<u>`:
- **`<u>`**: Každý `<u>` reprezentuje úsek projevu projevu a má atributy:
   - `start` a `end`: Počáteční a koncový čas v sekundách.
   - `who`: Mluvčí (např. "EXAM_1" pro zkoušejícího a "CAND_1" pro kandidáta).
- **`<s>`**: Každá věta je označena elementem `<s>`.
- **`<tok>`**: Elementy tokenů, jejichž atributy popisují lemma, slovní druh, morfologické rysy a syntaktický vztah.
- **`<anon/>`**: Anonymizovaný úsek nahrávky.
- **`<gap reason="unintelligible"/>**: Nesrozumitelný úsek nahrávky.

### Příprava souborů TEITOK
Příprava souborů TEITOK probíhala v několika fázích:

1. **Předběžná anotace**. Za účelem časové a finanční efektivity jsme porovnávali přímou ruční anotaci s post-editací výstupů systémů na automatické rozpoznávání řeči. Toto je rozlíšeno pomocí atributu `preannot-source`, jehož hodnota je jedna z nasledujících:
    - `from_scratch`: Kompletně manuální anotace, t.j. předběžná anotace je prázdná.
    - `from_whisperX`: Předběžná anotace získaná pomocí systému WhisperX (CITE).
    - `from_mixed`: Předběžná anotace získaná náhodným kombinovaním výstupů 4 systémů na úrovni replik.
Když není předběžná anotace prázdná, převedeme ji do základní verze formátu TEITOK.
Na konci této fáze tak obsahuje přepisy rozdělené do replik (elementy `<u>`), přiřazení mluvčích k replikám (atribut `who`) a časové zarovnání s nahrávkou (atributy `start` a `end`).
2. **Manuální anotace**. Po nahrání súborů ji vykonávali zaškolené anotátorky vo webovém prostředí TEITOK. Manuální anotací vznikali nebo byli opraveny přepisy, přiřazení mluvčích k replikám a časové zarovnání s nahrávkou.
3. **Revize**. Ruční kontrola manuálních anotací spoluautorkou databáze.
4. **Normalizace**. Automatická úprava přepisů, které se můžou po manuálním zpracování v prostředí TEITOK mírně lišit v techických detailech. Konkrétně v tomto kroce odstra§ujeme odchylky v jménech mluvčích, třídime repliky podle jejich počátečního času a přidělujeme replikám nové sekvenční ID.
4. **Rozdělení na cvičení a selekce**. Poskytovatel nahrávek (ÚJOP UK) povolil k zveřejnění jenom vybraná cvičení. Ty jsme museli z nahrávek a jejich přepisů vystřihnout a v přepisech upravit časové značky, aby se zachovalo zarovnání replik v přepisu s nahrávkou.
5. **Lingvistická anotace**. Až do tohoto momentu nejsou repliky v přepisech nijak dál strukturovány. V této fázi text rozdělíme na věty (element `<s>`) a věty na tokeny (elemety `<tok>`). Na úrovni tokenů jsou přepisy následně automaticky lingvisticky anotovány. Konkrétně je každému tokenu přirazeno lemma (atribut `lemma`), jazykovo specificá morfologická značka (atribut `xpos`), slovný druh a morfologické vlastnosti dle kategorizace projektu [Universal Dependencies](https://universaldependencies.org/) (atributy `upos` a `feats`), odkaz na ID rodiče dle pravidel závislostní syntaxe (atribut `head`) a typ závislosti tokenu ve vztahu k jeho rodiči (atribut `deprel`). Pro lingvistickou anotaci včetně tokenizace jsme použili nástroj UDPipe 2 (CITE), konkrétně model `czech-pdt-ud-2.12-230717` pro češtinu.I když tokenizaci a automatickou lingvistickou anotaci je možné přidat přímo v prostředí TEITOK, my jsme tak dělali samostatně. Metoda tokenizace v prostředí TEITOK se totiž liší od tokenizace, která je optimální pro UDPipe, což následně způsobovalo chyby v spojení těchot dvou kroků.
6. **Doplnění TEI hlavičky**. V závěru na základě všech dostupných metadat doplníme hlavičku tak, aby odpovídala standardům TEI.

Všechy nástroje a skripty (převažně v jazycích Python 3 a BASH) jsou k dispozici ve [verejném repozitáři projektu](https://github.com/ufal/evaldio) v adresáři `data_preparation`.



### Dotazování, vyhledávání a filtrování
Rychlé dotazování, vyhledávaní a filtrace jsou umožněny integrovaným procesorem dotazů CQP.
CQP je klíčová komponenta sady nástrojů IMS Open Corpus Workbench (CWB).
Korpusy ve formátu XML převádí do binární podoby a efektivně je indexuje.
Na dotazování v indexovaných korpusech slouží jazyk CQL, který je roky zavedeným standardem v korpusové lingvistice.
Pro zjednodušení formulace dotazů TEITOK nabízí i tzv. Query builder, kde může uživatel specifikovat svůj dotaz vyplněním položek formuláře.
Výsledek dotazu vrácen z CQP je následně zpracován pomocí TEITOKu a v přehledné formě je zobrazen užívateli.

Databáze je dostupná na platformě LINDAT/CLARIAH-CZ.




========


Databáze mluvených projevů nerodilých mluvčích češtiny zaměřená na jazykovou úroveň A2 (podle CEFR), požadovanou pro udělení trvalého pobytu v České republice, je výsledkem projektu realizovaného v Ústavu formální a aplikované lingvistiky Matematicko-fyzikální fakulty Univerzity Karlovy. Jazykový korpus je zveřejněn jako specializovaná veřejná databáze a je volně dostupný široké veřejnosti, vědecké komunitě, pedagogům a studentům.

## Umístění korpusu

Korpus je přístupný na platformě LINDAT/CLARIAH-CZ, která slouží jako repozitář jazykových dat. Data byla zpracována s využitím platformy TEITOK [XX]. 


## Obsah korpusu

Korpus obsahuje nahrávky mluvených projevů v celkovém rozsahu XX minut. Nahrávky zaznamenávají ústní část zkoušky CCE (Certifikovaná zkouška z češtiny pro cizince; http://ujop.cuni.cz/cce) na úrovni A2. Nahrávky zahrnují dialogy mezi zkoušejícím (rodilým mluvčím) a kandidátem zkoušky (nerodilým mluvčím). 

Nahrávky byly anonymizovány v souladu s požadavky Ústavu jazykové a odborné přípravy Univerzity Karlovy (ujop.cuni.cz), který audio nahrávky pro korpus poskytl. Někteří anotátoři z opatrnosti anonymizovali i údaje, které anonymizovány být nemusely (např. smyšlená jména osob). 

Každá nahrávka je opatřena manuálně vytvořeným přepisem. Přepisy zároveň obsahují i ručně přiřazené časové značky, které spojují repliky s konkrétními úseky nahrávky. Součástí anotace je také manuální označení jednotlivých mluvčích.

K některým nahrávkám je připojeno více přepisů od různých anotátorů, což umožňuje srovnání různých přepisů téže nahrávky a vyhodnocení míry shody při převodu mluvené řeči do psaného textu. 


## Struktura údajů

**Repliky:** Manuální přepis mluveného projevu, členěný na repliky, s možností přehrát konkrétní úseky nahrávky.

**Mluvčí:** Manuální označení: EXAM_1 (zkoušející), CAND_1 (kandidát).

**Anotace:** Každý slovní tvar je opatřen automatickou anotaci slovních druhů a morfologickými značkami. Korpus byl také automaticky lemmatizován a obsahuje syntaktickou anotaci (závislostní stromy).

**Waveform view:** Vizualizace zvukového signálu, s možností přehrát repliky včetně časových značek.

Pro účely vyhledávaní a filtrování se vstupní soubory a jejich obsah indexuje do binárního formátu [Corpus Workbench](https://cwb.sourceforge.io). 


## Práce s daty

**Prohlížení (Browse):** Uživatelé mohou prohlížet jednotlivé záznamy, včetně přepisů, morfologických anotací, lemmatizace a syntaktických závislostí.

**Vyhledávání (Search):** Uživatelé mohou zadávat dotazy ve formátu CQL (Corpus WorkBench Query Language) pro vyhledávání specifických slovních tvarů, lemmat a sekvencí slov.

**Export:** Výsledky dotazů je možné stáhnout v XML formátu nebo prohlížet v kontextu.


**Licence:**

Korpus je zveřejněn pod licencí CC BY-NC-SA 4.0.


**Financování:**

Vznik databáze byl financován z prostředků Programu na podporu aplikovaného výzkumu v oblasti národní a kulturní identity na léta 2023 až 2030 (NAKI III) Ministerstva kultury ČR v rámci projektu _Automatické hodnocení mluveného projevu v češtině_ (DH23P03OVV037).


**Poděkování:**

Autoři databáze srdečně děkují PhDr. Pavlovi Pečenému, Ph.D., z Ústavu jazykové a odborné přípravy Univerzity Karlovy za poskytnutí audio dat a za jejich finální kontrolu.


**Jak citovat:**

Rysová Kateřina, Novák Michal, Rysová Magdaléna, Polák Peter, Bojar Ondřej: Databáze mluvených projevů v češtině jako cizím jazyce (trvalý pobyt v ČR). Ústav formální a aplikované lingvistiky MFF UK, Praha 2024. Dostupná z WWW [https://lindat.mff.cuni.cz/services/teitok-live/evaldio/cs/index.php?action=db_residency](https://lindat.mff.cuni.cz/services/teitok-live/evaldio/cs/index.php?action=db_residency).

Rysová Kateřina, Novák Michal, Rysová Magdaléna, Polák Peter, Bojar Ondřej: Czech as Second Language Speech Dataset (Permanent Residency Applicants). Institute of Formal and Applied Linguistics MFF UK, Prague 2024. Available from WWW [https://lindat.mff.cuni.cz/services/teitok-live/evaldio/en/index.php?action=db_residency](https://lindat.mff.cuni.cz/services/teitok-live/evaldio/en/index.php?action=db_residency).


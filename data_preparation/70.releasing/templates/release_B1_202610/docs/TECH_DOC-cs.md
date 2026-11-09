# Databáze mluvených projevů v češtině jako cizím jazyce (státní občanství v ČR): technická dokumentace

## a) Základní údaje

**Název výsledku:** Databáze mluvených projevů v češtině jako cizím jazyce (státní občanství v ČR)

**Typ výsledku:** S – specializovaná veřejná databáze

**Vlastník výsledku:** Univerzita Karlova

**Tvůrce databáze:** Ústav formální a aplikované lingvistiky, Matematicko-fyzikální fakulta, Univerzita Karlova.

**Uživatelé databáze:** Pedagogové a studenti, vědecká a odborná komunita, instituce zabývající se výukou češtiny jako cizího jazyka nebo zajišťující zkoušky z češtiny jako cizího jazyka a další vzdělávací instituce, široká veřejnost, zejména zájemci o češtinu jako cizí jazyk.

**Umístění databáze:** Databáze je integrována do systému [TEITOK](http://teitok.corpuswiki.org/), který je provozován na platformě [LINDAT/CLARIAH-CZ](https://lindat.cz/).

**Veřejná adresa databáze:** <http://hdl.handle.net/11346/H4WT>

## b) Cíl výsledku

Cílem databáze je zpřístupnit veřejnosti autentické mluvené projevy nerodilých mluvčích češtiny na jazykové úrovni B1 podle Společného evropského referenčního rámce pro jazyky (SERR), která je požadována pro udělení státního občanství v České republice. Databáze obsahuje nahrávky zachycující ústní část [Certifikované zkoušky z češtiny pro cizince](https://ujop.cuni.cz/cce) na úrovni B1. Nahrávky zahrnují dialogy mezi zkoušejícím (rodilým mluvčím) a kandidátem zkoušky (nerodilým mluvčím). Nahrávky jsou opatřeny manuálními přepisy a bohatou lingvistickou anotací.

Databáze vznikla v rámci projektu realizovaného v Ústavu formální a aplikované lingvistiky Matematicko-fyzikální fakulty Univerzity Karlovy. Vytvoření databáze navazuje na výzkum realizovaný v rámci projektu. Při její přípravě byly provedeny zejména následující výzkumné a datově analytické činnosti: sběr audionahrávek, jejich anonymizace, výzkum mluvených projevů nerodilých mluvčích češtiny v oblasti lingvistiky, výzkum týkající se metodiky přepisu získaných projevů do textové podoby, tvorba a revize manuálních přepisů, identifikace jednotlivých mluvčích (zkoušející vs. kandidát zkoušky), časové zarovnání přepisů s nahrávkami, automatická lingvistická anotace a příprava strukturovaných dat pro zveřejnění v prostředí TEITOK.

Rozsah prací na výsledku: 0,8 FTE

**Další záměr příjemce s databází:** Databáze je zpřístupněna jako specializovaná veřejná databáze a je volně a bezplatně dostupná široké veřejnosti. Databáze je zároveň zamýšlena jako datový podklad pro naprogramování softwaru na automatické hodnocení mluvených projevů nerodilých mluvčích češtiny.

## c) Architektura údajů

### Základní popis databáze a rozsah dat

Databáze obsahuje audionahrávky ústní části Certifikované zkoušky z češtiny pro cizince na úrovni B1 a jejich manuální přepisy ve formátu TEITOK (XML). Jednotlivé soubory TEITOK jsou propojeny s odpovídajícími audionahrávkami ve formátu MP3.

Poskytovatel nahrávek, [Ústav jazykové a odborné přípravy Univerzity Karlovy (ÚJOP UK)](https://ujop.cuni.cz/UJOP-1.html), povolil ke zveřejnění pouze vybrané úlohy. Databáze proto obsahuje pouze ty části nahrávek, jejichž zveřejnění bylo poskytovatelem povoleno.

Jednotlivé záznamy obsahují odpovídající audionahrávku a její manuální přepis. Přepisy zachycují jednotlivé repliky, identifikaci mluvčích (zkoušející vs. kandidát zkoušky) a časové zarovnání s nahrávkou. Dále obsahují automatickou lingvistickou anotaci.

#### Rozsah databáze

Základní statistiky databáze jsou shrnuty v následujícím přehledu:

- Počet audionahrávek: 65
- Celková délka nahrávek v databázi: 4h 51m 48s
- Počet souborů s manuálními přepisy: 65
- Počet tokenů: 29 572
- Počet replik: 3 348
- Jazyk: čeština
- Jazyková úroveň: B1 podle SERR

### Struktura databáze

Databáze se skládá z následujících entit a vazeb mezi nimi:

1. **Recording (Nahrávka)** – Představuje původní zvukový záznam. Ke každé nahrávce z databáze existuje její manuální přepis.
2. **Document (Dokument)** – Odpovídá jednotlivému přepisu ve formátu TEITOK (XML). Obsahuje metadata o zkoušce a jejím přepisu (úroveň CEFR, ID zkoušky, číslo úlohy, kód anotátora přepisu atd.) a je spojen s nahrávkou.
3. **Utterance (Replika)** – Jednotlivé repliky uvnitř dokumentu. Obsahují informaci o mluvčím (`who`) a časových značkách (`start`, `end`).
4. **Token** – Základní jednotka textu (slovní tvar). Každý token je specifikován svou textovou realizací (`form`), lemmatem (`lemma`), slovním druhem (`upos`, `xpos`), morfologickými rysy (`feats`) a syntaktickou závislostí (`deprel`).
    - *Rekurzivní vazba:* Token může odkazovat sám na sebe (`head`), což tvoří stromovou strukturu závislostního syntaktického popisu.

#### Grafické znázornění struktury databáze

Následující E-R diagram blíže znázorňuje výše popsanou strukturu databáze:

![E-R diagram struktury databáze](media/database-er-diagram.png)

### Struktura souborů TEITOK

Databáze je tvořena soubory, které obsahují přepisy ve formátu TEITOK. TEITOK je formát XML, který odpovídá standardu [Text Encoding Initiative (TEI)](https://www.tei-c.org/), avšak s mírně odlišným přístupem k tokenizaci. Struktura souborů TEITOK v naší databázi je následující:

#### Hlavička s metadaty `<teiHeader>`

Hlavička souboru TEITOK se skládá z následujících částí:

1. `<fileDesc>`: Popis souboru
    - `<titleStmt>`: Obsahuje název souboru a informace o autorech a anotátorech.
    - `<editionStmt>`: Obsahuje číslo verze.
    - `<publicationStmt>`: Publikační detaily, jako je vydavatel, datum vydání a licence.
    - `<sourceDesc>`: Popis zdrojové nahrávky a odkaz na ni.
2. `<encodingDesc>`: Popis kódování
    - `<projectDesc>`: Stručný popis projektu, v jehož rámci data vznikla.
    - `<annotationDecl>`: Detaily o jednotlivých krocích přepisu a anotace (primární transkripce, revize, lingvistická anotace).
3. `<profileDesc>`: Profil textu
    - `<langUsage>`: Použitý jazyk (čeština).
    - `<textClass>`: Metadata dokumentu:
      - `database`: Název databáze.
      - `exam-id`: Identifikátor zkoušky.
      - `cefr-level`: Úroveň podle SERR. Tato databáze obsahuje výhradně nahrávky zkoušek úrovně B1.
      - `task-number`: Číslo úlohy.
      - `preannot-source`: Zdroj předběžné transkripce. Jelikož všechny přepisy v této databázi vznikly kompletně manuálně, hodnota je vždy `from_scratch`.
      - `annotator`: Kód anotátora.
      - `canonical`: Hodnota 1 značí kanonický přepis. Jelikož databáze neobsahuje duplicitní přepisy, každý přepis je kanonický.

#### Hlavní obsah `<text>`

Sekce `<text>` obsahuje jednotlivé úseky mluveného projevu strukturované pomocí elementů `<u>`:

- `<u>`: Element reprezentuje úsek projevu a má atributy:
  - `start` a `end`: Počáteční a koncový čas v sekundách.
  - `who`: Mluvčí (např. EXAM_1 pro zkoušejícího a CAND_1 pro kandidáta).
- `<s>`: Element ohraničuje větu.
- `<tok>`: Elementy tokenů, jejichž atributy popisují lemma, slovní druh, morfologické rysy a syntaktický vztah.
- `<anon/>`: Anonymizovaný úsek nahrávky.
- `<gap reason="unintelligible"/>`: Nesrozumitelný úsek nahrávky.

#### Anotace tokenu v elementu `<tok>`

Element `<tok>` reprezentuje token, který většinou odpovídá slovnímu tvaru. Každý token je dále popsán následujícími atributy, které odpovídají standardům z projektu [Universal Dependencies](https://universaldependencies.org/guidelines.html):

- `ord`: pořadové číslo tokenu ve větě
- `lemma`: základní tvar slova
- `upos`: značka univerzálního slovního druhu
- `xpos`: originální morfologická značka
- `feats`: morfologické vlastnosti
- `head`: odkaz na rodičovský token
- `deprel`: typ závislostního syntaktického vztahu k rodiči

### Úplnost záznamů

Jednotlivé záznamy obsahují odpovídající audionahrávku a její manuální přepis. Přepisy obsahují identifikaci mluvčích (zkoušející vs. kandidát zkoušky) a časové značky jednotlivých replik. Součástí přepisů je rovněž automatická lingvistická anotace. Uvedené údaje obsahují všechny záznamy v databázi.

Rozsah zveřejněných nahrávek je dán souhlasem poskytovatele dat, který povolil zveřejnění pouze vybraných úloh. Zveřejněné nahrávky proto nemusí obsahovat původní záznam celého průběhu zkoušky.

## d) Práce s údaji (třídění, filtrování, vyhledávání atd.)

Databáze umožňuje následující funkce:

- Prohlížení audionahrávek a jejich manuálních přepisů.
- Zobrazení jednotlivých replik a identifikace mluvčích.
- Přehrávání nahrávek a synchronizované prohlížení přepisů.
- Zobrazení časových značek začátku a konce jednotlivých replik.
- Zobrazení automatické lingvistické anotace jednotlivých tokenů:
  - slovní druh (PoS),
  - morfologický tag,
  - podrobné morfologické příznaky (features),
  - lemma (základní tvar slova).
- Zobrazení automatické syntaktické analýzy ve formě závislostního stromu.
- Vyhledávání pomocí jazyka CQL.
- Sestavování vyhledávacích dotazů prostřednictvím grafického rozhraní Query Builder.
- Zobrazování výsledků vyhledávání v přehledné podobě.
- Export výsledků vyhledávání ve formátu XML.

Podrobný návod k používání jednotlivých funkcí a příklady vyhledávání jsou uvedeny v samostatné uživatelské příručce.

## e) Použité softwarové nástroje

Databáze je veřejně dostupná prostřednictvím platformy LINDAT/CLARIAH-CZ a systému TEITOK. Přístup k ní je bezplatný a nevyžaduje registraci.

Data tvořící obsah databáze jsou současně uložena v certifikovaném repozitáři LINDAT/CLARIAH-CZ, který zajišťuje jejich dlouhodobé uchovávání, pravidelné zálohování a opatření persistentním identifikátorem typu Handle. Záznamy repozitáře LINDAT/CLARIAH-CZ jsou indexovány internetovými vyhledávači (včetně Google) a související metadata jsou zpřístupněna také v katalogu CLARIN Virtual Language Observatory (VLO). Záznam lze tak nalézt běžným vyhledáváním. Datová sada odpovídající této databázi je dostupná prostřednictvím identifikátoru Handle: <http://hdl.handle.net/11234/1-6311>

Repozitář LINDAT/CLARIAH-CZ v současné době nepřiděluje persistentní identifikátory typu DOI. Z toho důvodu je záznam o databázi evidován i v Datovém Catch-all repozitáři, který však v současné době nemá plnou certifikaci. Záznam je k dispozici zde: [https://doi.org/10.48700/hftww-b2k53](https://doi.org/10.48700/hftww-b2k53)

Pro přípravu a zpracování dat, transkripcí a anotací jsme použili další nástroje, které popisujeme níže.

### TEITOK

[TEITOK](https://www.teitok.org/) je framework pro vytváření, správu a zveřejňování anotovaných korpusů. Umožňuje spravovat, prohlížet, prohledávat a zpřístupnit databázi. Jeho webové rozhraní je implementováno v kombinaci jazyků PHP a JavaScript.

Pro náš projekt, který kombinuje nahrávky mluveného projevu a jejich přepisy, je stěžejní funkcionalita prostředí TEITOK, která umožňuje [vytvářet, zobrazovat a upravovat přepisy nahrávek](http://www.teitok.org/index.php?action=help&id=wavesurfer).

K práci se samotnou nahrávkou TEITOK využívá JavaScriptovou knihovnu [WaveSurfer.js](http://wavesurfer-js.org/).

#### Uložení dat

Data korpusu jsou v prostředí TEITOK primárně uložena ve formě souborů. V tomto případě se jedná o nahrávky ve formátu MP3, hlavní části jsou však soubory ve formátu TEITOK, které obsahují všechny přepisy a anotace včetně metadat. Tyto soubory jsou navzájem provázány s odpovídajícími nahrávkami.

Kromě toho jsou data z databáze uložena v repozitáři LINDAT/CLARIAH-CZ (viz níže), který zabezpečuje spolehlivé úložiště s pravidelným zálohováním a persistentními identifikátory.

#### Dotazování, vyhledávání a filtrování

Rychlé dotazování, vyhledávání a filtrace jsou umožněny integrovaným [procesorem dotazů CQP](https://cwb.sourceforge.io/files/CQP_Manual.pdf), klíčovou komponentou sady nástrojů [IMS Open Corpus Workbench (CWB)](https://cwb.sourceforge.io/).

CQP převádí korpusy ve formátu XML do binární podoby a efektivně je indexuje.

Dotazování v indexovaných korpusech probíhá pomocí jazyka [CQL](https://www.latl.leeds.ac.uk/wp-content/uploads/sites/49/2019/07/CQL-Help-1.3.pdf), který je standardem v korpusové lingvistice.

TEITOK také nabízí Query Builder, v němž může uživatel specifikovat dotaz vyplněním formuláře. Výsledek dotazu vrácený z CQP je následně zpracován pomocí TEITOKu a zobrazen uživateli v přehledné formě. Výsledky dotazů je možné stáhnout ve formátu XML.

### Repozitář LINDAT/CLARIAH-CZ

Kromě výše uvedeného jsou data z databáze uložena v repozitáři [LINDAT/CLARIAH-CZ](https://lindat.mff.cuni.cz/repository/), který provozuje Ústav formální a aplikované lingvistiky Matematicko-fyzikální fakulty Univerzity Karlovy (ÚFAL MFF UK). Repozitář je primárně součástí velké výzkumné infrastruktury LINDAT/CLARIAH-CZ a zároveň je součástí Národní repozitářové platformy (NRP), která představuje českou implementaci iniciativy European Open Science Cloud (EOSC). Je postaven na softwaru CLARIN-DSpace, který patří mezi hlavní systémy dále vyvíjené v rámci NRP. Repozitář je rovněž součástí evropské infrastruktury CLARIN ERIC.

Celý repozitář pravidelně prochází certifikací [CoreTrustSeal](https://www.coretrustseal.org/). Certifikace vychází ze sebehodnocení, které následně posuzují nezávislí recenzenti. Součástí sebehodnocení je také popis ukládání dat, zálohování a perzistentních identifikátorů. Aktuálně platné hodnocení je dostupné [zde](http://hdl.handle.net/11234/6-CTS).

#### Uložení a zálohovaní dat

Repozitář dlouhodobě pečuje o uložené položky a využívá automatizované postupy, včetně kontrol integrity, které zajišťují neporušenost dat a úplnost metadat. Obnova po havárii je řešena vícestupňovým schématem záloh, jehož součástí je týdenní záloha na externím hierarchickém úložišti. Zálohy se provádějí automaticky na samostatné servery a hardwarová platforma i provoz služeb jsou monitorovány. Podrobnosti jsou uvedeny v dokumentu CoreTrustSeal. Zásadou repozitáře je uložené datové sady nemazat.

#### Zabezpečení perzistentních identifikátorů

Každá položka uložená v repozitáři získává perzistentní identifikátor typu Handle, registrovaný ve spolupráci s konsorciem EPIC. Handle i příslušný URL odkaz zůstávají funkční i při změně technického umístění či adresy repozitáře. V současné době LINDAT/CLARIAH-CZ nepřiděluje persistentní identifikátory typu DOI. Z toho důvodu záznam o databázi evidujeme i v Datovém Catch-all repozitáři (viz níže).

#### Indexace a vyhledávání

Repozitář LINDAT/CLARIAH-CZ je postaven na softwaru DSpace 7, který [podporuje indexaci](https://wiki.lyrasis.org/spaces/DSDOC7x/pages/104566800/Search+Engine+Optimization) obsahu webovými vyhledávači, včetně Google a Google Scholar. Repozitář zveřejňuje mapy webu ve formátu XML i HTML (`sitemap_index.xml`, `sitemap_index.html`), na které odkazuje soubor `robots.txt`. Stránka každé položky navíc obsahuje metadata ve formátu Dublin Core a značky `citation\_\*` doporučené pro Google Scholar. Veřejně dostupné položky, včetně dat popisované databáze, jsou tak vyhledávačům snadno dostupné, a to i pod perzistentním odkazem Handle.

### Datový Catch-all repozitář

Záznam o databázi je evidován i v [Datovém Catch-all repozitáři](https://datarepo.eosc.cz/), který je rovněž součástí Národní repozitářové platformy (NRP). Na rozdíl od LINDAT/CLARIAH-CZ tento repozitář přiděluje persistentní identifikátory typu DOI. Na druhou stranu tento repozitář zatím nemá plnou certifikaci.

### Příprava souborů TEITOK

Příprava souborů TEITOK probíhala v několika fázích:

1. **Manuální transkripce.** Všechny nahrávky byly transkribovány manuálně od začátku (from scratch), bez využití výstupů systémů pro automatické rozpoznávání řeči. Transkripce byly vytvářeny přímo ve formátu TEITOK, který umožňuje zachytit přepisy rozdělené do replik (elementy `<u>`), identifikaci mluvčích (atribut `who`) a časové zarovnání replik s nahrávkou (atributy `start` a `end`).

   Manuální přepisy nahrávek provedly zaškolené anotátorky spolu s jejich anonymizací v souladu s požadavky ÚJOP UK, který audionahrávky pro korpus poskytl. Některé anotátorky preventivně anonymizovaly i údaje, které anonymizovány být nemusely (např. smyšlená jména osob).

2. **Revize.** Ruční kontrola manuálních přepisů spoluautorkou databáze.
3. **Normalizace.** Automatická úprava přepisů, která odstraní odchylky ve jménech mluvčích, seřadí repliky podle počátečního času a přidělí replikám nová sekvenční ID.
4. **Rozdělení na úlohy a selekce.** ÚJOP UK povolil ke zveřejnění pouze vybrané úlohy. Ty jsme museli z nahrávek vystřihnout a upravit časové značky v přepisech, aby se zachovalo zarovnání replik v přepisu s nahrávkou. Pro stříhání nahrávek jsme použili nástroj [FFmpeg](https://www.ffmpeg.org/).
5. **Lingvistická anotace.** Až do této fáze nebyly repliky v přepisech dále strukturovány. V této fázi jsme text rozdělili na věty (elementy `<s>`) a následně věty na tokeny (elementy `<tok>`). Na úrovni tokenů jsou přepisy automaticky lingvisticky anotovány. Každému tokenu je přiděleno lemma, slovní druh, morfologické vlastnosti a syntaktické vztahy.
6. **Doplnění hlavičky TEI.** Na závěr jsme doplnili hlavičku podle všech dostupných metadat, aby odpovídala standardům TEI.

Všechny nástroje a skripty (převážně v jazycích Python 3 a BASH) jsou k dispozici ve [veřejném repozitáři projektu](https://github.com/ufal/evaldio) v adresáři `data_preparation`.

#### Lingvistická anotace

Přepisy obsahují automatickou lingvistickou anotaci zahrnující tokenizaci, lemmatizaci, morfologickou analýzu a závislostní syntaktickou analýzu.

Pro lingvistickou anotaci, včetně tokenizace, jsme použili nástroj [UDPipe 2](https://ufal.mff.cuni.cz/udpipe/2), konkrétně model `czech-pdt-ud-2.12-230717` pro češtinu.

Každému tokenu je přiděleno lemma (atribut `lemma`), jazykově specifická morfologická značka (atribut `xpos`), slovní druh a morfologické vlastnosti dle kategorizace projektu [Universal Dependencies](https://universaldependencies.org/) (atributy `upos` a `feats`). Dále je každému tokenu přiřazen odkaz na ID rodiče podle pravidel závislostní syntaxe (atribut `head`) a typ závislosti tokenu ve vztahu k jeho rodiči (atribut `deprel`).

Ačkoli je možné provádět tokenizaci a automatickou lingvistickou anotaci přímo v prostředí TEITOK, my jsme tento proces realizovali samostatně. Důvodem je, že metoda tokenizace v prostředí TEITOK se liší od té, která je optimalizována pro UDPipe, což by mohlo způsobovat chyby při spojování těchto dvou kroků.

## f) Prokázání novosti a unikátnosti specializované veřejné databáze

Databáze představuje unikátní, dosud nepublikovaný jazykový materiál – autentické audionahrávky ústních zkoušek z češtiny jako cizího jazyka na úrovni B1, jejich manuální přepisy, identifikaci jednotlivých mluvčích (zkoušející vs. kandidát zkoušky), časové zarovnání replik s nahrávkami a automatické lingvistické anotace.

Vytvoření databáze předcházel výzkum zaměřený na sběr a zpracování autentických mluvených projevů, porovnávání metod přepisu mluvené řeči, manuální anotaci a revizi přepisů a také na následnou automatickou lingvistickou anotaci.

Specifickým přínosem databáze je propojení zvukové podoby mluvených projevů s jejich strukturovaným textovým přepisem a podrobnou lingvistickou anotací. Časové značky jednotlivých replik umožňují přesné propojení textu s odpovídající částí nahrávky. Automatická morfologická a syntaktická anotace usnadňuje vyhledávání jazykových jevů a využití databáze při výuce a studiu češtiny jako cizího jazyka.

## Jak citovat

Rysová Kateřina, Novák Michal, Rysová Magdaléna, Polák Peter, Bojar Ondřej: *Databáze mluvených projevů v češtině jako cizím jazyce (státní občanství v ČR)*. Ústav formální a aplikované lingvistiky MFF UK, Praha 2026. Dostupná z WWW <http://hdl.handle.net/11346/H4WT>

## Dedikace

Vznik databáze byl financován z prostředků Programu na podporu aplikovaného výzkumu v oblasti národní a kulturní identity na léta 2023 až 2030 (NAKI III) Ministerstva kultury ČR v rámci projektu *Automatické hodnocení mluveného projevu v češtině* (DH23P03OVV037).

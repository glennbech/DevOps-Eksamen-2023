## Lag en fork

Du må start med å lage en fork av dette repoet til din egen GitHub-konto.

![Alt text](img/fork.png  "a title")

## Logg i Cloud 9 miljøet ditt

![Alt text](img/aws_login.png  "a title")

* Logg på med din AWS bruker med URL, brukernavn og passord
* Gå til tjenesten Cloud9 (Du nå søke på Cloud9 uten mellomrom i søket)
* Velg "Open IDE"
* Hvis du ikke ser ditt miljø, kan det hende du har valgt feil region.

### Lag et Access Token for GitHub

* Når du skal autentisere deg mot din GitHub konto fra Cloud9 trenger du et access token.  Gå til  https://github.com/settings/tokens og lag et nytt.
* NB. Ta vare på tokenet et sted, du trenger dette senere når du skal gjøre ```git push```

Access token må ha "repo" tillatelser, og "workflow" tillatelser.

![Alt text](img/new_token.png  "a title")

### Lage en klone av din Fork (av dette repoet) inn i ditt Cloud 9 miljø

Fra Terminal i Cloud 9. Klone repositoriet *ditt* med HTTPS URL.

```
git clone https://github.com/≤github bruker>/DevOps-Eksamen-2023.git
```

OBS Når du gjør ```git push``` senere og du skal autentisere deg, skal du bruke GitHub brukernavn, og access token som passord,

For å slippe å autentisere seg hele tiden kan man få git til å cache nøkler i et valgfritt antall sekunder på denne måten;

```shell
git config --global credential.helper "cache --timeout=86400"
```

Konfigurer også brukernavnet og e-posten din for GitHub CLI. Da slipepr du advarsler i terminalen når du gjør commit senere.

````shell
git config --global user.name <github brukernavn>
git config --global user.email <email for github bruker>
````

## Slå på GitHub actions for din fork

I din fork av dette repositoriet, velg "actions" for å slå på støtte for GitHub actions i din fork.

![Alt text](img/workflow.png "3")

### Lag Repository secrets

* Lag AWS IAM Access Keys for din bruker.  
* Se på .github/workflows/build_deploy.yaml - Vi setter hemmeligheter ved å legge til følgende kodeblokk i github actions workflow fila vår slik at terraform kan autentisere seg med vår identitet, og våre rettigheter.


```yaml
    env:
      AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
      AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
      AWS_REGION: eu-west-1
```

## Sett en local miljøvariabel i terminalen:
sett en miljøvariabel ```export BUCKET_NAME=your_s3bucket_name```
skriv ```echo $BUCKET_NAME``` for å se om riktig variabelen ble satt.

## Instruksjoner for å kjøre programmet

* pip3 install -r requirements.txt
* For å sette et local environment variable skriv: ```export BUCKET_NAME="kandidat-2030"```
* For å teste python koden skriv: ```cd DevOps-Eksamen-2023/kjell/hello_world``` så skriv: ```python3 app.py```
* For å test sam invoke skriv: ```cd DevOps-Eksamen-2023/kjell``` så skriv: ```sam local invoke HelloWorldFunction --event events/event.json```

## GitHub Actions workflow

* For å teste Github Actions må du gjøre en endring på prosjektet, så kan du lagre CTRL + S og ta ```git add``` for å legge til endringen.
* Så må du comitte endringen ```git commit -m"kommentar her"``` og ```git push``` for å sende in endringen.
* Nå kan du gå inn på Guihub Actions og se at workflows filene jobber med on: push: main: hvis du commited til main branch.

# Oppgave 5

## A. Kontinuelig Integrering

* Kontinuerlig integrasjon (CI) er en utviklingspraksis der kodelinjer fra forskjellige teammedlemmer integreres regelmessig, ofte flere ganger om dagen, i et delt repository. Hver integrasjon utløser automatiserte bygge- og testprosesser for å identifisere og løse konflikter og feil tidlig i utviklingsprosessen.
* Det er flere fordeler med kontinuelig integrasjon, CI identifiserer konflikter og feil tidlig under utviklingsprosessen som reduserer sjansen for feil å bygge seg opp og kan bli vanskelig å løse mye senere. Kodekvalitet er også en av styrkene, for ved å integrere koden ofte vil CI at koden opprettholder høy standard. Dette fører til god kodeformatering og implementering i praksis. Utviklings prosessen vil også bli raskere under en automatisert bygging og testing for da trenger man ikke gjøre dette individuelt lenger, CI gir automatisk tilbakemelding til alle utviklere rask. Siden CI gir beskjed om testene feiler eller virker vil utviklere bli oppdatert i delte repositoriet som hjelper å holde hverandre oppdatert uten å holde møter så ofte som det trengs.
* Om man jobber i gruppe på 4 til 5 vil man bruke CI i GitHub på en måte hvor hver utvikler som ikke jobber på samme del av prosjektet oppretter egen branch for å ungå konflikter når de jobber med seperate funksjoner og oppgaver. Det er også nyttig om man gjør commit og push ofte til sin egen branch for å kjøre automatiske tester av github actions og se om noen jobb feiler eller for å lese tilbakemeldinger på commiten. Når oppgaven er ferdig så kan man kjøre en pull request, her vil CI automatisk teste for å sikre at endringene er kompitabel med eksisterende kode. Så gjøres det kode review hvor man merger kode sånn at det passer og kanskje finner måter å forbedre før det merger. Når pull requesten er godkjent kan CI automatisk dele ut koden til produksjon.

## B. Sammenligning av Scrum/Smidig og DevOps fra et Utviklers Perspektiv

### 1. Scrum/Smidig Metodikk:
Scrum har korte utviklingssykluser som kallses for sprints, hver sprint har potensielt leverbar funksjon eller prdukt. Scrum innholder roller som produkt eier scrum master og utviklere, det er også produkt backlog hvor oppgavene er listet opp og skal gjennomføres. Det er også sprint planlegging hver uke hvor tamet og produkt owner diskuterer hva som skal gjøres i denne ukens sprint, her er det veldig viktig at kommunikasjonen går bra for planleggingen eller kan sprinten bli veldig kaotisk noe jeg har opplevd i min Scrum gruppe. Det er også fint med korte møter på starten av dagen hvor utviklere kan se om noen trenger å parprogrammere for å løse større oppgaver som kan være vaskleig alene, for det er viktig å få oppgaver gjort ferdig under sprints. Det er også meningen at man ikke skal gjøre endringer på planen til sprinten før sprint uken er over. Noen styrker med Scrum er at man har kontinuelig leveranse av kode som går gjennom CI og automatisk testing som er bra for punktene nevnet i oppgave a. Man får se et mer fullført produkt på slutten av hver sprint som gjør det enklere å evaluere hva som mangler eller hva som eventuelt bør endres. Noen utfordringer med Scrum kan komme fra ledelsen og hvordan de bruker tiden til utviklere under sprint dagene, noen scrum master og prdukt owner kan i blant bruke for mye tid på møter og noen store oppgaver kan ofte få alt for lite tid som vil føre til ufullstendig implementering. Det er viktig å ikke overkomplisere oppgaver, men å heler dele dem opp små og sette nokk tid for hver oppgave som de behøver.

### 2. DevOps Metodikk:
Vi får med oss CI kontinuelig integrasjon av kodelinjer fra utviklere flere ganger om dagen, og det er fokus på testing av commited kode for feildeteksjon. Det er også potensielt CD for automatisert testing og distribusjon for å sette kodeendringene i produksjon. DevOps oppsettet automatiserer de manuelle posessene for hvordan man skal commite ferdig code videre i et system med flere utviklere. Risiko er også redusert for feil når man ikke trenger å gjøre det meste manuelt, pipeinen kan også finne feilene på koden tidlig så det ikke kan skape et stop i produksjon. Det finnes også overvåking med loggføring av systemer som gir innsikt i ytelse og drift av produksjonen, dette gir rask informasjon om en ny utlevering av prosjektet var en forbedring av systemet. En ulempe med DevOps kan være at det koster å oppholde en pipeline struktur siden man ofte bruker en service fra for eksempel AWS Services, men siden det har så mange fordeler for sikkerhet, hastighet og struktur så kan det være en større fordel å betale for et DevOps system. Utviklere må også bli lært opp til å bruke dette DevOps systemet effektivt, som ikke vil ta alt for langt tid hvis ikke man er utvikleren som skal jobbe på å forbedre pipelinen.

### 3. Sammenligning og Kontrast:
* Scrum har sterk fokus på tett samarbeid og fleksibilitet som gir mulighet til å tilpasse seg endrende krav og rask respons til feedback. Gjennom høy antall leveranser og kontinuerlig testing legger Scrum vekt på å sikre at koden som leveres har høy kvalitet. Gjennom korte sprints vil Scrum gi raske leveranser, men disse leveransene er normalt sett mindre komplisert og krever mer koordinering. Prosjektet blir som regel klar for produksjon raskt ved bruk av Scrum metodikk, men leveringstiden kan variere veldig over hvor kompleks prosjektet blir.

* DevOps automatiseringen med infrastruktur som kode bidrar til å skape konsistente og solide miljøer, noe som indirekte påvirker programvarekvalitet positivt på mange måter. Overvåkingen i produksjon gir respons fort om feil dukker opp, forbedrer kvalitet ved å redusere nedetid og øker stablitet. Det legges vekt på kontinuerlig leveranse innen DevOps som gir ut oppdateringer raskere til markedet noe som er spesielt for mindre oppdateringer og endringer. Automatiseringen av testing, bygging og distribusjon sparer betydelig mye tid og hver kodeendring kan potensielt være i produksjon raskt og enkelt.

* I konklusjon er valget mellom Scrum og DevOps avhengig av prosjekt spesifikke krav, størrelse, kompleksitet og organisasjonen sin kultur. Begge metodikkene har unike styrker og kan utfylle hverandre i situasjoner der både fleksibilitet og rask leveranse er mer nyttig.

## C. Det Andre Prinsippet - Feedback

Det kan være smart å få brukere til å teste prototyper og designkonsepter av prosjektet, tidlig tilbakemelding kan hjelpe med å bygge en solid plan før implementering. Når brukere gir tilbakemelding, så gir de også tilbakemelding på brukeropplevelsen og hvor brukervennlig prosjektet er. Det er også fint å sette opp et solid automatisert CI for å sikre at hver kodeendring ikke ødeleger for eksisterende kode funksjonalitet, men også fordi vi kan få rask tilbakemelding til utviklere av kontinuelig integrasjon.

En annen måte å teste om en funksjonalitet er god, kan være ved å gradvis levere ut produktet til noen begrenset brukere for å se hvordan resultatene er fra den nye endringen. Dette kan gi nyttig data til utviklerene om funksjonene skaper flere problemer enn forbedringer og det gjøres for noen få brukere som gir denne metoden for å teste en lav risiko. Det kan også være fint å spørre om tilbakemelding om endringene fra brukerene for å se om de er enige i oppdateringen.

Vi kan også sette opp diagrammer for alarmer og traffik på en nettsiden for å se om endringene påvirker tallene. Et eksempel er en varebutikk hvor vi leser av hvor mange som fullfører sin handel i mot hvor mange som forlater handlekurven fordi de ble forvirret over hvordan de skulle fullføre handelen etter den nye oppdateringen. Det kan også være noe så simpelt som en endring på fargen av handlekurv knappen som kan føre til endringer på antall salg i grafen. Statestikk er fint å få med på et dashbord for å overvåke hvilken effekt endringer tar på produksjon, går det dårlig kan man bare gå tilbake til eldre versjon før statestikken for salg falt.

Ved bruk av feedback i alle trinn av utviklingssyklusen blir det mulig å kontinuerlig tilpasse og utvikle programvaren etter brukerens behov og forventninger. Dette skaper en kontinuerlig forbedring og støtter utvikling av kvalitetsprogramvare.


### Jeg måtte droppe Oppgave 4 siden det ikke var noe mer tid, Jeg var syk den første uken og var sengeliggende i 3-4 dager som ga meg tidspress for å fullføre eksamen.

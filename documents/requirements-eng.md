# Stakeholders

## ST01 - Studierende
* Upload von Vorlesungsfolien möglich
* Interaktiver Chatbot zum stellen von Fragen bezüglich hochgeladener Vorlesungsfolien
* Auswahl aus vorgegebenen Vorlesungsfolien
* Antwort auf Chatnachricht mit "möglichst geringer Wartezeit"
* Inkludierung von Informationen/Wissen von Industrieexperten

## ST02 - Lehrstuhl Software-Engineering
* Nutzung der zur Verfügung gestellten API für GPT-3.5 Turbo
* Informationen zur Erweiterung sollen nicht bei jeder Anfrage durchsucht werden -> Vector Store
* Wirtschaftlichkeit der Lösung - festes Budget der bereigestellten API
* Wünschen die Abgabe eines Prototypen und eine finale Auslieferung zu jeweils festen Terminen

## ST03 - Ersteller von Vorlesungsfolien / Dozenten
* Wahrung des Copyrights ihrer hochgeladenen Folien

## ST04 - Development Team

# Scenarios

## SC01 - Stellen von Frage für einen bestehenden Foliensatz
* Nutzer ruft Webanwendung auf (ggf. Authentifizierung)
* Nutzer wird eine Liste der hochgeladenen (ggf. für ihn sichtbaren) Foliensätze präsentiert
* Nutzer wählt einen Foliensatz aus
* Dem Nutzer wird eine Ansicht präsentiert, welche die entsprechenden Vorlesungsfolien und ein Chatfenster kombiniert
* Der Nutzer gibt eine Frage ein
* Der Nutzer erhält eine passende Antwort auf seine Frage mit Inhalten aus der Vorlesung und der Industrie

## SC02 - Hochladen eines neuen Foliensatzes
* Nutzer ruft Webanwendung auf (ggf. Authentifizierung)
* Nutzer ruft die Funktion "Neuen Foliensatz hochladen" aus
* Dem Nutzer wird eine Ansicht präsentiert, in der er den Foliensatz hochladen kann
* Wenn der Foliensatz hochgeladen wurde und die Integration der Daten abläuft, soll dem Nutzer der Fortschritt signalisiert werden (aus der Seite bleiben ist nicht notwendig)
* Wenn der Foliensatz fertig hochgeladen wurde (und er noch auf der Hochlade-Sicht ist), soll dem Nutzer das Stellen von Fragen angeboten werden
* Der Nutzer kann die Vorlesungsfolien nun äquivalent zu SC01 jederzeit auswählen

## SC03 - Löschen eines Foliensatzes
* Nutzer ruft Webanwendung auf (ggf. Authentifizierung)
* Nutzer wird eine Liste der hochgeladenen (ggf. für ihn sichtbaren) Foliensätze präsentiert
* Nutzer wählt zu löschenden Foliensatz aus
* Der Foliensatz ist nun nicht mehr verfügbar um Fragen zu stellen und die Datei sollte vom Server entfernt sein

# Functional Requirements
Functional features of a system (e.g. interface to a payment system, email notification, order system, logistics, management)

## FR01 - Foliensätze hochladen
### Description
Als ein Nutzer, möchte ich beliebiege Foliensätze jederzeit in einer Webanwendung hochladen können.
### Rationale
Die Funktion des Hochladens ist notwendig um die Wissensbasis des Tools zu erweitern und Nutzern zu ermöglichen, zu ihren eigenen Foliensätzen Fragen zu stellen.
### Originator
ST01 - Studierende
### Fit criterion
Nutzer muss ein Upload-Button bereitstehen und nachdem ein Foliensatz hochgeladen wurde, muss dieser auf dem Server für weitere Aktionen bereitstehen.

## FR02 - Fragen zu Foliensätzen stellen
### Description
Als ein Nutzer, möchte ich beliebige hochgeladene Foliensätze auswählen und dann diesbezüglich Fragen stellen können
### Rationale
Es soll Studierenden die Arbeit mit Vorlesungsfolien erleichtert werden, indem Sie dazu gezielt Fragen stellen können
### Originator
ST01 - Studierende
### Fit criterion
Nutzer muss eine Liste an Foliensätzen bereitgestellt bekommen. Nach der Auswahl eines Foliensatzes gibt es eine Ansicht mit Vorlesungen, aus welcher eine ausgewählt werden kann. Abschließend wird in einer Foliensatz-Ansicht dann der Foliensatz an sich gezeigt und das Chatfenster zum Fragen stellen ist sichtbar.

## FR03 - Antworten auf Fragen mit Kontext aus der Industrie ergänzen
### Description
Als ein Nutzer, möchte ich das für die Antwort meiner Frage zusätzliches Industriewissen herangezogen wird.
### Rationale
Oftmals würde eine Antwort lediglich aus Perspektive der Vorlesungsfolien zu wenig praktisches und wirklich erprobtes Wissen vermitteln. Ggf. ist eine zusätzliche Recherche notwendig um das praktische Wissen zu vertiefen.
### Originator
ST01 - Studierende
### Fit criterion
Die Antwort auf die Nutzerfrage beinhaltet nicht nur Wissen, welches aus der Vorlesung oder dem allgemeinen Verständnis des Sprachmodells stammt. Es sind explizit Informationen sichtbar, welche von bestimmten praxisorientierten Blogs stammen und den Nutzen der Antwort verbessern

## FR04 - Grundlegende Sammlung von Vorlesungsfolien abrufbar
### Description
Als Lehrstuhl Software-Engineering möchte ich, dass eine Basis-Sammlung von Vorlesungssätzen in der Anwendung bereits verfügbar ist und ausgewählt werden kann.
### Rationale
Grundlegende Tests der Anwendung sollen durchgeführt werden können, ohne dass erst ein Foliensatz hochgeladen werden muss. Die grundlegenden Funktionalitäten sollen mit dieser Basis einfach nachvollzogen werdne können.
### Originator
ST03 - Lehrstuhl Software-Engineering
### Fit criterion
Bereitgestellter Basis-Foliensatz ist verfügbar und es können Fragen dazu gestellt werden.

# Non-Functional Requirements
All properties, abilities, conditions, and behaviors of the system that are not associated with a functionality (e.g. performance, energy consumption, privacy, safety, security, reliability, development cost)

## NR01 - Schnelligkeit der Beantwortung von Fragen mit möglichst geringer Wartezeit
### Description
Als ein Nutzer möchte ich, dass meine Frage bezüglich eines Foliensatzes mit möglichst geringer Wartezeit beantwortet wird.

Möglichst gering kann in Anlehnung an https://ieeexplore.ieee.org/abstract/document/6263888 und den Kontext der Anwendung spezifiziert werden.
* 10s als ein Limit um den Fokus eines Nutzers auf einen Dialog zu halten
### Rationale
Die Nutzer sollen nicht den Fokus in der Zeitspanne zwischen Frage und Antwort verlieren. Wenn die Antwortzeit zu lang ist, kann der Nutzer abgelenkt werden und die Erfahrung verschlechtert sich. 
### Originator
ST01 - Studierende
### Fit criterion
Die Zeit einer Antwort auf eine Frage liegt im Durchschnitt nicht über 10s.

# Constraints
Restrictions in the implementation of the system (e.g. must run on system X; must deliver a result in X seconds; must finish dev in 180 days)

## CO01 - Anwendung muss in Kubernetes lauffähig sein
### Description
Als Lehrstuhl Software-Engineering möchte ich, dass die Anwendung auf Kubernetes Infrastruktur der Universität lauffähig ist.
### Rationale
Der Lehrstuhl/Fakultät ist lediglich in der Lage eine Kubernetes-Infrastruktur bereitzustellen. Somit muss die Anwendung in dieser Umgebung unbedingt lauffähig sein.
### Originator
ST03 - Lehrstuhl Software-Engineering
### Fit criterion
Die Anwendung muss vollständig containerisiert sein und es muss ein Deployment-Konzept für Kubernetes vorliegen, welches praktisch läuft.

## CO02 - Nutzung eines GPT-3.5 Turbo API Wrappers
### Description
Als Lehrstuhl Software-Engineering gebe ich vor, dass zwingend ein GPT-3.5 Turbo LLM für die direkte Beantwortung genutzt werden muss und dafür auch zwingend der bereitgestellte API-Wrapper verwendet werden soll
### Rationale
Der Lehrstuhl muss das ausgegebene Budget kontrollieren und nutzt dazu den API Wrapper, welcher nur für ein spezifisches LLM bereitgestellt wird.
### Originator
ST03 - Lehrstuhl Software-Engineering
### Fit criterion
Die Anwendung kann einen beliebigen Prompt formatgerecht an den API Wrapper übermitteln und die finale Antwort kann korrekt von der Anwendung verarbeitet werden.

## CO03 - Abschluss eines Prototyps bis 23.06.2023
### Description
Als Lehrstuhl Software-Engineering fordere ich, dass ein Prototyp der Datenintegration bis spätestens 23.06.2023 ausgeliefert werden soll.
### Rationale
### Originator
ST03 - Lehrstuhl Software-Engineering
### Fit criterion
Implementierung der Datenpipeline kann nachvollzogen werden.

## CO04 - Nutzbarkeit produktiver Anwendung bis 25.08.2023
### Description
Als Lehrstuhl Software-Engineering fordere ich, dass die produktive Anwendung bis spätestens 25.08.2023 ausgeliefert und nutzbar sein soll.
### Rationale
### Originator
ST03 - Lehrstuhl Software-Engineering
### Fit criterion
Der gesamte Code der Anwendung kann ausgeliefert werden und sie ist lauffähig im Kubernetes-Cluster.
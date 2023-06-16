# Herausforderungen

## Keine Nutzung der OpenAI Embeddings möglich durch API Wrapper
Umstieg auf ein lokales Embedding Model auf Basis von sBert

## Auslastung des Services, wenn alle Komponenten darauf liegen
Aufteilung der Services nach Rechenintensität in Core Service und Ingest Service

## Synchonisation der beiden Services bezüglich Ingest-Status
Einbringung einer Datenbank, welche neben gescrapten Websites und hochgeladenen Foliensätzen auch den Status von einzelnen Upload Jobs trackt

## Ermittlung des Themas aus hochgeladenen Folien als Basis für Scraping
Es wurden zwei Methoden erprobt (statistischer Ansatz und Language Model-basiert). Dabei ist aufgefallen, dass das Topic Modelling des Language Model zu unzuverlässig ist, da domänenspezifisches Vokabular und themenspezifische Begriffe automatisch als Thema ermittelt werden. Mit dem statistischen Ansatz wurden gute Ergebnisse erzielt mit bestimmten Anpassungen. Allerdings wurde final festgelegt, dass die Nutzer noch ein Thema der Vorlesungsfolien beim Hochladen mitliefern sollen, um die Passgenauigkeit der gescrapeten Beiträge zu verbessern.

## Länge der Elemente für Embedding und Einfügung in Vektor DB
Es wurde zunächst ein Satz als Basis für Embeddings gewählt. Dies hat allerdings insbesondere für Blog-Beiträge zu sehr kurzen Embeddings geführt, welche nicht in der Lage sind einen Wert zu liefern. Unter Umständen waren mehrere Sätze notwendig um ein semantisch sinnvolles Element zu erhalten, welches dann als Kontext geliefert werden kann. Es wurde sich auf eine Länge von 1000 Zeichen geeinigt, wobei NLTK eine sinnvolle Teilung gemäß der Sprache sicherstellt.

# Arbeitsweise
Es wurde in 2-wöchigen Sprints gearbeitet mit einem kombinierten Sprint Review und Planning an den Übergangstagen. Dies hat in den studentischen Alltag und neben den anderen Modulen und teilweise auch Projekten gut funktioniert. Längere Zeiträume hätten ggf. dazu geführt dass das Projekt neben anderen Aufgaben versickert. Kürzere Sprints hätten darin resultiert, dass oft nicht alle Zeit zur Teilnahme gehabt hätten. Eine Kombination von Review und Planning sollte Zeit sparen. Um den Projekterfolg im Studentenalltag zu sichern, wurde im Planning nach Festlegung der zu absolvierenden Features bereits darüber gesprochen, wer welche Teile gerne umsetzen würde und eine lose Unterteilung gemacht. Eine gänzlich freie Einteilung wäre hier chaotisch geworden, da keiner von uns Volllzeit am Projekt arbeitet, wie dies sonst in agilen Teams üblich ist.

# Weiteres Vogehen
Es wurde bereits ein Fokus auf die Modularität gelegt, damit dieser Aufwand nicht vollständig in der zweiten Phase liegt. In der kommenden Zeit soll der Fokus trotzdem zunächst auf eine Stukturierung und Containerisierung der Bestandteile gelegt werden. Dann sollen die Schnittstellen für die Bestandteile definiert werden, welche einerseits als Basis für die tatsächliche Implementierung dieser dienen soll, allerdings auch essenziell für die Frontend-Entwicklung ist. Insofern die Funktionalität der Komponenten und die Interoperabilität implementiert ist, soll die tatsächliche Inbetriebnahme dieser auf dem Kubernetes Cluster erfolgen und auch das gesamte Ops-Tooling dafür entwickelt werden. Abschließendd erfolgt dann die Implementierung von Features wie dem A/B Testing und auch die Validierung von bspw. Response Times kann erfolgen.
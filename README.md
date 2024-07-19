# keycloak-training

## Starten der Anwendung

Nachdem das image der Webanwendung durch `make docker` gebaut wurde, kann mittels `make run` die komplette anwendung gestartet werden.
Durch `make stop` werden alle Services wieder gestoppt.

## Lokales debuggen

Zum lokalen arbeiten kann mit `make venv` die Arbeitsumgebung eingerichtet werden, und mittels `make run-services-only` der Keycloak- und Datenbankservice gestartet werden, sodass die Webanwendung aus VScode gestartet werden kann.

## Login für spezielles Realm

http://localhost:8080/realms/phobosys/account

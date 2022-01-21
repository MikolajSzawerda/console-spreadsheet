# Console Spreadsheet

## Cel i opis projektu

---

Projekt polegał na zaimplementowaniu w pythonie konsolowego arkusza kalkulacyjnego. Program w założeniach miał umożliwiać:


* utworzenie arkusza o zadanych wymiarach

* uruchomienie arkusza z podpoleceniami

* zapis arkusza do pliku

* odczyt arkusza z pliku

* wprowadzanie do komórek wartości tekstowych i liczbowych

* wprowadzanie do komórek funkcji wyliczanych na podstawie wartości z innych komórek

* wprowadzanie do komórek funkcji wyliczanych na podstawie zakresów komórek

* odnoszenie się do wartości komórek za pomocą adresowania identycznego jak w Excelu

* wyświetlanie i bieżące odświeżania wartości komórek

## Opis podziału programu na klasy

---

### Addresses.py

```Address```

Klasa opisująca obiekt adresu, umożliwiająca:

* rozbicie adresu na literę i liczbę,

* przesunięcie adresu o wektor liczbowy w zadanym obszarze ograniczającym

```RangeAddress```

Klasa opisująca obiekt zakresu adresów, umożliwiająca:

* podanie wszystkich adresów wchodzących w skład zakresu,

* określenie ilości wierszy i kolumn wchodzących w skład zakresu

* robicie zakresu na litery i liczby wchodzące w skład adresów zakresu

### Cells.py

```Cell```

Klasa opisująca obiekt komórki arkusza, umożliwiająca:

* podanie wartości komórki lub wpisanego weń polecenia

### Spreadsheets.py

```Spreadsheet```

Klasa opisująca obiekt arkusza, umożliwiająca:

* dodanie/usunięcie komórek do arkusza

* podanie/ ustawienie wartości komórki

* podanie opisu każdej komórki (adres, wartość, "wartość tekstowa")

### Spreadsheets_IO.py

```SpreadsheetIO```

Klasa opisująca obiekt managera do operacji IO na arkuszu, umożliwiająca:

* zapisanie arkusza do pliku

* odczytania arkusza z pliku

* utowrzenie arkusza o zadanych wymiarach i lokalizacji

### SpreadsheetViewes.py

```SpreadsheetView```

Klasa opisująca obiekt widoku arkusza, udostępniająca:

* widok arkusza tak jak w excelu

* wprowadzanie i edytowanie zawartości komórek

* poruszanie się po arkuszu przy pomocy specjalnego kursora

* skalowanie wielkości pokazywanego arkusza do wielkości konsoli

### Commands.py

```CommandInterpreter```

Klasa opisująca obiekt interpretera poleceń, umożliwiająca:

* obliczenie wartości nawiasowanego wyrażenia matematycznego przy pomocy ONP

* obliczenie wartości funkcji korzystających z wartości innych komórek

* przypisanie do podanej komórki wartości wyrażenia, liczby lub tekstu

* odświeżenie wartości w arkuszu, po przez ponowne obliczenie zawartości komórek z komendami


### Errors.py

Skrypt posiadający definicje klas opisujących możliwe wyjątki:

* ```UncorrectAddressAddressValue``` nie poprawny tekst opisujący adres

* ```CellNotInSpreadsheetError``` sięgnięcie po wartość komórki której nie ma w arkuszu

* ```NoTargetCommandAddressError``` nie podanie w komendzie komórki docelowej

* ```UncorrectSpreadsheetPath``` ścieżka nie prowadzi do pliku arkusza

* ```UncorrectSpreadsheetFileFormat``` podany plik nie jest plikiem arkusza

* ```MalformedSpreadsheetFile``` podany plik jest uszkodzony i niemożliwy do odczytania

* ```UncorrectSpreadsheetSize``` użytkownik przy tworzeniu arkusza podał niepoprawny rozmiar

* ```UncorrectCommandName``` użytkownik podał komendą z syntaktycznym błędem

* ```UncorrectGivenCommandValues``` komenda wywołana z niepoprawnymi parametrami

## Instrukcja użytkownika
---

### Uruchomienie programu i podpolecenia

**Brak podpoleceń**
```py
python3 app.py
```
Program pokaże domyślny pusty arkusz, który przy zapisie zostanie utworzony pod nazwą "spreadsheet.py" w miejscu uruchomienia programu

**Podpolecenie -l**

```py
python3 app.py -l ~/spr.csv
```
Program załaduje arkusz dostępny pod zadanym adresem, przy zapisie arkusze, będzie to również plik zapisu

**Podpolecenie -n**

```py
python3 app.py -n ~/spr.csv 10:10
```

Program utworzy i otworzy arkusz w wskazanej lokalizacji o rozmiarach podanych w formacie XxY lub X:Y, gdzie X,Y to ilość wierszy, kolumn

### Nawigacja po arkuszu

**Strzałki** : Służą do przesuwania kursora w wskazanym kierunku

**Edycja zawartości komórki** : ***i***

Po wciśnięciu program przechodzi w tryb edycji, gdzie w specjalnym podświetlonym na zielono polu użytkownik wprowadza nową wartość komórki

**Zapis stanu arkusza** : ***s***

Po każdorazowej edycji program wskazuje na możliwość zapisania nowej zawartości

**Wyjście z programu** : ***q***

Program wychodzi do konsoli

### Wprowadzanie zawartości

**Wprowadzanie tekstu i liczb**

Tak jak w excelu, wystarczy wprowadzić wartość

**Wprowadzanie komend**

*nazwa*(*początek zakresu komórek* **:** *koniec zakresu komórek*)

np: **sum(A1:C3)**

**Wprowadzanie wyrażenia**

Tak jak w excelu należy rozpocząć od **"="**

np: =sum(A1:C3)+12-A2*(C1/(4+3))

**Obsługiwane komendy:** min, max, avg, sum

## Część refleksyjna

---

### Zakres wykonanych prac

* wyświetlanie arkusza tak jak w excelu
* poruszanie się po arkuszu, z przesuwaniem wyświetlanego zakresu arkusza
* responsywna zmiana rozmiaru arkusza wraz z zmianą rozmiaru terminala
* zaprojektowanie optymalnego systemu przechowywania zawartości akrusza
* zaimplementowanie parsersa wyrażeń matematycznych z dostępem do zawartości innych komórek
* odświeżanie widoku arkusza i wartości komórek zależnych przy zmianie wartości
* system adresowania i konwersji na liczbowe koordynaty
* zapis arkusza do pliku, z określeniem lokalizacji, rozmiaru i zawartości arkusza
* odtworzenie arkusza z pliku

### Możliwe dalsze modyfikacje

* sprawdzanie rekursji w wprowadzonych poleceniach
* możliwość ruszania kursorem w polu edycji
* zakres komórek może być listą, a nie prostokątnym zakresem

Głównym powodem niezaimplementowania powyższych punktów był ograniczony zasób czasowy, a także możliwe(głównie przy sprawdzaniu rekursji) obniżenie prędkości działania programu

### Napotkane trudności

Największy problem sprawiło mi napisanie systemu przesuwania widoku arkusza, kiedy kursor przechodził do niewidocznych komórek, a także zmiana rozmiaru arkusza przy zmianie rozmiaru terminala. Pewien problem stanowiło też zaimplementowanie parsera komend, z racji paru możliwych rodzaji wprowadzanych danych(liczba, tekst, wyrażenie) i samego wyliczenia wartości wyrażenia.

## Podsumowanie

Uważam, że mój projekt zasługuje na wysoką ocenę, ponieważ w pełni spełnia podane wymagania funkcjonalne projektu, a także posiada parę dodatkowych funkcjonalności, jak np. dość rozbudowany system wyświetlania i poruszania się po arkuszu i responywny rozmiar to rozmiaru terminala. Ponadto starałem się wprowadzić optymalizacje wydajnościowe, takie jak przechowywanie tylko niepustych komórek w postaci słownika, jedynymi przeliczalnymi komórkami są komórki w którym są wyrażenia, zakresy komórek zaczynają przechowywać wszystkie dostępne w nich adresy, dopiero po pierwszej próbie uzyskania dostępu(dzięki temu arkusz może mieć potencjalnie nieskończony rozmiar), przy ruszaniu kursora przerysowaniu ulegają jedynie dwie komórki.

Sam pomysł projektu był dla mnie interesujący i przyjemnie mi się nad nim pracowało.

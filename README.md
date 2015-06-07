# HardDriveDataAnalyzer#

Aplikacja analizująca dane na dysku twardym i prezentująca użytkownikowi w sposób interaktywny w jaki sposób jest zajęte miejsce (które foldery/typy plików zajmują go najwięcej) - narzędzie pozwalające na ocenienie jak najłatwiej uzyskać wolne miejsce, sugerujące które można usunąć.


Po wybraniu folderu startowego możemy rozpocząć analizę danych. Wyniki analizy zawsze zwracają pliki/foldery posortowane malejąco w stosunku do ich rozmiaru co ułatwia znalezienie plików które są "ciężkie".

Jest również opcja przeszukiwania plików po ich rozszerzeniu. Otrzymujemy wtedy listę rozszerzeń i w każdym z nich podlistę konkretnych plików z tym rozszerzeniem (odpowiednio posortowane).

Następną użyteczną funkcjonalnością jest możliwość filtrowania plików/folderów po rozmiarze np. począwszy od folderu x możemy znaleźć wszystkie pliki/folderu które zajmują więcej niż 1GB.

## Architektura aplikacji##
Aplikacje można podzielić na 3 logiczne podzespoły:
- model (Directory, File) - model danych
- widok - przy użyciu biblioteki Tk
- logikę (w postaci utils'ów) która jest odpowiedzialna za analizę danych

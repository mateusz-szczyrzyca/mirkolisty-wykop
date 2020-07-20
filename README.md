Only for Polish website and polish users

## Co to jest

Skrypt do generowania wiadomości "wołania" w serwisie wykop.pl na podstawie analizy danych wpisów 
pod danym tagiem. Wygenerowaną przez niego wiadomość należy później wkleić do wpisu w wątku.
Zrobiony celem zastąpienia mirkolist.

Skrypt domyślnie stworzony i ustawiony pod wpisy dla tagu [#devopsiarz](https://www.wykop.pl/tag/devopsiarz/), 
ale edytując `mirkolisty.conf` można wpłynąć na tag jak i "tuningować" algorytm dla innych tagów.

Zobacz do pliku `mirkolisty.conf`, aby dowiedzieć się więcej o algorytmie.




## Instalacja

Do uruchomienia wymagane środowisko z Pythonem (zalecana wersja >3.6)

Do instalacji potrzebnych pakietów, użyj `requirements.txt`: `pip install -r requirements.txt`

Skrypt nie korzysta z dostępu do API - w związku z tym nie jest potrzebne nawet bycie zalogowanym na wykop, 
ale z tego też powodu, na razie nie wysyła wygenerowanej wiadomości (to na liście todoana  kiedyś)



## Pytania

Można pisać do `@devopsiarz` na wykop.pl

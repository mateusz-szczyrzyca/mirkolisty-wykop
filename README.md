Only for Polish website and polish users



## Co to jest

Skrypt do generowania wiadomości "wołania" w serwisie wykop.pl na podstawie analizy danych wpisów 
pod danym tagiem. Wygenerowaną przez niego wiadomość należy później wkleić do wpisu w wątku.
Zrobiony celem zastąpienia mirkolist.

Skrypt domyślnie stworzony i ustawiony pod wpisy dla tagu [#devopsiarz](https://www.wykop.pl/tag/devopsiarz/), 
ale edytując `mirkolisty.conf` można wpłynąć na tag jak i "tuningować" algorytm dla innych tagów.

Zobacz do pliku `mirkolisty.conf`, aby dowiedzieć się więcej o algorytmie działania.




## Instalacja

Do uruchomienia wymagane środowisko z Pythonem (wymagana wersja =>3.6)

Do instalacji potrzebnych pakietów, użyj pliku `requirements.txt`, pisząc:
 
`$ pip install -r requirements.txt` 

Nie jest zalecane instalowanie tego z poziomu roota (za pomocą pipa jak również managera pakietów), 
stosuj dockera lub virtualenv (lub podobne rozwiąznaia), aby nie doinstalowywać dodatkowych bibliotek 
do Twojego systemu operacyjnego.

Skrypt **nie korzysta z dostępu do API** - w związku z tym nie jest potrzebne nawet bycie zalogowanym 
na wykop, ale z tego też powodu, na razie nie wysyła wygenerowanej wiadomości (to na liście todo na kiedyś)



## Pytania, bugi, poprawki

W sprawie pytań lub zauważonych błędów utwórz [Issue](https://github.com/mateusz-szczyrzyca/mirkolisty-wykop/issues), 
można też pisać do mnie na wykop.pl - [devopsiarz](https://www.wykop.pl/ludzie/devopsiarz/) (nie obiecuję, że odpiszę)

W razie czego, zachęcam do tworzenia poprawek i otwierania PRów. Dopóki jestem jedynym kontrybutorem, na bezczela 
merguję w mastera.
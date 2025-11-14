rmdir /s /q dist
pyinstaller.exe .\src\main.py -w -i img\icon.ico
mkdir dist\main\img
copy img\logo192.png dist\main\img
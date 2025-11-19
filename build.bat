set argus_version=1.1.0

rmdir /s /q dist\argus_%argus_version%\
pyinstaller.exe .\src\main.py -w -i img\icon.ico -n argus_%argus_version%
ren dist\argus_%argus_version%\argus_%argus_version%.exe argus.exe
mkdir dist\argus_%argus_version%\img
copy img\logo192.png dist\argus_%argus_version%\img
mkdir dist\argus_%argus_version%\tools
copy tools\HadesSavesExtractor.exe dist\argus_%argus_version%\tools\
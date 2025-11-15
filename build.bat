set argus_version=1_1_0

rmdir /s /q dist
pyinstaller.exe .\src\main.py -w -i img\icon.ico -n argus_%argus_version%
ren dist\argus_%argus_version%\argus_%argus_version%.exe argus.exe
mkdir dist\argus_%argus_version%\img
copy img\logo192.png dist\argus_%argus_version%\img
mkdir dist\argus_%argus_version%\tools
copy tools\HadesSavesExtractor.exe dist\argus_%argus_version%\tools\
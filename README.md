# picarro
Scripts para generar datos L1 y gráficos de equipos Picarro de la RUOA

Station Scripts:
Para iniciar el programa que promedia 5 min y envía los datos al servidor, dar doble-click en:
start.bat

===================================
Para enviar un archivo
reprosend.bat año mes dia

Ejemplo: 
call reprosend.bat 2014 01 06

===================================
Para reprocesar cada minuto
en terminal
cd C:\Python_scripts
call reprosend_60s.bat año mes dia


Server Scripts:
Estos archivos van en el servidor para leer los datos L1 (promedios cada 5 min) y generar los gráficos de las últimas 24 h y los archiivos diarios *.png en el servidor de la RUOA.


rem Este script define los argumentos, llama el programa para reprocesar y envía el fichero al servidor 
@echo off
rem Editar estación
set estacion=xxxx
echo %estacion%
python picarro_avg_actual.py  %estacion% UT-6

set buildDate=%DATE:~4,10%
set dateStr=%buildDate:~6,4%-%buildDate:~0,2%-%buildDate:~3,2%_%estacion%_avg.txt
echo %dateStr%
pscp.exe  -pw ru04cc4 avg\\%dateStr% fotos@132.248.8.29:/var/www/Datos/%estacion%/gei/

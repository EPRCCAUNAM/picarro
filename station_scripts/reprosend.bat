rem Este script define los argumentos, llama el programa para reprocesar y envía el fichero al servidor 
@echo off
set anio=%1
set mes=%2
set dia=%3
rem Editar estacion (Ej: unam, altz, cham, jqro, ltux, erno)
set estacion=xxxx
echo %estacion%
python picarro_avg_repo.py  %estacion% UT-6 %anio% %mes% %dia%
set dateStr=%anio%-%mes%-%dia%_%estacion%_avg.txt
echo %dateStr%
pscp.exe  -pw ru04cc4 avg\\%dateStr% fotos@132.248.8.29:/var/www/Datos/%estacion%/gei/

@echo off
chcp 65001 > nul
echo Instalando dependencias...
pip install pybit requests flask streamlit plotly pandas
echo.
echo Listo!
pause

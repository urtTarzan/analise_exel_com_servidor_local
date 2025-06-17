@echo off
cd /d "C:\Users\Administrador\Desktop\automação exel com servidor local"

REM Abre o navegador primeiro (abre numa janela separada e continua o script)
start "" "http://192.168.1.105:5000"

REM Agora executa o Python rodando o servidor (fica na mesma janela)
python iniciador.py

pause
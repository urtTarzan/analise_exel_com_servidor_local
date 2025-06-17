from os.path import exists
from time import sleep
from codigo import codigo_principal
while True:
    if exists("server_on.flag"):

        print('servidor ativo - processando arquivos')
        codigo_principal()

    else:
        print("servidor não repsondeu - aguradoando...")
    sleep(3)

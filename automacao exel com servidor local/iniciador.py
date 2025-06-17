from threading import Thread
from subprocess import run

def iniciar_flask():
    run(["python", "app.py"])

def iniciar_processador():
    run(["python", "servidor.py"])

# Criando as duas threads
thread1 = Thread(target=iniciar_flask)
thread2 = Thread(target=iniciar_processador)

# Iniciando as duas
thread1.start()
thread2.start()

# Esperar terminar (opcional)
thread1.join()
thread2.join()
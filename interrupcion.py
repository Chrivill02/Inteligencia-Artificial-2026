import signal
import time
import sys

def manejar_interrupcion(signum, frame):
    print("\n⚠️ Interrupción del sistema operativo detectada")
    print(f"Señal recibida: {signum}")
    print("Finalizando proceso de forma segura...")
    sys.exit(0)

signal.signal(signal.SIGINT, manejar_interrupcion)

print("Programa en ejecución. Presiona Ctrl+C para interrumpir.")

while True:
    print("Trabajando...")
    time.sleep(1)

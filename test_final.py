import mediapipe as mp
import os

print(f"Ubicación del archivo mediapipe que se está cargando: {mp.__file__}")
try:
    print(f"Soluciones disponibles: {dir(mp.solutions)}")
except AttributeError:
    print("ERROR: Sigue cargando un archivo local o una instalación corrupta.")
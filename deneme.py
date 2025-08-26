import subprocess
import os

def open_text_file(filename):
    try:
        # Windows'ta Notepad'i kullanarak dosya açıyoruz
        subprocess.run(['notepad', filename])
    except FileNotFoundError:
        print("Notepad bulunamadı!")

with open("ornek_dosya.txt", "a", encoding="utf-8") as dosya:
    pass
# Örnek kullanım
open_text_file('ornek_dosya.txt')

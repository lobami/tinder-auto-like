#!/usr/bin/env python3
"""Auto-instalador de dependencias para Tinder Auto-Like Bot"""
import subprocess
import sys
import os
from pathlib import Path

def install_dependencies():
    """Instala dependencias en un virtual environment si no existen."""
    
    # Crear venv si no existe
    venv_path = Path(".venv")
    venv_python = venv_path / "bin" / "python3" if os.name != "nt" else venv_path / "Scripts" / "python.exe"
    
    if not venv_path.exists():
        print("[*] Creando virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", ".venv"], check=True)
        print("[✓] Virtual environment creado")
    
    # Actualizar pip
    print("[*] Actualizando pip...")
    subprocess.run([str(venv_python), "-m", "pip", "install", "--upgrade", "pip"], check=False)
    
    # Instalar dependencias
    print("[*] Instalando dependencias...")
    deps = ["playwright", "python-dotenv"]
    subprocess.run([str(venv_python), "-m", "pip", "install"] + deps, check=True)
    
    # Instalar navegador
    print("[*] Instalando Chromium...")
    subprocess.run([str(venv_python), "-m", "playwright", "install", "chromium"], check=True)
    
    print("[✓] Todo listo!")
    return venv_python

if __name__ == "__main__":
    python_path = install_dependencies()
    print(f"\n[*] Ejecuta: {python_path} main.py")

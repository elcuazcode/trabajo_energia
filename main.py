# main.py
# Módulo principal que inicia la aplicación y conecta los módulos.

import tkinter as tk
from gui import SimulationGUI

def main():
    """Función principal que inicializa la aplicación."""
    root = tk.Tk()
    app = SimulationGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
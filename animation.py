# animation.py
# Módulo para gestionar la animación del movimiento de la caja.
# Coordina las actualizaciones entre física y GUI.

from config import FRAME_TIME

class AnimationManager:
    def __init__(self, gui, physics):
        """Inicializa el gestor de animación.
        
        Args:
            gui (SimulationGUI): Instancia de la interfaz gráfica.
            physics (PhysicsCalculator): Instancia del calculador físico.
        """
        self.gui = gui
        self.physics = physics
        self.running = False
    
    def start(self):
        """Inicia la animación."""
        if not self.running:
            self.running = True
            self.animate()
    
    def pause(self):
        """Pausa la animación."""
        self.running = False
    
    def animate(self):
        """Bucle de animación: actualiza posición y redibuja."""
        if not self.running:
            return
        
        # Actualizar posición (delta_time en segundos)
        delta_time = FRAME_TIME / 1000.0
        try:
            can_move = self.physics.update_position(delta_time)
        except ValueError as e:
            self.gui.show_error(str(e))
            self.pause()
            return
        
        # Actualizar GUI
        self.gui.update_simulation(self.physics)
        
        # Continuar animación si la caja puede moverse
        if can_move:
            self.gui.root.after(FRAME_TIME, self.animate)
        else:
            self.running = False
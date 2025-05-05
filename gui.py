# gui.py
# Módulo que define la interfaz gráfica usando Tkinter.
# Contiene el lienzo para la simulación, paneles de ajustes y resultados.

import tkinter as tk
from tkinter import messagebox
import math
from config import (
    CANVAS_WIDTH, CANVAS_HEIGHT, BOX_SIZE, SURFACE_Y,
    BOX_COLOR, SURFACE_COLOR, BACKGROUND_COLOR,
    GRAVITY_VECTOR_COLOR, NORMAL_VECTOR_COLOR,
    FRICTION_VECTOR_COLOR, APPLIED_VECTOR_COLOR,
    INCLINE_BACKGROUND_COLOR, TRAIL_COLOR, TRAIL_WIDTH,
    TRAIL_MARKER_COLOR, TRAIL_MARKER_SIZE,
    DEFAULT_FRICTION, DEFAULT_MASS, DEFAULT_FORCE, DEFAULT_ANGLE,
    DEFAULT_DISPLACEMENT, GRAVITY, VECTOR_SCALE, LABEL_OFFSET,
    PIXELS_PER_METER
)
from physics import PhysicsCalculator
from animation import AnimationManager

class SimulationGUI:
    def __init__(self, root):
        """Inicializa la interfaz gráfica.
        
        Args:
            root (tk.Tk): Ventana principal de Tkinter.
        """
        self.root = root
        self.root.title("Simulación Física - Fuerza y Trabajo")
        
        # Inicializar física y animación
        self.physics = None
        self.animation = None
        self.angle_deg = DEFAULT_ANGLE
        self.initial_box_x = 50  # Posición inicial de la caja en píxeles
        self.trail_points = []  # Puntos para la trayectoria
        self.trail_start = None  # Posición inicial de la trayectoria
        
        # Crear frame principal para organizar lienzo y panel de información
        main_frame = tk.Frame(self.root)
        main_frame.pack(pady=10)
        
        # Crear lienzo para la simulación
        self.canvas = tk.Canvas(
            main_frame, width=CANVAS_WIDTH, height=CANVAS_HEIGHT,
            bg=BACKGROUND_COLOR
        )
        self.canvas.pack(side=tk.LEFT, padx=10)
        
        # Crear panel de información a la derecha
        self.setup_info_panel(main_frame)
        
        # Dibujar elementos iniciales
        self.draw_initial_scene()
        
        # Crear panel de ajustes
        self.setup_controls()
        
        # Crear panel de resultados
        self.setup_results()
        
        # Crear panel de botones
        self.setup_buttons()
    
    def setup_info_panel(self, parent):
        """Crea el panel de información a la derecha del lienzo."""
        info_frame = tk.Frame(
            parent, bg="gray95", relief="groove", borderwidth=2, padx=8, pady=8
        )
        info_frame.pack(side=tk.LEFT, padx=10)
        
        # Título
        tk.Label(
            info_frame, text="Información Física", font=("Arial", 14, "bold"),
            bg="gray95"
        ).pack(pady=(0, 5))
        
        # Constantes
        tk.Label(
            info_frame, text="Constantes:", font=("Arial", 11, "underline"),
            bg="gray95"
        ).pack(anchor="w")
        self.gravity_label = tk.Label(
            info_frame, text=f"Gravedad (g): {GRAVITY} m/s²", bg="gray95"
        )
        self.gravity_label.pack(anchor="w", pady=1)
        
        # Fuerzas
        tk.Label(
            info_frame, text="Fuerzas:", font=("Arial", 11, "underline"),
            bg="gray95"
        ).pack(anchor="w", pady=(5, 0))
        self.weight_label = tk.Label(
            info_frame, text="Fuerza Gravitacional (F_g): - N",
            fg=GRAVITY_VECTOR_COLOR, bg="gray95"
        )
        self.weight_label.pack(anchor="w", pady=1)
        self.normal_label = tk.Label(
            info_frame, text="Fuerza Normal (F_n): - N",
            fg=NORMAL_VECTOR_COLOR, bg="gray95"
        )
        self.normal_label.pack(anchor="w", pady=1)
        self.friction_label = tk.Label(
            info_frame, text="Fuerza de Fricción (F_f): - N",
            fg=FRICTION_VECTOR_COLOR, bg="gray95"
        )
        self.friction_label.pack(anchor="w", pady=1)
        self.applied_label = tk.Label(
            info_frame, text="Fuerza Aplicada (F_a): - N",
            fg=APPLIED_VECTOR_COLOR, bg="gray95"
        )
        self.applied_label.pack(anchor="w", pady=1)
        self.net_force_label = tk.Label(
            info_frame, text="Fuerza Neta (F_net): - N", bg="gray95"
        )
        self.net_force_label.pack(anchor="w", pady=1)
        
        # Variables
        tk.Label(
            info_frame, text="Variables:", font=("Arial", 11, "underline"),
            bg="gray95"
        ).pack(anchor="w", pady=(5, 0))
        self.acceleration_info_label = tk.Label(
            info_frame, text="Aceleración: - m/s²", bg="gray95"
        )
        self.acceleration_info_label.pack(anchor="w", pady=1)
        self.velocity_info_label = tk.Label(
            info_frame, text="Velocidad: - m/s", bg="gray95"
        )
        self.velocity_info_label.pack(anchor="w", pady=1)
        self.work_info_label = tk.Label(
            info_frame, text="Trabajo: - J", bg="gray95"
        )
        self.work_info_label.pack(anchor="w", pady=1)
        self.displacement_info_label = tk.Label(
            info_frame, text="Desplazamiento: - m", bg="gray95"
        )
        self.displacement_info_label.pack(anchor="w", pady=1)
        self.time_info_label = tk.Label(
            info_frame, text="Tiempo: - s", bg="gray95"
        )
        self.time_info_label.pack(anchor="w", pady=1)
    
    def draw_initial_scene(self):
        """Dibuja la escena inicial: superficie inclinada, fondo gris, caja, trayectoria y marcador."""
        self.canvas.delete("all")  # Limpiar lienzo
        
        # Calcular coordenadas de la superficie inclinada
        angle_rad = math.radians(self.angle_deg)
        surface_length = CANVAS_WIDTH
        surface_start_x = 0
        surface_start_y = SURFACE_Y
        surface_end_x = surface_length * math.cos(angle_rad)
        surface_end_y = SURFACE_Y - surface_length * math.sin(angle_rad)
        
        # Dibujar fondo gris bajo la superficie inclinada
        self.canvas.create_polygon(
            surface_start_x, surface_start_y,
            surface_end_x, surface_end_y,
            surface_end_x, CANVAS_HEIGHT,
            surface_start_x, CANVAS_HEIGHT,
            fill=INCLINE_BACKGROUND_COLOR
        )
        
        # Dibujar superficie inclinada
        self.canvas.create_line(
            surface_start_x, surface_start_y,
            surface_end_x, surface_end_y,
            fill=SURFACE_COLOR, width=5
        )
        
        # Posición de la caja
        box_x = self.initial_box_x
        if self.physics:
            box_x += self.physics.position * PIXELS_PER_METER
        
        box_y_surface = SURFACE_Y - box_x * math.tan(angle_rad)
        box_top_y = box_y_surface - BOX_SIZE
        box_bottom_y = box_y_surface
        
        # Guardar posición inicial de la trayectoria si no está definida
        if not self.trail_start:
            self.trail_start = (self.initial_box_x + BOX_SIZE / 2, box_y_surface)
        
        # Dibujar marcador en el inicio de la trayectoria
        if self.trail_start:
            marker_x, marker_y = self.trail_start
            self.canvas.create_oval(
                marker_x - TRAIL_MARKER_SIZE, marker_y - TRAIL_MARKER_SIZE,
                marker_x + TRAIL_MARKER_SIZE, marker_y + TRAIL_MARKER_SIZE,
                fill=TRAIL_MARKER_COLOR
            )
        
        # Dibujar trayectoria (desde el centro de la base de la caja)
        if self.trail_points:
            for i in range(len(self.trail_points) - 1):
                x1, y1 = self.trail_points[i]
                x2, y2 = self.trail_points[i + 1]
                self.canvas.create_line(
                    x1, y1, x2, y2, fill=TRAIL_COLOR, width=TRAIL_WIDTH
                )
        
        # Actualizar puntos de la trayectoria (centro de la base)
        trail_x = box_x + BOX_SIZE / 2
        trail_y = box_y_surface
        if not self.trail_points or self.trail_points[-1] != (trail_x, trail_y):
            self.trail_points.append((trail_x, trail_y))
        
        # Dibujar caja (rectángulo)
        self.box_id = self.canvas.create_rectangle(
            box_x, box_top_y, box_x + BOX_SIZE, box_bottom_y,
            fill=BOX_COLOR
        )
    
    def setup_controls(self):
        """Crea el panel de ajustes para parámetros ajustables."""
        controls_frame = tk.Frame(self.root)
        controls_frame.pack(pady=10)
        
        # Coeficiente de fricción
        tk.Label(controls_frame, text="Coef. Fricción (μ):").grid(row=0, column=0, padx=5)
        self.friction_scale = tk.Scale(
            controls_frame, from_=0.0, to=1.0, resolution=0.01,
            orient=tk.HORIZONTAL, length=200, command=self.update_friction
        )
        self.friction_scale.set(DEFAULT_FRICTION)
        self.friction_scale.grid(row=0, column=1, padx=5)
        
        # Masa
        tk.Label(controls_frame, text="Masa (kg):").grid(row=1, column=0, padx=5)
        self.mass_entry = tk.Entry(controls_frame, width=10)
        self.mass_entry.insert(0, str(DEFAULT_MASS))
        self.mass_entry.grid(row=1, column=1, padx=5)
        
        # Fuerza aplicada
        tk.Label(controls_frame, text="Fuerza Aplicada (N):").grid(row=2, column=0, padx=5)
        self.force_entry = tk.Entry(controls_frame, width=10)
        self.force_entry.insert(0, str(DEFAULT_FORCE))
        self.force_entry.bind("<Return>", self.update_force)
        self.force_entry.grid(row=2, column=1, padx=5)
        
        # Ángulo de inclinación
        tk.Label(controls_frame, text="Ángulo (grados):").grid(row=3, column=0, padx=5)
        self.angle_scale = tk.Scale(
            controls_frame, from_=0.0, to=45.0, resolution=0.1,
            orient=tk.HORIZONTAL, length=200, command=self.update_angle
        )
        self.angle_scale.set(DEFAULT_ANGLE)
        self.angle_scale.grid(row=3, column=1, padx=5)
    
    def update_friction(self, value):
        """Actualiza el coeficiente de fricción dinámicamente.
        
        Args:
            value (str): Valor del coeficiente de fricción.
        """
        if self.physics:
            friction_coeff = float(value)
            self.physics.update_parameters(
                friction_coeff,
                self.physics.applied_force,
                math.degrees(self.physics.angle_rad)
            )
    
    def update_force(self, event=None):
        """Actualiza la fuerza aplicada dinámicamente."""
        if self.physics:
            try:
                applied_force = float(self.force_entry.get())
                if applied_force < 0:
                    raise ValueError("La fuerza aplicada no puede ser negativa")
                self.physics.update_parameters(
                    self.friction_scale.get(),
                    applied_force,
                    math.degrees(self.physics.angle_rad)
                )
            except ValueError as e:
                self.show_error(str(e))
                if self.animation:
                    self.animation.pause()
                self.force_entry.delete(0, tk.END)
                self.force_entry.insert(0, str(self.physics.applied_force))
    
    def update_angle(self, value):
        """Actualiza el ángulo y redibuja la escena.
        
        Args:
            value (str): Valor del ángulo desde el deslizante.
        """
        self.angle_deg = float(value)
        if self.physics:
            self.physics.update_parameters(
                self.friction_scale.get(),
                self.physics.applied_force,
                self.angle_deg
            )
        self.draw_initial_scene()
        if self.physics:
            self.draw_force_vectors(self.physics.calculate_forces())
    
    def setup_results(self):
        """Crea el panel para mostrar resultados de cálculos."""
        results_frame = tk.Frame(self.root)
        results_frame.pack(pady=10)
        
        self.work_label = tk.Label(results_frame, text="Trabajo (J): -")
        self.work_label.pack()
        
        self.acceleration_label = tk.Label(results_frame, text="Aceleración (m/s²): -")
        self.acceleration_label.pack()
        
        self.displacement_label = tk.Label(
            results_frame, text=f"Desplazamiento (m): {DEFAULT_DISPLACEMENT}"
        )
        self.displacement_label.pack()
        
        self.time_label = tk.Label(results_frame, text="Tiempo (s): -")
        self.time_label.pack()
        
        self.status_label = tk.Label(results_frame, text="Estado: En Reposo")
        self.status_label.pack()
    
    def setup_buttons(self):
        """Crea los botones de control."""
        buttons_frame = tk.Frame(self.root)
        buttons_frame.pack(pady=10)
        
        tk.Button(
            buttons_frame, text="Play", command=self.start_animation
        ).pack(side=tk.LEFT, padx=5)
        tk.Button(
            buttons_frame, text="Pausa", command=self.pause_animation
        ).pack(side=tk.LEFT, padx=5)
        tk.Button(
            buttons_frame, text="Detener y Reiniciar", command=self.stop_and_reset
        ).pack(side=tk.LEFT, padx=5)
        tk.Button(
            buttons_frame, text="Reiniciar", command=self.reset_simulation
        ).pack(side=tk.LEFT, padx=5)
        tk.Button(
            buttons_frame, text="Calcular", command=self.calculate
        ).pack(side=tk.LEFT, padx=5)
    
    def calculate(self):
        """Ejecuta los cálculos físicos y actualiza resultados y vectores."""
        try:
            # Obtener parámetros de la GUI
            mass = float(self.mass_entry.get())
            if mass <= 0:
                raise ValueError("La masa debe ser mayor a 0")
            friction_coeff = self.friction_scale.get()
            applied_force = float(self.force_entry.get())
            if applied_force < 0:
                raise ValueError("La fuerza aplicada no puede ser negativa")
            angle_deg = self.angle_scale.get()
            
            # Inicializar calculador físico
            self.physics = PhysicsCalculator(
                mass, friction_coeff, applied_force, angle_deg
            )
            
            # Calcular fuerzas
            forces = self.physics.calculate_forces()
            
            # Calcular aceleración
            acceleration = self.physics.calculate_acceleration()
            
            # Calcular trabajo (usando desplazamiento fijo para cálculo estático)
            work = self.physics.calculate_work(DEFAULT_DISPLACEMENT)
            
            # Actualizar etiquetas de resultados
            self.work_label.config(text=f"Trabajo (J): {work:.2f}")
            self.acceleration_label.config(text=f"Aceleración (m/s²): {acceleration:.2f}")
            self.displacement_label.config(text=f"Desplazamiento (m): {DEFAULT_DISPLACEMENT}")
            self.time_label.config(text="Tiempo (s): 0.00")
            self.status_label.config(text="Estado: En Reposo")
            
            # Actualizar panel de información
            self.update_info_panel(forces, acceleration, 0.0, work, DEFAULT_DISPLACEMENT, 0.0)
            
            # Redibujar escena
            self.trail_points = []  # Reiniciar trayectoria
            self.trail_start = None
            self.draw_initial_scene()
            
            # Dibujar vectores de fuerza
            self.draw_force_vectors(forces)
            
            # Inicializar animación
            self.animation = AnimationManager(self, self.physics)
            
            # Deshabilitar el campo de masa
            self.mass_entry.config(state="disabled")
            
        except ValueError as e:
            self.show_error(str(e))
    
    def start_animation(self):
        """Inicia la animación del movimiento de la caja."""
        if self.physics and self.animation:
            self.animation.start()
    
    def pause_animation(self):
        """Pausa la animación del movimiento de la caja."""
        if self.animation:
            self.animation.pause()
    
    def reset_simulation(self):
        """Reinicia la simulación a su estado inicial."""
        if self.physics:
            self.physics.reset()
        self.initial_box_x = 50
        self.trail_points = []
        self.trail_start = None
        self.draw_initial_scene()
        self.work_label.config(text="Trabajo (J): -")
        self.acceleration_label.config(text="Aceleración (m/s²): -")
        self.displacement_label.config(text=f"Desplazamiento (m): {DEFAULT_DISPLACEMENT}")
        self.time_label.config(text="Tiempo (s): 0.00")
        self.status_label.config(text="Estado: En Reposo")
        self.canvas.delete("vector")
        self.canvas.delete("label")
        self.update_info_panel({}, 0.0, 0.0, DEFAULT_DISPLACEMENT, 0.0, 0.0)  # Añadido el argumento 'time'
        if self.animation:
            self.animation.pause()
        # Habilitar el campo de masa al reiniciar
        self.mass_entry.config(state="normal")
    
    def stop_and_reset(self):
        """Detiene la animación y reinicia la simulación."""
        if self.animation:
            self.animation.pause()
        self.reset_simulation()
    
    def show_error(self, message):
        """Muestra un mensaje de error.
        
        Args:
            message (str): Mensaje de error a mostrar.
        """
        messagebox.showerror("Error", message)
    
    def update_simulation(self, physics):
        """Actualiza la simulación durante la animación.
        
        Args:
            physics (PhysicsCalculator): Instancia del calculador físico.
        """
        # Redibujar escena con la nueva posición
        self.draw_initial_scene()
        
        # Calcular fuerzas y aceleración
        forces = physics.calculate_forces()
        acceleration = physics.calculate_acceleration()
        velocity = physics.get_velocity()
        
        # Calcular trabajo dinámico (usando desplazamiento acumulado)
        work = physics.calculate_work(physics.displacement)
        
        # Actualizar etiquetas de resultados
        self.work_label.config(text=f"Trabajo (J): {work:.2f}")
        self.acceleration_label.config(text=f"Aceleración (m/s²): {acceleration:.2f}")
        self.displacement_label.config(text=f"Desplazamiento (m): {physics.displacement:.2f}")
        self.time_label.config(text=f"Tiempo (s): {physics.time:.2f}")
        
        # Actualizar estado
        if abs(velocity) < 0.01:
            self.status_label.config(text="Estado: En Reposo")
        elif velocity > 0:
            self.status_label.config(text="Estado: Moviendo a la Derecha")
        else:
            self.status_label.config(text="Estado: Moviendo a la Izquierda")
        
        # Actualizar panel de información
        self.update_info_panel(forces, acceleration, velocity, work, physics.displacement, physics.time)
        
        # Redibujar vectores
        self.draw_force_vectors(forces)
    
    def update_info_panel(self, forces, acceleration, velocity, work, displacement, time):
        """Actualiza el panel de información con los valores actuales.
        
        Args:
            forces (dict): Diccionario con fuerzas calculadas.
            acceleration (float): Aceleración en m/s².
            velocity (float): Velocidad en m/s.
            work (float): Trabajo en Joules.
            displacement (float): Desplazamiento en metros.
            time (float): Tiempo en segundos.
        """
        # Actualizar fuerzas
        self.weight_label.config(text=f"Fuerza Gravitacional (F PROM_g): {forces.get('weight', 0.0):.2f} N")
        self.normal_label.config(text=f"Fuerza Normal (F_n): {forces.get('normal', 0.0):.2f} N")
        self.friction_label.config(text=f"Fuerza de Fricción (F_f): {forces.get('friction', 0.0):.2f} N")
        self.applied_label.config(text=f"Fuerza Aplicada (F_a): {forces.get('applied', 0.0):.2f} N")
        self.net_force_label.config(text=f"Fuerza Neta (F_net): {forces.get('net', 0.0):.2f} N")
        
        # Actualizar variables
        self.acceleration_info_label.config(text=f"Aceleración: {acceleration:.2f} m/s²")
        self.velocity_info_label.config(text=f"Velocidad: {velocity:.2f} m/s")
        self.work_info_label.config(text=f"Trabajo: {work:.2f} J")
        self.displacement_info_label.config(text=f"Desplazamiento: {displacement:.2f} m")
        self.time_info_label.config(text=f"Tiempo: {time:.2f} s")
    
    def draw_force_vectors(self, forces):
        """Dibuja vectores de fuerza con colores, nombres y valores.
        
        Args:
            forces (dict): Diccionario con fuerzas calculadas.
        """
        # Limpiar vectores y etiquetas anteriores
        self.canvas.delete("vector")
        self.canvas.delete("label")
        
        # Centro de la caja
        box_center_x = self.initial_box_x + BOX_SIZE / 2
        if self.physics:
            box_center_x += self.physics.position * PIXELS_PER_METER
        angle_rad = math.radians(self.angle_deg)
        box_y_surface = SURFACE_Y - box_center_x * math.tan(angle_rad)
        box_center_y = box_y_surface - BOX_SIZE / 2
        
        # Definir vectores: tipo, magnitud, color, nombre
        vectors = [
            ("weight", forces["weight"], GRAVITY_VECTOR_COLOR, "F_g"),
            ("normal", forces["normal"], NORMAL_VECTOR_COLOR, "F_n"),
            ("friction", forces["friction"], FRICTION_VECTOR_COLOR, "F_f"),
            ("applied", forces["applied"], APPLIED_VECTOR_COLOR, "F_a")
        ]
        
        for force_type, magnitude, color, label in vectors:
            # Obtener coordenadas del vector
            end_x, end_y = self.physics.get_vector_coordinates(
                force_type, magnitude, box_center_x, box_center_y
            )
            
            # Dibujar vector
            self.canvas.create_line(
                box_center_x, box_center_y,
                end_x, end_y,
                fill=color, arrow=tk.LAST, tags="vector"
            )
            
            # Posicionar etiqueta (nombre y valor)
            label_x = end_x + LABEL_OFFSET * math.cos(math.atan2(end_y - box_center_y, end_x - box_center_x))
            label_y = end_y + LABEL_OFFSET * math.sin(math.atan2(end_y - box_center_y, end_x - box_center_x))
            self.canvas.create_text(
                label_x, label_y,
                text=f"{label}: {magnitude:.2f} N",
                fill=color, tags="label"
            )
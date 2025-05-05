# physics.py
# Módulo para cálculos físicos: fuerzas, aceleración, trabajo y movimiento.
# Usado para simular el comportamiento de la caja en la superficie.

import math

class PhysicsCalculator:
    def __init__(self, mass, friction_coeff, applied_force, angle_deg):
        """Inicializa el calculador físico con parámetros iniciales.
        
        Args:
            mass (float): Masa de la caja en kg.
            friction_coeff (float): Coeficiente de fricción (estático y cinético).
            applied_force (float): Fuerza aplicada en N.
            angle_deg (float): Ángulo de inclinación en grados.
        """
        self.mass = mass
        self.friction_coeff = friction_coeff  # Usado para fricción estática y cinética
        self.applied_force = applied_force
        self.angle_rad = math.radians(angle_deg)
        self.gravity = 9.81  # Aceleración gravitacional en m/s²
        
        # Variables para la animación
        self.velocity = 0.0  # Velocidad inicial en m/s
        self.position = 0.0  # Posición inicial en metros (relativa al inicio)
        self.time = 0.0  # Tiempo acumulado en segundos
        self.displacement = 0.0  # Desplazamiento acumulado en metros
        self.is_moving = False  # Indica si la caja está en movimiento
    
    def update_parameters(self, friction_coeff, applied_force, angle_deg):
        """Actualiza los parámetros dinámicamente durante la animación.
        
        Args:
            friction_coeff (float): Nuevo coeficiente de fricción.
            applied_force (float): Nueva fuerza aplicada.
            angle_deg (float): Nuevo ángulo de inclinación.
        """
        self.friction_coeff = friction_coeff
        self.applied_force = applied_force
        self.angle_rad = math.radians(angle_deg)
    
    def calculate_forces(self):
        """Calcula las fuerzas actuando sobre la caja.
        
        Returns:
            dict: Fuerza gravitacional, normal, fricción, neta y sus componentes.
        """
        # Fuerza gravitacional total
        weight = self.mass * self.gravity
        
        # Componentes de la fuerza gravitacional
        weight_parallel = weight * math.sin(self.angle_rad)  # Paralela a la superficie
        weight_normal = weight * math.cos(self.angle_rad)   # Perpendicular
        
        # Fuerza normal (igual a la componente perpendicular en este caso)
        normal_force = weight_normal
        
        # Fuerza de fricción estática máxima
        friction_static_max = self.friction_coeff * normal_force
        
        # Fuerza resultante sin fricción (fuerza aplicada + componente gravitacional)
        force_without_friction = self.applied_force - weight_parallel
        
        # Determinar si la caja se mueve (fricción estática vs. cinética)
        if abs(force_without_friction) > friction_static_max:
            self.is_moving = True
        elif abs(self.velocity) < 0.01:  # Si la velocidad es muy baja, detener
            self.is_moving = False
        
        # Calcular fuerza de fricción
        if self.is_moving:
            # Fricción cinética (en dirección opuesta al movimiento)
            friction_force = self.friction_coeff * normal_force
            if force_without_friction > 0:
                friction_force = -friction_force  # Opuesta a la dirección positiva
            elif force_without_friction < 0:
                friction_force = abs(friction_force)  # Opuesta a la dirección negativa
        else:
            # Fricción estática (ajusta para mantener la caja en reposo)
            friction_force = -force_without_friction
            if abs(friction_force) > friction_static_max:
                friction_force = friction_static_max if force_without_friction < 0 else -friction_static_max
        
        # Fuerza neta
        net_force = self.applied_force - weight_parallel + friction_force
        
        return {
            "weight": weight,
            "weight_parallel": weight_parallel,
            "normal": normal_force,
            "friction": friction_force,
            "applied": self.applied_force,
            "net": net_force
        }
    
    def calculate_acceleration(self):
        """Calcula la aceleración de la caja.
        
        Returns:
            float: Aceleración en m/s².
        """
        forces = self.calculate_forces()
        net_force = forces["net"]
        return net_force / self.mass if self.mass > 0 else 0.0
    
    def calculate_work(self, displacement):
        """Calcula el trabajo realizado por la fuerza aplicada.
        
        Args:
            displacement (float): Desplazamiento en metros.
        
        Returns:
            float: Trabajo en Joules.
        """
        # Trabajo: W = F * d * cos(θ), donde θ es el ángulo entre F y d
        return self.applied_force * displacement * math.cos(self.angle_rad)
    
    def update_position(self, delta_time):
        """Actualiza la posición y velocidad de la caja durante la animación.
        
        Args:
            delta_time (float): Tiempo transcurrido desde el último fotograma en segundos.
        
        Returns:
            bool: True si la caja puede seguir moviéndose, False si llegó al límite.
        """
        from config import CANVAS_LIMIT, PIXELS_PER_METER
        
        # Calcular aceleración
        acceleration = self.calculate_acceleration()
        
        # Actualizar velocidad: v = v0 + a * t
        self.velocity += acceleration * delta_time
        
        # Actualizar posición: x = x0 + v * t
        delta_position = self.velocity * delta_time
        self.position += delta_position
        self.displacement += abs(delta_position)
        
        # Actualizar tiempo
        self.time += delta_time
        
        # Verificar límites del lienzo (en píxeles)
        pixel_position = self.position * PIXELS_PER_METER
        if pixel_position >= CANVAS_LIMIT:
            self.velocity = 0  # Detener movimiento
            self.position = CANVAS_LIMIT / PIXELS_PER_METER
            self.is_moving = False
            return False
        # Permitir movimiento hacia atrás (posición negativa)
        # No detener en posición 0, dejar que la caja se mueva libremente
        return True
    
    def get_vector_coordinates(self, force_type, magnitude, start_x, start_y):
        """Calcula las coordenadas finales de un vector de fuerza para dibujo.
        
        Args:
            force_type (str): Tipo de fuerza ("weight", "normal", "friction", "applied").
            magnitude (float): Magnitud de la fuerza en Newtons.
            start_x (float): Coordenada x inicial.
            start_y (float): Coordenada y inicial.
        
        Returns:
            tuple: Coordenadas finales (end_x, end_y).
        """
        from config import VECTOR_SCALE
        
        # Dirección de los vectores relativa a la superficie inclinada
        if force_type == "weight":
            # Gravitacional: siempre hacia abajo
            end_x = start_x
            end_y = start_y + magnitude * VECTOR_SCALE
        elif force_type == "normal":
            # Normal: perpendicular a la superficie (hacia arriba, rotada)
            angle = math.pi / 2 - self.angle_rad  # Perpendicular a la superficie
            end_x = start_x + magnitude * VECTOR_SCALE * math.cos(angle)
            end_y = start_y - magnitude * VECTOR_SCALE * math.sin(angle)
        elif force_type == "friction":
            # Fricción: opuesta al movimiento, paralela a la superficie
            end_x = start_x - magnitude * VECTOR_SCALE * math.cos(self.angle_rad)
            end_y = start_y - magnitude * VECTOR_SCALE * math.sin(self.angle_rad)
        elif force_type == "applied":
            # Aplicada: en la dirección del movimiento, paralela a la superficie
            end_x = start_x + magnitude * VECTOR_SCALE * math.cos(self.angle_rad)
            end_y = start_y + magnitude * VECTOR_SCALE * math.sin(self.angle_rad)
        else:
            end_x, end_y = start_x, start_y
        
        return end_x, end_y
    
    def get_velocity(self):
        """Devuelve la velocidad actual de la caja.
        
        Returns:
            float: Velocidad en m/s.
        """
        return self.velocity
    
    def reset(self):
        """Reinicia las variables de animación."""
        self.velocity = 0.0
        self.position = 0.0
        self.time = 0.0
        self.displacement = 0.0
        self.is_moving = False
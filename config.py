# config.py
# Módulo para almacenar constantes y configuraciones globales.
# Estas configuraciones facilitan la personalización sin modificar otros módulos.

# Constantes físicas
GRAVITY = 9.81  # Aceleración gravitacional en m/s²

# Configuraciones de la GUI
CANVAS_WIDTH = 600  # Ancho del lienzo en píxeles
CANVAS_HEIGHT = 400  # Alto del lienzo en píxeles
BOX_SIZE = 50  # Tamaño de la caja (ancho y alto) en píxeles
SURFACE_Y = CANVAS_HEIGHT - 50  # Posición Y de la superficie plana (cuando θ=0)

# Colores
BOX_COLOR = "blue"  # Color de la caja
SURFACE_COLOR = "black"  # Color de la superficie
BACKGROUND_COLOR = "white"  # Color de fondo del lienzo
GRAVITY_VECTOR_COLOR = "green"  # Color del vector gravitacional
NORMAL_VECTOR_COLOR = "purple"  # Color del vector normal
FRICTION_VECTOR_COLOR = "orange"  # Color del vector de fricción
APPLIED_VECTOR_COLOR = "red"  # Color del vector de fuerza aplicada
INCLINE_BACKGROUND_COLOR = "gray80"  # Color del fondo bajo la superficie inclinada
TRAIL_COLOR = "cyan"  # Color de la trayectoria de la caja

# Valores predeterminados de parámetros físicos
DEFAULT_FRICTION = 0.3  # Coeficiente de fricción inicial
DEFAULT_MASS = 1.0  # Masa inicial en kg
DEFAULT_FORCE = 10.0  # Fuerza aplicada inicial en N
DEFAULT_ANGLE = 0.0  # Ángulo de inclinación inicial en grados
DEFAULT_DISPLACEMENT = 5.0  # Desplazamiento fijo para cálculos estáticos en m

# Configuraciones de vectores
VECTOR_SCALE = 10  # Escala para visualizar vectores (píxeles por Newton)
LABEL_OFFSET = 10  # Desplazamiento de etiquetas de vectores en píxeles

# Configuraciones de animación
FPS = 60  # Fotogramas por segundo
FRAME_TIME = 1000 // FPS  # Tiempo por fotograma en milisegundos
PIXELS_PER_METER = 50  # Escala de conversión: píxeles por metro
CANVAS_LIMIT = CANVAS_WIDTH - BOX_SIZE - 10  # Límite derecho del lienzo para la caja
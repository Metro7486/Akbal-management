import argparse

def generate_dm_pitch(handle: str, name: str, followers: int, country: str = "Latam"):
    first_name = name.split()[0] if name else handle.lstrip('@')
    clean_handle = handle.lstrip('@')
    
    pitch = f"""
========================================================================
PITCH DE PROSPECCIÓN PARA CREADORAS LATINAS (@akbal_mgt // 57K SEGUIDORES)
OBJETIVO: @{clean_handle} ({first_name}) | Región: {country}
========================================================================

--- OPCIÓN 1: EL CABALLO DE TROYA (MICRO-PRUEBA GRATIS EN VIVO - MÁXIMA CONVERSIÓN) ---

Hola {first_name}, qué tal. Te escribimos desde la dirección de @akbal_mgt (57K).

Estuvimos viendo tu perfil y tu contenido estético tiene calidad de Top 1%, pero notamos que tu cuenta tiene {followers:,} seguidores y el algoritmo te tiene limitada a tráfico local, cuando el dinero real en plataformas privadas proviene de suscriptores en Estados Unidos y Europa.

Sabemos que en internet hay mucha estafa y desconfianza. Para que no tengas que creer en palabras, hagamos una prueba 100% gratis en tu propia cuenta sin que pongas un solo centavo: mándanos el enlace de tu último Reel o publicación y en menos de 20 minutos le inyectamos 200 likes y comentarios estratégicos para que veas cómo reacciona el algoritmo en tiempo real.

Si te gusta lo que ves, hablamos de nuestros planes mensuales (desde $49 USD/mes con 100% de retención de tus ganancias). Si no, te quedas con el alcance gratis. ¿Cuál es el link de tu Reel más reciente?


--- OPCIÓN 2: ENFOQUE AGENCIA LIBRE (CONTRA LAS AGENCIAS QUE COBRAN 50%) ---

Hola {first_name}. Un saludo desde Akbal Management (@akbal_mgt).

Sabemos que muchas agencias en Latinoamérica intentan quitarte entre el 40% y 50% de tus ganancias para 'manejarte' las redes. En Akbal operamos diferente: te damos infraestructura de autoridad (57K), optimización de perfil y semillado algorítmico por una tarifa fija accesible desde $49 USD/mes, y tú conservas el 100% del control y de tus suscripciones.

Podemos hacer una prueba gratuita en tu último Reel para que veas la calidad antes de decidir cualquier cosa. ¿Te gustaría probarlo?


--- OPCIÓN 3: ENFOQUE BLINDAJE & ALTO ESTATUS (CORTO Y DIRECTO) ---

Hola {first_name}. Vemos tu perfil desde la dirección de @akbal_mgt (57K). Tu estética fotográfica es impecable, pero tu interacción actual está frenando la conversión a tus enlaces privados.

Contamos con cupos limitados este mes en nuestro programa de aceleración para creadoras independientes de Latinoamérica. Planes BBB desde $49 USD/mes con micro-prueba inicial gratuita de 24 horas sin tarjeta.

Si estás activa recibiendo propuestas de crecimiento para tu marca este mes, te comparto los detalles sin compromiso. Un saludo.
========================================================================
"""
    print(pitch)
    return pitch

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generador de Pitches para Creadoras Latinas | Akbal Management')
    parser.add_argument('--handle', required=True, help='Usuario de Instagram')
    parser.add_argument('--name', default='', help='Nombre o alias')
    parser.add_argument('--followers', type=int, default=2500, help='Seguidores actuales')
    parser.add_argument('--country', default='Latam', help='País de la creadora')
    args = parser.parse_args()
    generate_dm_pitch(args.handle, args.name, args.followers, args.country)

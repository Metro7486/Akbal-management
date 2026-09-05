import argparse

def generate_dm_pitch(handle: str, name: str, followers: int, country: str = "Latam"):
    first_name = name.split()[0] if name else handle.lstrip('@')
    clean_handle = handle.lstrip('@')
    
    pitch = f"""
========================================================================
PITCH DE PROSPECCIÓN PARA CREADORAS LATINAS (@akbal_mgt // 57K SEGUIDORES)
OBJETIVO: @{clean_handle} ({first_name}) | Región: {country}
========================================================================

--- OPCIÓN 1: GANCHO INTERNACIONAL (EL DOLOR DE SOLO ATRAER SEGUIDORES LOCALES QUE NO PAGAN) ---

Hola {first_name}, qué tal. Te escribimos desde la dirección de @akbal_mgt (57K).

Estuvimos viendo tu perfil y tu contenido estético tiene calidad de Top 1%. Sin embargo, notamos que tu cuenta tiene {followers:,} seguidores y el algoritmo te tiene limitada a tráfico local, cuando el 85% del dinero real en plataformas privadas proviene de suscriptores en Estados Unidos, Canadá y Europa.

Tenemos un protocolo de aceleración diseñado especialmente para creadoras latinas: posicionamos tu cuenta con autoridad digital y comentarios estratégicos para atraer público con alto poder adquisitivo, sin tocar ni quedarnos con tus comisiones (te quedas con el 100% de tus ingresos).

Te armamos un diagnóstico visual rápido de 2 minutos para destrabar tu alcance. ¿Te gustaría revisarlo por aquí o por correo?


--- OPCIÓN 2: ENFOQUE AGENCIA LIBRE (CONTRA LAS AGENCIAS TRADICIONALES QUE COBRAN 50%) ---

Hola {first_name}. Un saludo desde Akbal Management (@akbal_mgt).

Sabemos que muchas agencias en Latinoamérica intentan quitarte entre el 40% y 50% de tus ganancias para 'manejarte' las redes. En Akbal operamos diferente: te damos la infraestructura de autoridad (57K), optimización de perfil y semillado algorítmico por una tarifa fija accesible en dólares/USDT, y tú conservas el 100% del control y de tus suscripciones.

Detectamos 2 ajustes inmediatos en tus Reels y en tu enlace que te están costando seguidores de alto valor. ¿Te los comparto por aquí?


--- OPCIÓN 3: ENFOQUE BLINDAJE & ALTO ESTATUS (CORTO Y DIRECTO) ---

Hola {first_name}. Vemos tu perfil desde la dirección de @akbal_mgt. Tu estética fotográfica es impecable, pero tu interacción actual está frenando la conversión a tus enlaces privados.

Contamos con cupos limitados este mes en nuestro programa de aceleración para creadoras independientes de Latinoamérica. Paquetes desde $97 USD/mes para blindar tu perfil contra shadowbans y multiplicar tus clics.

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

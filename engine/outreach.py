import argparse

def generate_dm_pitch(handle: str, name: str, followers: int, platform: str = "OnlyFans"):
    first_name = name.split()[0] if name else handle
    clean_handle = handle.lstrip('@')
    
    pitch = f"""
========================================================================
PITCH DIRECTO DE PROSPECCIÓN (ENVIAR DESDE @akbal_mgt // 57K SEGUIDORES)
OBJETIVO: @{clean_handle} ({first_name}) | Plataforma: {platform}
========================================================================

--- OPCIÓN A: ENFOQUE DIRECTO Y EXCLUSIVO (DM DE INSTAGRAM) ---

Hola {first_name}, un gusto. Te escribimos directamente desde la dirección de Akbal Management (@akbal_mgt).

Estuvimos revisando tu perfil y tu contenido estético tiene potencial evidente para posicionarse en el Top 1% de creadoras de {platform}. Sin embargo, notamos que tu cuenta está en {followers:,} seguidores, lo que activa el filtro restrictivo de Instagram: el algoritmo no está recomendando tus Reels a audiencias internacionales de alto poder adquisitivo y estás perdiendo entre un 70% y 80% de clics hacia tu enlace.

Te armamos un diagnóstico visual rápido de cómo podemos sembrar autoridad en tu cuenta y llevarla a +15,000 seguidores con tráfico calificado en menos de 7 días sin que tengas que ceder comisiones de tus suscripciones.

¿Gusta que te comparta la micro-auditoría por aquí?

--- OPCIÓN B: ENFOQUE CORTO / HIGH-STATUS (DM) ---

Hola {first_name}. Vemos tu perfil desde la dirección de @akbal_mgt (57K). Tu contenido fotográfico tiene nivel editorial muy alto, pero tu ratio de interacción actual está frenando el tráfico directo a tu {platform}. 

Tenemos un protocolo de aceleración de autoridad diseñado exclusivamente para modelos y creadoras independientes para desbloquear el algoritmo esta misma semana.

Si estás activa recibiendo postulaciones de crecimiento para tu marca, te envío la propuesta detallada. Un saludo.
========================================================================
"""
    print(pitch)
    return pitch

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generador de Pitches de Prospección | Akbal Management')
    parser.add_argument('--handle', required=True)
    parser.add_argument('--name', default='')
    parser.add_argument('--followers', type=int, default=1200)
    parser.add_argument('--platform', default='OnlyFans')
    args = parser.parse_args()
    generate_dm_pitch(args.handle, args.name, args.followers, args.platform)

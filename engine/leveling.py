import sys, time, json, requests
sys.stdout.reconfigure(encoding="utf-8")
try:
    from config import MTP_API_KEY, MTP_API_URL
except ImportError:
    from engine.config import MTP_API_KEY, MTP_API_URL

def post_mtp(payload):
    payload['key'] = MTP_API_KEY
    res = requests.post(MTP_API_URL, data=payload, timeout=30)
    return res.json()

# 1. Dispatch Likes for Posts 6, 7, 8
likes_targets = [
    {"post": 6, "url": "https://www.instagram.com/p/DTvGqYBDlRb/", "qty": 600},
    {"post": 7, "url": "https://www.instagram.com/p/DTsVHfxjgly/", "qty": 600},
    {"post": 8, "url": "https://www.instagram.com/p/DTqz8nWjpVI/", "qty": 650},
]

print("=== 1. DESPACHANDO LIKES PARA POSTS DEL FONDO (6, 7, 8) ===")
likes_orders = []
for item in likes_targets:
    payload = {
        'action': 'add',
        'service': 2519, # IG Real Likes
        'link': item['url'],
        'quantity': item['qty']
    }
    r = post_mtp(payload)
    print(f"Post {item['post']} ({item['qty']} likes) -> Response: {r}")
    likes_orders.append({'target': item, 'response': r})
    time.sleep(1)

# 2. Distinct Custom Comments Pools
comments_pools = {
    1: [
        "El error que todas cometemos al principio 🤦🏻‍♀️",
        "Totalmente de acuerdo, esperar al algoritmo es perder meses de trabajo",
        "La mejor explicación que he leído en mucho tiempo 👏",
        "Literalmente esto me pasaba a mí hasta que cambié de enfoque",
        "Información de altísimo valor para creadoras independientes ✨",
        "Gracias por compartir esto, abre los ojos",
        "Súper clave el tema de la autoridad inicial 🤍",
        "100% real, sin masa crítica no hay conversión",
        "Ese dato del 80% de abandono es durísimo pero real",
        "Excelente perspectiva estratégica",
        "Recomiendo muchísimo este enfoque a todas las chicas que empiezan",
        "La consistencia y la estrategia lo son todo 📈",
        "Vibes impecables y contenido súper profesional",
        "Muy pocas agencias explican las cosas con tanta claridad",
        "Me encanta la seriedad con la que abordan el crecimiento",
        "Clave para no quemar perfiles intentando cosas a ciegas",
        "Demasiado top esta publicación 🤍✨",
        "Totalmente de acuerdo 🙌🏼",
        "Guardado para repasar siempre",
        "Información que vale oro 🔥"
    ],
    2: [
        "La libertad de mantener el control de tus ingresos es invaluable ✨",
        "Poder monetizar sin ceder porcentajes abusivos hace toda la diferencia",
        "Por fin un modelo de agencia moderno y respetuoso con la creadora",
        "100% de acuerdo con esta filosofía de trabajo 🤍",
        "Tu marca, tus reglas. Exactamente así debe ser 🙌",
        "La visión que tienen es impecable",
        "Excelente propuesta de valor",
        "Profesionalismo y transparencia absoluta",
        "El respeto por la autonomía de la creadora es lo mejor de Akbal",
        "Muy pocas agencias entienden esto hoy en día",
        "De verdad que son los mejores en su área ✨",
        "Marcaron un antes y un después en mi perspectiva 🤍",
        "Totalmente identificada con este mensaje",
        "Adoro esta mentalidad de trabajo",
        "El futuro de la gestión de talento independiente 🔥",
        "Trato directo, sin intermediarios molestos",
        "La mejor decisión 🙌🏼✨",
        "Súper agradecida con el equipo",
        "Elegancia y respeto absoluto",
        "Grandes 👏🤍"
    ],
    3: [
        "El paso de seguidor a suscriptor es pura cuestión de confianza",
        "La primera impresión en Instagram define si compran o se van, tal cual",
        "Excelente desglose del embudo de creadora ✨",
        "El estatus del perfil lo cambia todo radicalmente",
        "Muchísima razón, nadie invierte en un perfil que se ve descuidado",
        "Ese filtro mental del visitante es 100% real 🙌",
        "Súper bien explicado",
        "La autoridad elimina cualquier objeción de precio",
        "Exacto, el perfil público es la carta de presentación",
        "Muy buen contenido, súper aplicable",
        "La psicología de la atención digital en su máxima expresión ✨",
        "De las mejores publicaciones sobre el tema",
        "Clarísimo todo 👏",
        "Totalmente de acuerdo con el protocolo de 7 a 30 días",
        "Impecable análisis",
        "Aportando valor real siempre 🤍",
        "Nivel top de consultoría",
        "Me encantó este post ✨",
        "Información estratégica de primer nivel",
        "Felicidades por la calidad de contenido 🔥"
    ],
    4: [
        "Tener fotos hermosas no basta si nadie las ve, gran verdad 👏",
        "Muchísimas chicas tienen contenido editorial increíble pero cero alcance",
        "Romper el cuello de botella del algoritmo es la clave 📈",
        "Súper identificada con lo de la tracción algorítmica",
        "Es frustrante crear tanto contenido y que Instagram no lo muestre",
        "El impulso adecuado lo cambia todo por completo ✨",
        "Totalmente de acuerdo con esta reflexión",
        "Excelente enfoque para creadoras que se sienten estancadas",
        "La combinación de estética y volumen es invencible",
        "Gracias por poner en palabras lo que nos pasa a muchas 🤍",
        "Ese desbloqueo de alcance es justamente lo que se necesita",
        "Maravilloso post 🙌🏼",
        "Muy top la perspectiva",
        "Verdades que nadie en esta industria dice abiertamente",
        "Un alivio saber que el problema no siempre es el contenido",
        "Gran mensaje para la comunidad ✨",
        "Estrategia pura y dura 👏",
        "Me encantó este diagnóstico",
        "Totalmente real 🤍✨",
        "Siguiendo muy de cerca el trabajo de Akbal 🔥"
    ],
    5: [
        "Increíble oportunidad para las chicas que buscan dar el salto profesional ✨",
        "Mucho éxito a la nueva cohorte de creadoras 🙌",
        "La calidad de representación que ofrecen es inigualable",
        "Plazas súper codiciadas, no me extraña",
        "Gran iniciativa para formalizar el talento independiente 🤍",
        "El nivel de exclusividad que manejan se nota en cada detalle",
        "Recomiendo al 100% postularse con ellos",
        "Una oportunidad de oro para crecer en serio 📈",
        "Todo lo que tocan lo convierten en alta calidad",
        "Orgullo ver agencias con este nivel de compromiso",
        "Qué gran paso para la industria digital ✨",
        "Las mejores vibras para esta nueva selección",
        "Súper emocionada con lo que viene",
        "Profesionalismo de principio a fin 👏",
        "El estándar de la agencia es altísimo",
        "Crecimiento real garantizado",
        "Muchos éxitos a las seleccionadas 🤍",
        "Top tier management ✨",
        "Excelente proyecto",
        "Vamos con todo 🔥"
    ],
    6: [
        "La prueba social es literalmente todo en redes sociales hoy",
        "Nadie entra a una tienda vacía, lo mismo aplica a un perfil de Instagram",
        "Comprobado: suben los seguidores y se disparan las suscripciones 📈",
        "Qué gran frase: la prueba social es la moneda de cambio digital",
        "100% de acuerdo con esta premisa 🙌",
        "La percepción de estatus lo facilita todo",
        "Totalmente demostrado en los números",
        "Excelente post para entender el juego de las redes ✨",
        "La confianza del usuario es lo más caro de conseguir",
        "Maravilloso concepto 👏",
        "La diferencia entre 2K y 25K en conversiones es abismal",
        "Muy acertado este punto de vista",
        "Prueba social = autoridad inmediata 🤍",
        "Clave para cualquier creadora que quiera vivir de esto",
        "Me encantó la analogía",
        "Directo al grano y sin rodeos",
        "Gran verdad digital ✨",
        "Felicidades por compartir contenido tan transparente",
        "Súper alineada con esta visión 🤍",
        "A seguir creciendo con fuerza 🔥"
    ],
    7: [
        "Separar la vitrina pública de la comunidad privada es la regla de oro",
        "Mantener el perfil de Instagram impecable y profesional es clave 🤍",
        "Así se evitan bloqueos y se mantiene el respeto de la marca personal",
        "La mejor estrategia de blindaje para creadoras independientes ✨",
        "Totalmente cierto, cero vulgaridad en redes públicas y máxima elegancia",
        "El tráfico de alto valor prefiere perfiles limpios y sofisticados",
        "Súper de acuerdo con este enfoque multicanal 🙌",
        "Estrategia inteligente y con visión de largo plazo",
        "Proteger la imagen pública es proteger el negocio",
        "Excelente consejo para todas las modelos y creadoras",
        "La sofisticación convierte mucho más, confirmado 📈",
        "Brillante forma de estructurar la presencia digital",
        "Muy pocas personas dominan esta distinción",
        "Me encanta cómo cuidan la imagen de su roster ✨",
        "Elegancia, estatus y discreción",
        "Un diez de diez esta publicación 👏",
        "La clave para atraer suscriptores de alto poder adquisitivo 🤍",
        "Totalmente de acuerdo",
        "Gran lección de branding personal",
        "Nivel superior 🔥"
    ],
    8: [
        "Un manifiesto impecable de cómo debe ser la nueva era del management 👏",
        "Crecimiento real, autonomía y transparencia. Exactamente lo que faltaba ✨",
        "Mucho éxito con este proyecto que rompe los moldes tradicionales",
        "Orgullo ver este nivel de sofisticación en la gestión de talento",
        "El futuro del creador independiente está en agencias como Akbal 🤍",
        "Innovación, estatus y respaldo técnico indiscutible",
        "Felicidades por marcar la diferencia en el mercado",
        "Larga vida a Akbal Management 🙌🏼",
        "La visión es clara y los resultados hablan por sí solos",
        "Impresionante la presencia y el concepto de marca ✨",
        "Un estándar completamente nuevo para la industria",
        "Poniendo la vara muy alta en el mercado hispanohablante 📈",
        "Todo el éxito a esta nueva etapa",
        "Gran equipo y gran filosofía de trabajo 🤍",
        "Siempre inspirando con su calidad estética",
        "De aquí al Top mundial 🔥",
        "Excelente presentación",
        "Adelante con todo el poder ✨",
        "Profesionalismo de elite",
        "Bienvenida esta visión 👏🤍"
    ]
}

targets_comments = [
    {"post": 1, "url": "https://www.instagram.com/p/DVOU-_JDlqu/"},
    {"post": 2, "url": "https://www.instagram.com/p/DVOOSO1DvOA/"},
    {"post": 3, "url": "https://www.instagram.com/p/DVONxwADvvR/"},
    {"post": 4, "url": "https://www.instagram.com/p/DT-TXhoDhIk/"},
    {"post": 5, "url": "https://www.instagram.com/p/DTxmp5Cjqwl/"},
    {"post": 6, "url": "https://www.instagram.com/p/DTvGqYBDlRb/"},
    {"post": 7, "url": "https://www.instagram.com/p/DTsVHfxjgly/"},
    {"post": 8, "url": "https://www.instagram.com/p/DTqz8nWjpVI/"},
]

print("\n=== 2. DESPACHANDO COMENTARIOS PERSONALIZADOS (POSTS 1 AL 8) ===")
comments_orders = []
for item in targets_comments:
    p_num = item['post']
    lines = comments_pools[p_num]
    payload = {
        'action': 'add',
        'service': 4641, # Custom Comments
        'link': item['url'],
        'comments': "\n".join(lines)
    }
    r = post_mtp(payload)
    print(f"Post {p_num} (20 comentarios custom) -> Response: {r}")
    comments_orders.append({'post': p_num, 'response': r})
    time.sleep(1)

# Check new balance
bal = post_mtp({'action': 'balance'})
print(f"\n[SALDO ACTUAL MTP]: {bal.get('balance')} {bal.get('currency')}")

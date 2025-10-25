Velocidades por capa (parallax)
Estrellas: speed = 0.25
Justificación: Son el fondo más lejano, deben moverse muy lento para dar sensación de profundidad.
Montañas: speed = 1.3
Justificación: Más cerca que las estrellas, pero aún fondo. Se mueven un poco más rápido.
Ciudad: speed = 1.1
Justificación: Similar a montañas, pero con edificios. Se mueve despacio para que no distraiga y se mantenga como fondo.
Nubes: speed = 1.2
Justificación: Elemento atmosférico, velocidad intermedia para que no se vean estáticas ni demasiado rápidas.
Colinas (primer plano): speed = 2.0
Justificación: Son el elemento más cercano, deben moverse más rápido para reforzar el efecto parallax y dar dinamismo.
Resumen:
Las capas más lejanas se mueven más lento, las cercanas más rápido. Esto simula la profundidad y hace que el escenario se vea más realista y dinámico.

frame_duration por estado (animación del personaje)
Idle (quieto): frame_duration = 0.10 segundos
Justificación: El personaje está quieto, la animación debe ser lenta y suave para transmitir calma.
Run (corriendo): frame_duration = 0.06 segundos
Justificación: El personaje está en movimiento, la animación debe ser rápida para dar sensación de velocidad y energía.
Jump (salto/aire): frame_duration = 0.12 segundos
Justificación: En el aire, el movimiento es más lento y flotante, así que la animación se hace más pausada.
Resumen:
La animación es más rápida cuando el personaje corre (más energía), más lenta cuando está quieto o en el aire (más calma o flotación). Esto ayuda a que el movimiento se sienta natural y acorde al estado del personaje.


EXTENSIONES
Salto (jump)
Valores clave: gravity = 0.7, jump_power = -13, suelo rect.bottom = 420.
Qué hace: gravity acelera hacia abajo; jump_power da el impulso inicial; 420 es la altura del suelo.
Ajuste rápido: saltos más altos → gravity 0.5, jump_power -10; saltos más rápidos → gravity 1.1, jump_power -16.
Parallax (capas)
Capas y velocidades usadas: estrellas speed 0.25, montañas 1.3, ciudad 1.1, colinas (primer plano) 2.0.
Qué hace: capas lejanas se mueven más lento; cercanas más rápido → sensación de profundidad.
Ajuste rápido: si la ciudad queda oculta sube city.base (edificios más altos) o baja hills.speed; para más profundidad, separa más las velocidades.
Partículas de polvo
Valores clave: spawn cuando |vel.x| > 2 y on_ground; vx ∈ [-0.5,0.5], vy ∈ [-1.0,-0.2], life = 22, tamaño 6x6.
Qué hace: rastro corto y ligero que se desvanece en ≈0.36 s.
Ajuste rápido: más polvo → spawn 3–6 y life 35–60.
Ciclo día/noche
Valores clave: day_speed = 0.0005 (por ms), paletas day/night y overlay alpha máximo ≈ 60.
Qué hace: interpola el gradiente y aplica overlay azul semitransparente para noche.
Ajuste rápido: ciclo más lento → day_speed 0.00005; noche más oscura → overlay alpha 100–120.

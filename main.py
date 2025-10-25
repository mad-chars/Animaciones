# Pygame Práctica 4 - Fondos y Animaciones (Área 1)
# Autor: Prof. Luis (plantilla generada)
# Objetivo: implementar fondos con parallax y animación de sprite (idle/run) con control básico.
import pygame, sys, math, random

pygame.init()
WIDTH, HEIGHT = 960, 540
WINDOW = pygame. display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Práctica 4 - Fondos y Animaciones")
CLOCK = pygame.time.Clock()
FPS = 60
# Debug flags (poner False para desactivar ayudas visuales/prints)
DEBUG = True
DEBUG_VISUALS = True

# ------------------- UTILIDADES -------------------
def make_text(txt, size=20, color=(230,230,240)):
    return pygame.font.SysFont(None, size).render(txt, True, color)

def clamp(v, a, b):
    return max(a, min(v, b))

# ------------------- CAPAS DE FONDO -------------------
class StarLayer:
    """Capa de estrellas que se desplaza (parallax)."""
    def __init__(self, w, h, density=0.02, speed=0.4):
        self.w, self.h = w, h
        self.speed = speed 
        self.offset = 0.0
        self.surf = pygame.Surface((w*2, h), pygame.SRCALPHA)
        self.surf.fill((0,0,0,0))
        count = int(w*h*density)
        for _ in range(count):
            x = random.randint(0, w*2-1)
            y = random.randint(0, h-1)
            # Brillo máximo para estrellas
            c = random.randint(230, 255)
            self.surf.set_at((x, y), (c, c, 255, 255))
            
    def update(self, dt_ms):
        # dt_ms en milisegundos
        self.offset = (self.offset + self.speed*dt_ms) % self.w
        
    def draw(self, screen):
        x = int(self.offset)
        screen.blit(self.surf, (-x, 0))
        screen.blit(self.surf, (-x + self.w, 0))
        
class HillsLayer: 
    """Capa de colinas dbujadas con polígono, parallax."""
    def __init__(self, w, h, color=(60,130,100), base=420, amp=28, freq=0.012, speed=1.0):
        self.w, self.h = w, h
        self.color = color
        self.base = base
        self.amp = amp
        self.freq = freq
        self.speed = speed
        self.offset = 0.0
        # Pre-render con *2 para scroll continuo
        self.surf = pygame.Surface((w*2, h), pygame.SRCALPHA)
        self._render()
        
    def _render(self):
        self.surf.fill((0,0,0,0))
        # Si la capa es ciudad, dibuja edificios
        if self.color == (220, 220, 220):
            for x in range(0, self.w*2, 32):
                b_height = random.randint(60, 120)
                b_width = random.randint(18, 32)
                pygame.draw.rect(self.surf, (220,220,220), (x, self.base-b_height, b_width, b_height))
                # Ventanas
                for wy in range(self.base-b_height+8, self.base, 16):
                    for wx in range(x+4, x+b_width-8, 12):
                        pygame.draw.rect(self.surf, (180,180,180), (wx, wy, 6, 8))
        else:
            for x in range(self.w*2):
                y = int(self.base + math.sin((x)*self.freq)*self.amp)
                pygame.draw.line(self.surf, self.color, (x, y), (x, self.h))
            # Suaviza el borde superior con más opacidad
            overlay = pygame.Surface((self.w*2, self.h), pygame.SRCALPHA)
            overlay.fill((*self.color, 80))
            self.surf.blit(overlay, (0,0))
            
    def update(self, dt_ms):
        self.offset = (self.offset + self.speed*dt_ms) % self.w
    def draw(self, screen):
        x = int(self.offset)
        screen.blit(self.surf, (-x, 0))
        screen.blit(self.surf, (-x + self.w, 0))
        
class CloudsLayer:
    """Capa de 'nubes' translúcidas que se repiten."""
    def __init__(self, w, h, speed=1.8, count=10):
        self.w, self.h = w, h
        self.speed = speed
        self.offset = 0.0
        self.surf = pygame.Surface((w*2, h), pygame.SRCALPHA)
        for _ in range(count):
            cx = random.randint(0, w*2-1)
            cy = random.randint(40, h//2)
            r = random.randint(28, 48)
            cloud = pygame.Surface((r*2, r), pygame.SRCALPHA)
            # Cuerpo principal
            pygame.draw.ellipse(cloud, (255,255,255,160), (0, r//4, r*2, r//2))
            # Borde superior
            pygame.draw.circle(cloud, (255,255,255,180), (r//2, r//2), r//3)
            pygame.draw.circle(cloud, (255,255,255,180), (r, r//2), r//3)
            pygame.draw.circle(cloud, (255,255,255,180), (int(1.5*r), r//2), r//4)
            self.surf.blit(cloud, (cx, cy))
            
    def update(self, dt_ms):
        self.offset = (self.offset + self.speed*dt_ms) % self.w
        
    def draw(self, screen):
        x = int(self.offset)
        screen.blit(self.surf, (-x, 0))
        screen.blit(self.surf, (-x + self.w, 0))
        
# --------------------SPRITE ANIMADO------------------------
def make_idle_frames(size=(48,48)):
    """Genera frames 'idle' simples (boteo) sin assets externos."""
    w, h = size
    frames = []
    for i in range(6):
        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        # cuerpo
        pygame.draw.rect(surf, (240, 220, 90), (8, 12, w-16, h-20), border_radius=10)
        # cara/bote
        dy = int(math.sin(i/6*math.tau)*2)
        pygame.draw.circle(surf, (30,30,30), (w//2-6, 18+dy), 4)
        pygame.draw.circle(surf, (30,30,30), (w//2+6, 18+dy), 4)
        pygame.draw.rect(surf, (30,30,30), (w//2-8, 26+dy, 16, 3), border_radius=2)
        frames.append(surf)
    return frames

def make_run_frames(size=(48,48)):
    """Genera frames 'run' básicos (brazos/piernas)."""
    w,h = size
    frames = []
    for i in range(8):
        surf = pygame.Surface((w,h), pygame.SRCALPHA)
        # cuerpo
        pygame.draw.rect(surf, (240, 120, 90), (8, 8, w-16, h-16), border_radius=10)
        phase = i/8*math.tau
        arm = int(math.sin(phase)*6)
        leg = int(math.cos(phase)*6)
        # brazos
        pygame.draw.rect(surf, (60,60,60), (4, 18+arm, 10, 6), border_radius=3)
        pygame.draw.rect(surf, (60,60,60), (w-14, 18-arm, 10, 6), border_radius=3)
        # piernas 
        pygame.draw.rect(surf, (40,40,40), (12, h-14+leg, 10, 6), border_radius=2)
        pygame.draw.rect(surf, (40,40,40), (w-22, h-14-leg, 10, 6), border_radius=2)
        # ojos
        pygame.draw.circle(surf, (30,30,30), (w//2-6, 18), 4)
        pygame.draw.circle(surf, (30,30,30), (w//2+6, 18), 4)
        frames.append(surf)
    return frames

class AnimSprite(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.frames_idle = make_idle_frames()
        self.frames_run = make_run_frames()
        self.frames_jump = self.make_jump_frames()
        self.frames = self.frames_idle
        self.frame_index = 0
        self.frame_time = 0
        self.frame_duration = 0.08  # s por frame
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=pos)

        # movimiento horizontal
        self.vel = pygame.Vector2(0, 0)
        self.accel = 0.7
        self.friction = 0.86
        self.max_speed = 6.5
        self.facing_left = False

        # salto y gravedad
        self.on_ground = True
        self.vel_y = 0
        self.gravity = 0.7
        self.jump_power = -13
        self.state = "idle"  # idle, run, jump

    def make_jump_frames(self, size=(48,48)):
        # Animación simple de salto (aire)
        w, h = size
        frames = []
        for i in range(4):
            surf = pygame.Surface((w, h), pygame.SRCALPHA)
            pygame.draw.rect(surf, (180, 180, 220), (8, 12, w-16, h-20), border_radius=10)
            pygame.draw.circle(surf, (30,30,30), (w//2-6, 18), 4)
            pygame.draw.circle(surf, (30,30,30), (w//2+6, 18), 4)
            pygame.draw.rect(surf, (30,30,30), (w//2-8, 26, 16, 3), border_radius=2)
            # piernas extendidas
            pygame.draw.rect(surf, (40,40,40), (12, h-18, 10, 6), border_radius=2)
            pygame.draw.rect(surf, (40,40,40), (w-22, h-18, 10, 6), border_radius=2)
            frames.append(surf)
        return frames

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel.x -= self.accel
            self.facing_left = True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel.x += self.accel
            self.facing_left = False
        # salto
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and self.on_ground:
            self.vel_y = self.jump_power
            self.on_ground = False
            self.state = "jump"

    def apply_physics(self):
        # horizontal
        self.vel.x = clamp(self.vel.x, -self.max_speed, self.max_speed)
        self.vel.x *= self.friction
        self.rect.x += int(self.vel.x)

        if self.rect.left < 0:
            self.rect.left = 0
            self.vel.x = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.vel.x = 0

        # salto y gravedad
        self.rect.y += int(self.vel_y)
        if not self.on_ground:
            self.vel_y += self.gravity
            # suelo
            if self.rect.bottom >= 420:
                self.rect.bottom = 420
                self.vel_y = 0
                self.on_ground = True
                self.state = "idle"

    def choose_animation(self):
        moving = abs(self.vel.x) > 0.2
        if not self.on_ground:
            target = self.frames_jump
        else:
            target = self.frames_run if moving else self.frames_idle

        if target is not self.frames:
            self.frames = target
            self.frame_index = 0
            self.frame_time = 0.0
            # animación corre más rápido que idle
            if target is self.frames_run:
                self.frame_duration = 0.06
            elif target is self.frames_jump:
                self.frame_duration = 0.12
            else:
                self.frame_duration = 0.10

    def animate(self, dt):
        self.frame_time += dt
        if self.frame_time >= self.frame_duration:
            self.frame_time = 0.0
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            frame = self.frames[self.frame_index]
            self.image = pygame.transform.flip(frame, True, False) if self.facing_left else frame

    def update(self, dt):
        self.handle_input()
        self.apply_physics()
        self.choose_animation()
        self.animate(dt)

# ------------- ESCENA ---------------
def draw_gradient_bg(screen, top=(10, 12, 22), bottom=(25, 28, 48)):
    """Fondo de degradado vertical rápido."""
    for y in range(HEIGHT):
        t = y/HEIGHT
        r = int(top[0]*(1-t) + bottom[0]*t)
        g = int(top[1]*(1-t) + bottom[1]*t)
        b = int(top[2]*(1-t) + bottom[2]*t)
        pygame.draw.line(screen, (r,g,b), (0,y), (WIDTH,y))


def main():
    # Capas de fondo
    stars_far = StarLayer(WIDTH, HEIGHT, density=0.004, speed=0.25)  # Más estrellas
    clouds = CloudsLayer(WIDTH, HEIGHT, speed=1.2, count=22)        # Más nubes
    hills = HillsLayer(WIDTH, HEIGHT, color=(35, 90, 70), base=400, amp=36, freq=0.010, speed=2.0)
    # Capas extra (montañas y ciudad) con mayor amplitud y frecuencia para más detalles
    mountains = HillsLayer(WIDTH, HEIGHT, color=(80, 80, 120), base=370, amp=32, freq=0.012, speed=1.3)
    city = HillsLayer(WIDTH, HEIGHT, color=(220, 220, 220), base=410, amp=0, freq=0, speed=1.1)  # Ciudad clara y alta

    player = AnimSprite((WIDTH//2, 360))
    group = pygame.sprite.Group(player)

    # Partículas de polvo
    particles = []

    # Día/noche
    day_time = 0.0  # 0 a 1
    day_speed = 0.0005

    running = True
    while running:
        dt_ms = CLOCK.tick(FPS)
        dt = dt_ms/1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        # Update
        stars_far.update(dt_ms)
        clouds.update(dt_ms)
        hills.update(dt_ms)
        mountains.update(dt_ms)
        city.update(dt_ms)
        group.update(dt)

        # Día/noche
        day_time += day_speed * dt_ms
        if day_time > 1.0:
            day_time = 0.0

        # Gradiente de fondo dinámico
        # Día: azul claro, Noche: azul oscuro
        day_factor = 0.5 + 0.5 * math.cos(day_time * math.tau)
        top_day = (60, 120, 220)
        bottom_day = (180, 220, 255)
        top_night = (10, 12, 22)
        bottom_night = (25, 28, 48)
        top = tuple(int(top_day[i]*day_factor + top_night[i]*(1-day_factor)) for i in range(3))
        bottom = tuple(int(bottom_day[i]*day_factor + bottom_night[i]*(1-day_factor)) for i in range(3))

        # Partículas de polvo al correr
        moving = abs(player.vel.x) > 2 and player.on_ground
        if moving:
            # Genera partículas cerca de los pies
            for _ in range(random.randint(1,2)):
                px = player.rect.centerx + random.randint(-10,10)
                py = player.rect.bottom - 4 + random.randint(-2,2)
                particles.append({
                    'x': px,
                    'y': py,
                    'vx': random.uniform(-0.5,0.5),
                    'vy': random.uniform(-1.0,-0.2),
                    'life': 22,
                    'alpha': 255
                })
        # Actualiza partículas
        for p in particles[:]:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['life'] -= 1
            p['alpha'] = max(0, int(255 * (p['life']/22)))
            if p['life'] <= 0:
                particles.remove(p)

        # Draw
        draw_gradient_bg(WINDOW, top, bottom)
        stars_far.draw(WINDOW)        # más lejos (más lento)
        mountains.draw(WINDOW)        # montañas
        city.draw(WINDOW)             # ciudad
        clouds.draw(WINDOW)           # medio
        hills.draw(WINDOW)            # cercano (más rápido)
        group.draw(WINDOW)

        # Partículas de polvo
        for p in particles:
            surf = pygame.Surface((6,6), pygame.SRCALPHA)
            surf.fill((200,200,180,p['alpha']))
            WINDOW.blit(surf, (p['x'], p['y']))

        # Día/noche: overlay azul más puro y menos opaco
        night_factor = 1 - day_factor
        night_alpha = int(60 * night_factor)  # Menos opacidad
        night_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        night_overlay.fill((30, 60, 120, night_alpha))
        WINDOW.blit(night_overlay, (0,0))

        # HUD
        hud = [
            "Práctica 4 – Fondos y Animaciones",
            f"FPS: {int(CLOCK.get_fps())} | Frame: {player.frame_index} | Anim: {'RUN' if player.frames is player.frames_run else ('JUMP' if player.frames is player.frames_jump else 'IDLE')}",
            "Izq/Der o A/D para mover | ESPACIO/ARRIBA para saltar | ESC para salir.",
            "Extensiones: salto, parallax extra, polvo, ciclo día/noche."
        ]
        for i, line in enumerate(hud):
            WINDOW.blit(make_text(line, 20), (10, 10 + i*20))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()


# ---------------- Retos/Extensiones ----------------
# 1) Sprite sheet real: carga una hoja (PNG) y corta frames con subsurface.
# 2) Estado 'salto' (JUMP): agrega una animación y física vertical simple (gravedad).
# 3) Parallax 4+ capas: agrega una capa de ciudad/montañas extra al frente.
# 4) Cámara: desplaza el mundo según la posición del jugador y repite fondo infinito.
# 5) Control de tiempo: usa acumulador para animación independiente del FPS.
# 6) Transiciones de día/noche: modifica el gradiente y alta de nubes con un ciclo.
# 7) Efectos: agrega partículas al correr (polvo) que desaparezcan con el tiempo.
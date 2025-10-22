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

# ------------------- UTILIDADES -------------------
def make_text(txt, size=20, color=(230,230,240)):
    return pygame.font.SysFont(None, size).render(txt, True, color)

def clamp(v, a, b):
    return max(a, min(v, b))

# ------------------- CAPAS DE FONDO -------------------
class StarLayer:
    """Capa de estrellas que se desplaza (parallax)."""
    def __init__(self, w, h, density=0.008, speed=0.4):
        self.w, self.h = w, h
        self.speed = speed 
        self.offset = 0.0
        self.surf = pygame.Surface((w*2, h), pygame.SRCALPHA)
        self.surf.fill((0,0,0,0))
        count = int(w*h*density)
        for _ in range(count):
            x = random.randint(0, w*2-1)
            y = random.randint(0, h-1)
            c = random.randint(180,255)
            self.surf.set_At((x, y), (c,c,c, 255))
            
    def update(self, dt_ms):
        # dt_ms en milisegundos
        self.offset = (self.offset + self.speed*dt_ms) % self.w
        
    def draw(self, screen):
        x = int(self.offset)
        screen.blit(self.surf, (-x, 0))
        screen.blit(self.surf, (-x + self.w, 0))
        
class HillsLayer: 
    """Capa de colinas dbujadas con polígono, parallax."""
    def __init__(self, w, h, color=(40,80,60), base=420, amp=28, freq=0.012, speed=1.0):
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
        for x in range(self.w*2):
            y = int(self.base + math.sin((x)*self.freq)*self.amp)
            pygame.draw.line(self.surf, self.color, (x, y), (x, self.h))
            # Suaviza el borde superior
            overlay = pygame.Surface((self.w*2, self.h), pygame.SRCALPHA)
            overlay.fill((*self.color, 30))
            self.surf.blit(overlay, (0,0))
            
    def update(self, dt_ms):
        self.offset = (self.offset + self.speed*dt_ms) % self.w
    def draw(self, screen):
        x = int(self.offset)
        screen.blit(self.surf, (-x, 0))
        screen.blit(self.surf, (-x, + self.w, 0))
        
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
            r = random.randint(20, 60)
            cloud = pygame.Surface((r*4, r*2), pygame.SRCALPHA)
            for i in range(6):
                pygame.draw.circle(cloud, (255, 255, 255, 60), (random.randint(r,3*r), random.randint(r//2, r)), random.randint(r//2, r))
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
        pygame.draw.rect(surf, (240, 220, 90), (8, 12, w-16, h-20), border_Radius=10)
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
        
import pygame, sys, random, os, math

# Initialize Game
pygame.init()

# Game States
MENU = 0
PLAYING = 1
GAME_OVER = 2
PAUSED = 3

game_state = MENU
score = 0
high_score = 0
has_moved = False

# Window Setup
window_w = 400
window_h = 600

screen = pygame.display.set_mode((window_w, window_h))
pygame.display.set_caption("Flap.py")
clock = pygame.time.Clock()
fps = 60

def asset_path(*path_parts):
    return os.path.join(os.path.dirname(__file__), *path_parts)

# Load Fonts
try:
    font_large = pygame.font.Font(asset_path("Fonts", "BaiJamjuree-Bold.ttf"), 60)
    font_medium = pygame.font.Font(asset_path("Fonts", "BaiJamjuree-Bold.ttf"), 36)
    font_small = pygame.font.Font(asset_path("Fonts", "BaiJamjuree-Bold.ttf"), 20)
except:
    font_large = pygame.font.Font(None, 60)
    font_medium = pygame.font.Font(None, 36)
    font_small = pygame.font.Font(None, 24)

# Load Sounds
try:
    slap_sfx = pygame.mixer.Sound(asset_path("Sounds", "slap.wav"))
    woosh_sfx = pygame.mixer.Sound(asset_path("Sounds", "woosh.wav"))
    score_sfx = pygame.mixer.Sound(asset_path("Sounds", "score.wav"))
    slap_sfx.set_volume(0.7)
    woosh_sfx.set_volume(0.5)
    score_sfx.set_volume(0.6)
except:
    slap_sfx = None
    woosh_sfx = None
    score_sfx = None

# Load Images or create colored rectangles as fallbacks
def load_image_or_fallback(path, size, color):
    try:
        return pygame.image.load(asset_path(*path))
    except:
        surf = pygame.Surface(size)
        surf.fill(color)
        return surf

player_img = load_image_or_fallback(("Images", "player.png"), (34, 24), (255, 255, 0))
pipe_up_img = load_image_or_fallback(("Images", "pipe_up.png"), (52, 320), (0, 200, 0))
pipe_down_img = load_image_or_fallback(("Images", "pipe_down.png"), (52, 320), (0, 200, 0))
ground_img = load_image_or_fallback(("Images", "ground.png"), (400, 64), (139, 69, 19))
bg_img = load_image_or_fallback(("Images", "background.png"), (400, 600), (135, 206, 235))

bg_width = bg_img.get_width()

# Variable Setup
bg_scroll_spd = 1
ground_scroll_spd = 2

# Particle system for effects
class Particle:
    def __init__(self, x, y, color, velocity, lifetime):
        self.x = x
        self.y = y
        self.color = color
        self.vx, self.vy = velocity
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.size = random.randint(2, 5)
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.1  # gravity
        self.lifetime -= 1
        return self.lifetime > 0
    
    def draw(self, surface):
        alpha = int(255 * (self.lifetime / self.max_lifetime))
        color = (*self.color, alpha)
        size = max(1, int(self.size * (self.lifetime / self.max_lifetime)))
        try:
            s = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, color, (size, size), size)
            surface.blit(s, (self.x - size, self.y - size))
        except:
            pygame.draw.circle(surface, self.color[:3], (int(self.x), int(self.y)), size)

particles = []

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 0
        self.rotation = 0
        self.animation_time = 0
        self.bob_offset = 0
        
    def jump(self):
        self.velocity = -10
        if woosh_sfx:
            pygame.mixer.Sound.play(woosh_sfx)
        
        # Add jump particles
        for _ in range(8):
            particles.append(Particle(
                self.x + player_img.get_width() // 2,
                self.y + player_img.get_height(),
                (255, 255, 255),
                (random.uniform(-2, 2), random.uniform(-3, -1)),
                30
            ))
    
    def update(self):
        if has_moved:
            self.velocity += 0.75
            self.y += self.velocity
            
            # Rotation based on velocity
            self.rotation = max(-30, min(30, self.velocity * 3))
        else:
            # Gentle bobbing animation when idle
            self.animation_time += 0.1
            self.bob_offset = math.sin(self.animation_time) * 3
    
    def draw(self):
        # Rotate player image based on velocity
        if has_moved:
            rotated_img = pygame.transform.rotate(player_img, -self.rotation)
            rect = rotated_img.get_rect(center=(self.x + player_img.get_width()//2, 
                                               self.y + player_img.get_height()//2))
            screen.blit(rotated_img, rect)
        else:
            screen.blit(player_img, (self.x, self.y + self.bob_offset))

class Pipe:
    def __init__(self, x, height, gap, velocity):
        self.x = x
        self.height = height
        self.gap = gap
        self.velocity = velocity
        self.scored = False
        self.highlight = False
        self.highlight_time = 0

    def update(self):
        self.x -= self.velocity
        if self.highlight:
            self.highlight_time += 1
            if self.highlight_time > 30:
                self.highlight = False
                self.highlight_time = 0

    def draw(self):
        # Add slight glow effect when scored
        if self.highlight:
            glow_surface = pygame.Surface((pipe_up_img.get_width() + 4, window_h), pygame.SRCALPHA)
            glow_color = (255, 255, 0, 100)
            pygame.draw.rect(glow_surface, glow_color, 
                           (0, 0, pipe_up_img.get_width() + 4, window_h))
            screen.blit(glow_surface, (self.x - 2, 0))
        
        # Draw top pipe
        screen.blit(pipe_down_img, (self.x, 0 - pipe_down_img.get_height() + self.height))
        
        # Draw bottom pipe
        screen.blit(pipe_up_img, (self.x, self.height + self.gap))

def create_explosion(x, y, color):
    """Create explosion particles"""
    for _ in range(15):
        particles.append(Particle(
            x, y, color,
            (random.uniform(-4, 4), random.uniform(-4, 4)),
            random.randint(20, 40)
        ))

def update_particles():
    """Update all particles and remove dead ones"""
    global particles
    particles = [p for p in particles if p.update()]

def draw_particles():
    """Draw all particles"""
    for particle in particles:
        particle.draw(screen)

def scoreboard():
    show_score = font_large.render(str(score), True, (255, 255, 255))
    score_rect = show_score.get_rect(center=(window_w//2, 64))
    
    # Add shadow effect
    shadow = font_large.render(str(score), True, (0, 0, 0))
    shadow_rect = shadow.get_rect(center=(window_w//2 + 2, 66))
    screen.blit(shadow, shadow_rect)
    screen.blit(show_score, score_rect)

def draw_menu():
    """Draw the main menu"""
    # Draw the game background (sky with clouds)
    screen.fill((135, 206, 235))  # Sky blue
    screen.blit(bg_img, (0, 0))
    screen.blit(ground_img, (0, 536))
    
    # Draw some clouds for atmosphere
    cloud_color = (255, 255, 255, 180)
    cloud_surface = pygame.Surface((80, 40), pygame.SRCALPHA)
    pygame.draw.ellipse(cloud_surface, cloud_color, (0, 10, 30, 20))
    pygame.draw.ellipse(cloud_surface, cloud_color, (20, 5, 35, 25))
    pygame.draw.ellipse(cloud_surface, cloud_color, (45, 10, 30, 20))
    
    # Position clouds
    screen.blit(cloud_surface, (50, 120))
    screen.blit(cloud_surface, (250, 180))
    screen.blit(cloud_surface, (120, 220))
    screen.blit(cloud_surface, (300, 80))
    
    # Title - large and centered
    title = font_large.render("Flap.py", True, (255, 255, 255))
    title_shadow = font_large.render("Flap.py", True, (0, 0, 0))
    title_rect = title.get_rect(center=(window_w//2, window_h//2 - 50))
    title_shadow_rect = title_shadow.get_rect(center=(window_w//2 + 3, window_h//2 - 47))
    screen.blit(title_shadow, title_shadow_rect)
    screen.blit(title, title_rect)
    
    # Main instruction - centered below title
    start_text = font_medium.render("Press SPACE to Start", True, (255, 255, 255))
    start_shadow = font_medium.render("Press SPACE to Start", True, (0, 0, 0))
    start_rect = start_text.get_rect(center=(window_w//2, window_h//2 + 30))
    start_shadow_rect = start_shadow.get_rect(center=(window_w//2 + 2, window_h//2 + 32))
    screen.blit(start_shadow, start_shadow_rect)
    screen.blit(start_text, start_rect)
    
    # High score - positioned above footer
    if high_score > 0:
        hs_text = font_medium.render(f"{high_score}", True, (255, 215, 0))
        hs_shadow = font_medium.render(f"{high_score}", True, (0, 0, 0))
        hs_rect = hs_text.get_rect(center=(window_w//2, 450))
        hs_shadow_rect = hs_shadow.get_rect(center=(window_w//2 + 2, 452))
        screen.blit(hs_shadow, hs_shadow_rect)
        screen.blit(hs_text, hs_rect)
    
    # Footer controls - at bottom
    controls_text = font_small.render("SPACE: Jump | P: Pause | ESC: Menu", True, (255, 255, 255))
    controls_shadow = font_small.render("SPACE: Jump | P: Pause | ESC: Menu", True, (0, 0, 0))
    controls_rect = controls_text.get_rect(center=(window_w//2, 490))
    controls_shadow_rect = controls_shadow.get_rect(center=(window_w//2 + 1, 491))
    screen.blit(controls_shadow, controls_shadow_rect)
    screen.blit(controls_text, controls_rect)

def draw_game_over():
    """Draw game over screen"""
    # Semi-transparent overlay
    overlay = pygame.Surface((window_w, window_h), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))
    screen.blit(overlay, (0, 0))
    
    # Game Over text - centered
    game_over_text = font_large.render("GAME OVER", True, (255, 100, 100))
    go_shadow = font_large.render("GAME OVER", True, (0, 0, 0))
    go_rect = game_over_text.get_rect(center=(window_w//2, window_h//2 - 80))
    go_shadow_rect = go_shadow.get_rect(center=(window_w//2 + 3, window_h//2 - 77))
    screen.blit(go_shadow, go_shadow_rect)
    screen.blit(game_over_text, go_rect)
    
    # Final score - centered below game over
    score_text = font_medium.render(f"Score: {score}", True, (255, 255, 255))
    score_shadow = font_medium.render(f"Score: {score}", True, (0, 0, 0))
    score_rect = score_text.get_rect(center=(window_w//2, window_h//2 - 20))
    score_shadow_rect = score_shadow.get_rect(center=(window_w//2 + 2, window_h//2 - 18))
    screen.blit(score_shadow, score_shadow_rect)
    screen.blit(score_text, score_rect)
    
    # High score - centered below final score
    hs_text = font_medium.render(f"Best: {high_score}", True, (255, 215, 0))
    hs_shadow = font_medium.render(f"Best: {high_score}", True, (0, 0, 0))
    hs_rect = hs_text.get_rect(center=(window_w//2, window_h//2 + 20))
    hs_shadow_rect = hs_shadow.get_rect(center=(window_w//2 + 2, window_h//2 + 22))
    screen.blit(hs_shadow, hs_shadow_rect)
    screen.blit(hs_text, hs_rect)
    
    # Instructions - in footer area
    restart_text = font_small.render("Press SPACE to Restart", True, (255, 255, 255))
    restart_shadow = font_small.render("Press SPACE to Restart", True, (0, 0, 0))
    restart_rect = restart_text.get_rect(center=(window_w//2, 470))
    restart_shadow_rect = restart_shadow.get_rect(center=(window_w//2 + 1, 472))
    screen.blit(restart_shadow, restart_shadow_rect)
    screen.blit(restart_text, restart_rect)
    
    menu_text = font_small.render("Press ESC for Menu", True, (200, 200, 200))
    menu_shadow = font_small.render("Press ESC for Menu", True, (0, 0, 0))
    menu_rect = menu_text.get_rect(center=(window_w//2, 490))
    menu_shadow_rect = menu_shadow.get_rect(center=(window_w//2 + 1, 492))
    screen.blit(menu_shadow, menu_shadow_rect)
    screen.blit(menu_text, menu_rect)

def draw_pause():
    """Draw pause screen"""
    overlay = pygame.Surface((window_w, window_h), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 100))
    screen.blit(overlay, (0, 0))
    
    # Pause text - centered
    pause_text = font_large.render("PAUSED", True, (255, 255, 255))
    pause_shadow = font_large.render("PAUSED", True, (0, 0, 0))
    pause_rect = pause_text.get_rect(center=(window_w//2, window_h//2))
    pause_shadow_rect = pause_shadow.get_rect(center=(window_w//2 + 3, window_h//2 + 3))
    screen.blit(pause_shadow, pause_shadow_rect)
    screen.blit(pause_text, pause_rect)
    
    # Resume instruction - in footer
    resume_text = font_medium.render("Press P to Resume", True, (255, 255, 255))
    resume_shadow = font_medium.render("Press P to Resume", True, (0, 0, 0))
    resume_rect = resume_text.get_rect(center=(window_w//2, 480))
    resume_shadow_rect = resume_shadow.get_rect(center=(window_w//2 + 2, 482))
    screen.blit(resume_shadow, resume_shadow_rect)
    screen.blit(resume_text, resume_rect)

def reset_game():
    """Reset game variables"""
    global score, has_moved, game_state
    score = 0
    has_moved = False
    game_state = PLAYING
    particles.clear()

def main():
    global game_state, score, high_score, has_moved
    
    bg_x_pos = 0
    ground_x_pos = 0
    
    player = Player(168, 300)
    pipes = [Pipe(600, random.randint(50, 200), 180, 2.4)]
    
    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if game_state == PLAYING or game_state == PAUSED:
                        game_state = MENU
                    elif game_state == GAME_OVER:
                        game_state = MENU
                elif event.key == pygame.K_SPACE:
                    if game_state == MENU:
                        reset_game()
                        player = Player(168, 300)
                        pipes = [Pipe(600, random.randint(50, 200), 180, 2.4)]
                    elif game_state == PLAYING:
                        has_moved = True
                        player.jump()
                    elif game_state == GAME_OVER:
                        reset_game()
                        player = Player(168, 300)
                        pipes = [Pipe(600, random.randint(50, 200), 180, 2.4)]
                elif event.key == pygame.K_p and game_state == PLAYING:
                    game_state = PAUSED
                elif event.key == pygame.K_p and game_state == PAUSED:
                    game_state = PLAYING
        
        # Update game logic
        if game_state == PLAYING:
            if has_moved:
                player.update()
                
                # Collision detection
                player_rect = pygame.Rect(player.x, player.y, 
                                        player_img.get_width(), player_img.get_height())
                
                collision = False
                for pipe in pipes:
                    pipe_width = pipe_up_img.get_width()
                    pipe_top_height = pipe.height
                    pipe_gap = pipe.gap
                    pipe_bottom_y = pipe_top_height + pipe_gap
                    
                    pipe_top_rect = pygame.Rect(pipe.x, 0, pipe_width, pipe_top_height)
                    pipe_bottom_rect = pygame.Rect(pipe.x, pipe_bottom_y, 
                                                 pipe_width, window_h - pipe_bottom_y)
                    
                    if (player_rect.colliderect(pipe_top_rect) or 
                        player_rect.colliderect(pipe_bottom_rect)):
                        collision = True
                        break
                
                # Ground and ceiling collision
                if player.y < -32 or player.y > 520:
                    collision = True
                
                if collision:
                    create_explosion(player.x + player_img.get_width()//2,
                                   player.y + player_img.get_height()//2,
                                   (255, 100, 100))
                    if slap_sfx:
                        pygame.mixer.Sound.play(slap_sfx)
                    high_score = max(high_score, score)
                    game_state = GAME_OVER
                
                # Update pipes
                for pipe in pipes:
                    pipe.update()
                
                # Remove off-screen pipes and add new ones
                if pipes[0].x < -pipe_up_img.get_width():
                    pipes.pop(0)
                    new_height = random.randint(50, 200)
                    pipes.append(Pipe(400, new_height, 180, 2.4))
                
                # Score checking
                for pipe in pipes:
                    if not pipe.scored and pipe.x + pipe_up_img.get_width() < player.x:
                        score += 1
                        pipe.scored = True
                        pipe.highlight = True
                        if score_sfx:
                            pygame.mixer.Sound.play(score_sfx)
                        
                        # Score particles
                        create_explosion(pipe.x + pipe_up_img.get_width()//2, 
                                       window_h//2, (255, 255, 0))
            else:
                player.update()  # For bobbing animation
            
            # Background scrolling
            bg_x_pos -= bg_scroll_spd
            ground_x_pos -= ground_scroll_spd
            
            if bg_x_pos <= -bg_width:
                bg_x_pos = 0
            if ground_x_pos <= -bg_width:
                ground_x_pos = 0
        
        # Update particles regardless of game state
        update_particles()
        
        # Drawing
        if game_state == MENU:
            draw_menu()
        else:
            # Draw game background
            screen.fill((135, 206, 235))
            screen.blit(bg_img, (bg_x_pos, 0))
            screen.blit(bg_img, (bg_x_pos + bg_width, 0))
            screen.blit(ground_img, (ground_x_pos, 532))
            screen.blit(ground_img, (ground_x_pos + bg_width, 532))
            
            # Draw game objects
            for pipe in pipes:
                pipe.draw()
            
            player.draw()
            scoreboard()
            
            # Draw particles
            draw_particles()
            
            # Draw UI overlays
            if game_state == GAME_OVER:
                draw_game_over()
            elif game_state == PAUSED:
                draw_pause()
        
        pygame.display.flip()
        clock.tick(fps)

if __name__ == "__main__":
    main()
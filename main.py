import pygame, random, time

pygame.init()

clock = pygame.time.Clock()
FPS = 60

width = 1400
height = 700
dim = (width, height)
screen = pygame.display.set_mode(dim)
pygame.display.set_caption("Space Shooter")
laserBeam = pygame.image.load("laser.png")
bg = pygame.image.load("background.jpg").convert()
bg_width = bg.get_width()
font = pygame.font.Font("font.ttf" , 32)
font2 = pygame.font.Font("font.ttf" , 20)

starwarsyellow = (255, 232, 31)
abuAbu = (36, 36, 36)

class Bullet:
    def __init__(self, x, y):
        self.image = laserBeam  
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.velocity = 10  
        self.active = True
    def checkCollision(self , enemy_rect):
        if self.active and self.rect.colliderect(enemy_rect):
            self.active = False
            return True
        return False
    

spaceship = pygame.image.load("spaceship1.png")
spaceship = pygame.transform.rotate(spaceship , -90)
spaceship_rec = spaceship.get_rect()
spaceship_rec.centery = height // 2
spaceship_rec.left = 100

score = 0
score_text = font.render("Score : " + str(score), True, starwarsyellow)
gameoverScore = font2.render("Score : " + str(score), True, starwarsyellow)
gameoverScore_rect = gameoverScore.get_rect()
score_rec = score_text.get_rect()
score_rec.left = 20
score_rec.top = 7

title_text = font.render("Space Shooter" , True, starwarsyellow)
title_rec = title_text.get_rect()
title_rec.centerx = width // 2
title_rec.centery = 30

gameover_text = font2.render("Gameover" , True , starwarsyellow)
gameover_rec = gameover_text.get_rect()
gameover_rec.centerx = width // 2
gameover_rec.centery = 750

lives = 3
lives_text = font.render("Lives : " + str(lives) ,True, starwarsyellow)
lives_rec = lives_text.get_rect()
lives_rec.left = 1180
lives_rec.top = 7 

laserSound = pygame.mixer.Sound("pop.mp3")
explosionSound = pygame.mixer.Sound("boom.mp3")

enemySpaceship = pygame.image.load("opp_spaceship.png")
enemySpaceship = pygame.transform.rotate(enemySpaceship , 90)
enemySpaceship_rec = enemySpaceship.get_rect()
enemySpaceship_rec.center = (width + 100, random.randint(110, height - 80))
enemySpaceship_active = True


def reset_enemy_spaceship():
    global enemySpaceship_rec , enemySpaceship_active
    enemySpaceship_rec.center = (width + 100, random.randint(110, height - 80))
    enemySpaceship_active = True



bullets = []
scroll = 0
scroll_speed = 30 
VELOCITY = 5 
gameOver = False
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = Bullet(spaceship_rec.centerx, spaceship_rec.centery)
                bullets.append(bullet)
                laserSound.play()
    for bullet in bullets:
        if bullet.active:
            bullet.rect.x += bullet.velocity
            if bullet.rect.right > width:
                bullet.active = False
            if bullet.rect.right > width:
                bullet.active= False    
        
            if enemySpaceship_active and bullet.checkCollision(enemySpaceship_rec):
                score += 100 
                enemySpaceship_active = False
                explosionSound.play()
            
    if not enemySpaceship_active:
        reset_enemy_spaceship()
        enemySpaceship_active = True

    if enemySpaceship_active:
        enemySpaceship_rec.centerx -= VELOCITY
    
    if enemySpaceship_rec.x < 0 :
        enemySpaceship_rec.center = (width + 100, random.randint(110, height - 80))

    if spaceship_rec.colliderect(enemySpaceship_rec):
        lives -= 1 
        enemySpaceship_rec.center = (width + 100, random.randint(110, height - 80))
        explosionSound.play()
        

    scroll -= scroll_speed
    if scroll <= -bg_width:
        scroll = 0
                
    screen.blit(bg, (scroll, 0))
    screen.blit(bg, (scroll + bg_width, 0))
    screen.blit(spaceship , spaceship_rec)
    screen.blit(score_text , score_rec)
    screen.blit(title_text , title_rec)
    screen.blit(lives_text , lives_rec)
    screen.blit(enemySpaceship , enemySpaceship_rec)
    
    score_text = font.render("Score : " + str(score), True, starwarsyellow)
    lives_text = font.render("Lives : " + str(lives) ,True, starwarsyellow)
    

    for bullet in bullets:
        if bullet.active:
            screen.blit(bullet.image, bullet.rect)


    


    keys = pygame.key.get_pressed()

    if keys[pygame.K_a] and spaceship_rec.left > 0:
        spaceship_rec.x -= VELOCITY 
    if keys[pygame.K_d] and spaceship_rec.right > 0:
        spaceship_rec.x += VELOCITY 
    if keys[pygame.K_w] and spaceship_rec.top > 80:
        spaceship_rec.y -= VELOCITY 
    if keys[pygame.K_s] and spaceship_rec.bottom < height:
        spaceship_rec.y += VELOCITY 

    if lives == 0:
        gameOver = True
                            
    if gameOver:  
        rect_surface = pygame.Surface((400 , 300))
        rect_surface.fill(abuAbu)
        rect_surface.set_alpha(200)

        rect_surface_rect = rect_surface.get_rect()
        rect_surface_rect.center = (width // 2 , height // 2)
        screen.blit(rect_surface , rect_surface_rect)

        gameover_text = font2.render("Gameover " , True , starwarsyellow)
        gameover_rec.center = rect_surface_rect.center
        screen.blit(gameover_text , gameover_rec)

        gameoverScore = font2.render("Score : " + str(score), True, starwarsyellow)
        gameoverScore_rect.centerx
        gameoverScore_rect.y = 400
        screen.blit(gameoverScore, gameoverScore_rect)

        pygame.display.update() 

        pausing = True
        while pausing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pausing = False
                    runing = False
                    

                if event.type == pygame.KEYDOWN:
                    running = True
                    pausing = False
                    gameOver = False
                    lives = 3
                    score = 0 
                    spaceship_rec.centery = height // 2
                    spaceship_rec.left = 100












    pygame.display.update()

pygame.quit()
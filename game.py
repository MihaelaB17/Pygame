import pygame
import random
import time

#init window
pygame.init()
WIDTH = 800
HEIGHT = 600
black=(0,0,0)
gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT)) # dimensiunea ferestrei
pygame.display.set_caption('TypeSpeed') # numele jocului
background = pygame.image.load('key.png')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))  #scale image 
font = pygame.font.Font('comic.ttf', 40)

word_speed = 0.5
f = open("highscore.txt", "r")
highscore = f.read()
nr_highscore = int(highscore)
f.close()
score = 0
scor_nou = 0 # se face 1 daca se inregistreaza high score
nr_cuv = 0

# functie care ia un cuvant random din fisierul words.txt
def new_word():
    global nr_cuv, displayword, yourword, x_cor, y_cor, word_speed
    x_cor = random.randint(250,700)     # coord x random
    y_cor = 200  # inaltimea de unde porneste cuvantul
    words = open("words.txt").read().split('\n')
    yourword = ''
    displayword = random.choice(words) # cuvant random din fisier
    while 1:
        if nr_cuv < 6:
            if len(displayword)<6:
                break
            else:
                displayword = random.choice(words)
        elif nr_cuv < 16:
            if len(displayword)>=6 and len(displayword)<9:
                break
            else:
                displayword = random.choice(words)
        else:
            if len(displayword)>=9:
                break
            else:
                displayword = random.choice(words)
    if nr_cuv < 19: # primele 16 cuvinte vor fi usoare dar va creste viteza; dupa vor veni cuvinte mai lungi
        word_speed += 0.10
    nr_cuv += 1
new_word()


#function to draw text
font_name = pygame.font.match_font('comic.ttf')
def draw_text(display, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, black)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    gameDisplay.blit(text_surface, text_rect)

 
#function to show front screen and gameover screen
def game_front_screen():
    gameDisplay.blit(background, (0,0))
    if not game_over :
        draw_text(gameDisplay, "GAME OVER!", 90, WIDTH / 2, HEIGHT / 4)
        draw_text(gameDisplay,"Score : " + str(score), 70, WIDTH / 2, HEIGHT /2)
        if scor_nou == 1:
            s= "NEW HighScore: "
        else:
            s="HighScore: "
        draw_text(gameDisplay,s + str(nr_highscore), 70, WIDTH/2, HEIGHT/1.5)
    else:
        draw_text(gameDisplay, "Press a key to begin!", 54, WIDTH / 2, 200)
    pygame.display.flip()
    # se asteapta input de la user la inceperea jocului (orice tasta)
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

#main loop
game_over = True
game_start = True
while True:
    if game_over:
        if game_start:
            game_front_screen()
        game_start = False
    game_over = False

    
    background = pygame.image.load('bg_img.jpg')
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    plat = pygame.image.load('platform3.png')
    plat = pygame.transform.scale(plat, (90,50))


    gameDisplay.blit(background, (0,0))

    y_cor += word_speed # "cade" cuvantul
    gameDisplay.blit(plat,(x_cor-50,y_cor+15))
    draw_text(gameDisplay, str(displayword), 40, x_cor, y_cor)
    draw_text(gameDisplay, 'Score: '+str(score), 40, WIDTH/2 , 25)

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            yourword += pygame.key.name(event.key)

            if displayword.startswith(yourword):
                if displayword == yourword:
                    score += len(displayword)
                    new_word()
            else:
                if score > nr_highscore:
                    scor_nou = 1
                    nr_highscore = score
                    f = open("highscore.txt","w")
                    f.write(str(score))
                game_front_screen()
                time.sleep(2)
                pygame.quit()
                
    if y_cor < HEIGHT-5:
        pygame.display.update()
    else:
        if score > nr_highscore:
            scor_nou = 1
            nr_highscore = score
            f = open("highscore.txt","w")
            f.write(str(score))
        game_front_screen()
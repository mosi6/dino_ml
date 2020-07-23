import pygame
import random
import time
import dino

speed = 50
dinos = 100
pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)
WHITE = (255,255,255)
BLACK = (0,0,0)
screen = pygame.display.set_mode((500, 500))
dinolst = [0 for jg in range(dinos)]
highscore = 0
for j in range(dinos):
    n = dino.generate()
    dinolst[j] = dino.dino(n[0],n[1])
for _ in range(10000):
    not_pasul = [True for k in range(dinos)]
    jumping = [False for l in range(dinos)]
    crouch = False
    cactus_list = []
    jump = [0 for p in range(dinos)]
    v_jump = [0.1 * speed for u in range(dinos)]
    g = 1/15000 * speed ** 2
    cactus_t = 0
    dtc = 0
    cactus_size = 0
    cactus_height = 0
    jumped =[False for k in range(dinos)]
    score = [0 for q in range(dinos)]
    texts = myfont.render(str(_), False, (0, 0, 0))
    textsurface = myfont.render(str(highscore), False, (0, 0, 0))
    while True in not_pasul:
        textscore = myfont.render(str(max(score)),False,(0,0,0))
        if max(score)>highscore:
            highscore = max(score)
        #controls for humans
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Usually wise to be able to close your program.
                exit()
                #not_pasul = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and not jumping:
                    jumping = True
        crouch = pygame.key.get_pressed()[pygame.K_DOWN]
        #cactus spawning
        if cactus_t <= 0:
            cactus_t = 3 + random.uniform(0,2)
            cactus_list.append([550,random.choice([10,20,60]),True if random.random()>1 else False,random.choice([400,450])])
        else:
            cactus_t -= 0.001 * speed
        #distance to next cactus
        if cactus_list[0][0] < 0:
            dtc = cactus_list[1][0] - 50
            cactus_size = cactus_list[1][1]
            cactus_height = 0 if cactus_list[1][2] and cactus_list[1][3]==400 else 1

        else:
            dtc = cactus_list[0][0] - 50
            cactus_size = cactus_list[0][1]
            cactus_height = 0 if cactus_list[0][2] and cactus_list[0][3]==400 else 1
        for e in range(dinos):
            if not jumping[e]:
                jumping[e] = dinolst[e].step(450/(dtc+0.01),cactus_size/60,cactus_height)
        #height of players
        for d in range(dinos):
            if jumping[d]:
                #if crouch:
                #    jump += v_jump - 0.1 * speed
                #else:
                jump[d] += v_jump[d]
                v_jump[d] -= g
                if jump[d] <= 0:
                    jumping[d] = False
                    jump[d] = 0
                    v_jump[d] = 0.1 * speed

        #player losing logic(writing just the logic for cacti and not birds)
        if (cactus_list[0][0] <= 60 and cactus_list[0][0] + cactus_list[0][1] >= 50):
            for s in range(dinos):
                if jump[s] < 30 and not_pasul[s] and not cactus_list[0][2]:
                    not_pasul[s] = False
                elif cactus_list[0][2] and cactus_list[0][3] == 400 and jump[s]>=38:
                    not_pasul[s] = False
                elif cactus_list[0][2] and cactus_list[0][3] ==450 and jump[s]>=0 and jump[s]<=30:
                    not_pasul[s] = False
        if (int(cactus_list[0][0]+cactus_list[0][1])==50) and not cactus_list[0][2]:
            for a in range(dinos):
                if not_pasul[a] and not jumped[a]:
                    score[a]+=1
                    jumped[a] = True
        elif cactus_list[0][2] and cactus_list[0][3]==400 and int(cactus_list[0][0]+30)==50:
            for b in range(dinos):
                if not_pasul[b] and not jumped[b]:
                    score[b]+=1
                    jumped[b]=True
        elif cactus_list[0][2] and cactus_list[0][3]==450 and int(cactus_list[0][0]+30)==50:
            for c in range(dinos):
                if not_pasul[c] and not jumped[c]:
                    score[c]+=1
                    jumped[c]=True


        screen.fill((255,255,255))
        #despawning cacti and drawing them
        if cactus_list[0][0] < -60:
            cactus_list.remove(cactus_list[0])
            jumped = [False for k in range(dinos)]
        for i in range(len(cactus_list)):
            if cactus_list[i][2]:
                pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(cactus_list[i][0], cactus_list[i][3], 30, 12))
            else:
                pygame.draw.rect(screen, (255,0,0), pygame.Rect(cactus_list[i][0], 450, cactus_list[i][1], 30))
            cactus_list[i][0] -= 0.05 * speed

        #drawing player
        #if crouch:
        #    pygame.draw.rect(screen, BLACK, pygame.Rect(50, 465 - jump, 20, 15))
        for v in range(dinos):
            if not_pasul[v]:
                pygame.draw.rect(screen,BLACK,pygame.Rect(50,450-jump[v],10,30))
        screen.blit(textscore,(250,50))
        screen.blit(texts,(50,50))
        screen.blit(textsurface,(450,50))
        pygame.display.flip()



    dinolst = dino.evolve(dinolst,score,dinos)

import pygame
from pygame.locals import *
import random
from pylab import math
from pylab import loadtxt

#Starter programmer
pygame.init()

#Skjermen
bredde = 800
høyde = 600
vindu = pygame.display.set_mode((bredde, høyde), RESIZABLE)
pygame.display.set_caption("Space invaders")


#Farger
YELLOW = (255, 255,0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


#Bakgrunn
bg = pygame.image.load("./assets/sort-bakgrunn.png")
bg = pygame.transform.scale(bg, (bredde, høyde))
start_bg = pygame.image.load("./assets/startbilde.png")
start_bg = pygame.transform.scale(start_bg, (bredde,høyde))


#Lager spiller
SPILLER = pygame.image.load("./assets/gul-skip.png")
spillerx = 370
spillery = 470
vindu.blit(SPILLER, (spillerx, spillery))
spillerx_forandring = 0
fart = 8 #Hastighet til spiller


#Laseren   ready = du kan ikke se laseren,  fire = du kan se laseren
SPILLERLASER = pygame.image.load("./assets/gul-laser.png")
laserx = 0
lasery = 480
laserx_forandring = 0
lasery_forandring = 20  #Hastighet til laser
lasertid = "ready"

#Fienden
fiende_nummer = 6
fiende_fart = 1
ROMVESEN = pygame.image.load("./assets/slemming.png")
ROMVESEN = pygame.transform.scale(ROMVESEN, (60,60))
fiendeImg = []
fiendex = []
fiendey = []
fiendex_forandring =[]
fiendey_forandring = []

"""for i in range(fiende_nummer):
    fiendeImg.append(ROMVESEN)
    fiendex.append(random.randint(0, bredde-40))
    fiendey.append(random.randint(50,150))
    fiendex_forandring.append(fiende_fart)
    fiendey_forandring.append(40)
"""


 #Score og level
score_value = 0
level_nå = 0
leveler = 10



def sjekk_high_score(poeng):  #Funksjon for å lage ny hugh_score på dokument
    if poeng > int(high_score):
        fil = open("./assets/poeng.txt","w")
        fil.write(str(poeng))
        fil.close()
        


def fiende(x,y,i):  #For å plassere og oppdatere posisjon til fienden på skjermen
    vindu.blit(fiendeImg[i], (x,y))

def spiller(x,y):  #For spiller på skjermen
    vindu.blit(SPILLER, (x,y))

def skyt_laser(x,y):  #For å skyte laser fra x-posisjon og y-endring
    global lasertid
    lasertid = "fire"
    vindu.blit(SPILLERLASER, (x,y+10))
    
def hviskollisjon(fiendex,fiendey,laserx,lasery):  #Funksjon for å sjekke om laser treffer romvesen
#Matematisk formel som sjekker om x,- og y -kordinatene til romvesen og laser er mindre enn en viss avstand fra hverandre
    avstand = math.sqrt(math.pow(fiendex-(laserx+30), 2) + (math.pow(fiendey-(lasery+40),2)))  
    if avstand < 27:
        return True
    else:
        return False


def skriv(t,størrelse,x,y,farge):   #Skriving på skjerm
    fontObj = pygame.font.Font(None, størrelse)  
    tekstFlateObj = fontObj.render(t, True, farge)  
    tekstRectObj = tekstFlateObj.get_rect()
    tekstRectObj.left = x
    tekstRectObj.top = y
    vindu.blit(tekstFlateObj, tekstRectObj)  #Sette teksten på skjermen

def ny_runde():  #Lager nye romvesen for hvert "spill"
    fiendeImg.clear()  #Fjerner alt innhold i romvesenlistene
    fiendex.clear()
    fiendey.clear()
    fiendex_forandring.clear()
    fiendey_forandring.clear()
    for i in range(fiende_nummer): #Lager nye romvesen og posisjoner
        fiendeImg.append(ROMVESEN)
        fiendex.append(random.randint(0, bredde-40))
        fiendey.append(random.randint(50,150))
        fiendex_forandring.append(fiende_fart)
        fiendey_forandring.append(40)
    



main = True  
intro = True
kjører = False

    
while main:  #Loop for hele programmet
    for e in pygame.event.get():  #For å lukke programmet
            if e.type == pygame.QUIT:
                pygame.quit()
    #High score oppdatering
    high_score_fil = open("./assets/poeng.txt","r")
    high_score = high_score_fil.read()
    
    
    #Introskjerm for spillet
    while intro:
        vindu.blit(start_bg, (0,0))
        skriv("v2",50,600,200,YELLOW)
        skriv("Av Jesper Vigtel Hølland", 30,550,10,WHITE)
        skriv("High score: "+high_score, 50,10,10, WHITE)
        skriv("Obs: Du bruker piltaster til bevegelse og mellomromsttast til skyting", 30,10,570,YELLOW)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                kjører = True
                intro = False
                
        pygame.display.update()
   
    ny_runde()  #Lager nye romvesen for hver runde
    fiende_fart = 1  
    score_value = 0
    
    #Koden for spillet
    while kjører:
        
        #Settter bakgrunnbilde
        vindu.blit(bg, (0,0))
        #Knapper som trykkes
        for e in pygame.event.get():
            
            if e.type == pygame.QUIT:  
                pygame.quit()
            
            if e.type == pygame.KEYDOWN:       
    #Bevegelser for spiller, piltaster
                if e.key == pygame.K_LEFT:  #For bevege deg mot venstre
                    spillerx_forandring = -fart
                if e.key == pygame.K_RIGHT:#For å bevege deg mot høyre
                   spillerx_forandring = fart
    #Skyting          
                if e.key == pygame.K_SPACE:
                    if lasertid == "ready":  #Sjekker om laseren er klar for å skytes
                        laserx = spillerx   #finner posisjonen til romskipet
                        skyt_laser(laserx,lasery)  #Skjører funksjon for å skyte laser
                        
            if e.type == pygame.KEYUP:  
                if e.key == pygame.K_LEFT or e.key == pygame.K_RIGHT: #Når man slipper piltast slutter romskip å bevege seg
                    spillerx_forandring = 0
            
    #Spillerbevegelser etter piltast
        spillerx += spillerx_forandring  
    #Begrensninger for bevegelsene til spilleren
        if spillerx <= 0:
            spillerx = 0
        if spillerx >= bredde-100:
            spillerx = bredde-100
       
     
    #Fiendebevegelse (gjøres for alle antall romvesen)
        for i in range(fiende_nummer):  
            
            if fiendey[i] > 440:   #spillet er over når romvesenet når en viss y-verdi på skjermen
                for j in range(fiende_nummer):
                    fiendey[j] = 2000
                    skriv("Game over",100, 200, høyde/2 , YELLOW)
                    skriv("Press på skjermen for å gå tilbake", 40, 160,400, WHITE)
                    sjekk_high_score(score_value)  #Sjekker scoren din mot high_scoren
                    
                    for e in pygame.event.get(): #Avslutter "spillskjermen" og fører deg tilbake til introskjermen
                        if e.type == pygame.MOUSEBUTTONDOWN:
                            kjører = False
                            intro = True
                    
             
            fiendex[i] += fiendex_forandring[i]     #Kontinuerlig bevegelse av romvesenet, med en viss fart
            if fiendex[i] <= 0:  #Når den treffer en vegg, går den ned og får samme fart motsatt vei
                fiendex_forandring[i] = fiende_fart
                fiendey[i] += fiendey_forandring[i]    
            elif fiendex[i] >= bredde-60:
                fiendex_forandring[i] = -fiende_fart
                fiendey[i] += fiendey_forandring[i]
                
        #Kollisjon laser og fiende    
            if hviskollisjon(fiendex[i], fiendey[i], laserx, lasery):
                lasery = 480  #Oppdaterer lasertilstand
                lasertid = "ready"
                score_value += 1
                fiendex[i] = random.randint(0, bredde-60) #Ny romvesenposisjon
                fiendey[i] = random.randint(50,150)
            
            fiende(fiendex[i], fiendey[i], i)
            
              
    #Laser bevegelse
        if lasery <= 0:  #Når laseren når toppen av skjermen, går den ned, og blir klar til å skytes
            lasery = 480
            lasertid = "ready"
            
        if lasertid == "fire":   #Når laseren skytes, og beveger seg oppover
            skyt_laser(laserx,lasery)
            lasery -= lasery_forandring
        
        for i in range (1,leveler+1): #Øker farten til romvesener for hver 6. skutt. (levelup)
            if score_value == i*6:
                fiende_fart = i
                skriv("Level "+str(i)+" Farten øker!",30,10,40,WHITE) 
                level_nå = i
                
               
            
        
        #Poeng/score
        skriv("Level: "+ str(level_nå),40,650,10,WHITE)
        skriv("Poeng: " + str(score_value),40,10,10,WHITE)
        skriv("High score: "+ high_score, 30,300,10, WHITE)
        spiller(spillerx,spillery)   
        pygame.display.update()
    
    

        

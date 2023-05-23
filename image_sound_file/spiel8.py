import pygame
import sqlite3
import sys
from pygame.locals import *
from datetime import datetime

width = 1200
height = 800
screen = pygame.display.set_mode((width, height))

pygame.font.init()

class Level:
    def __init__(self, level_id,sequence,duration_ms):
        self.level_id = level_id
        self.sequence = sequence
        self.duration_ms = duration_ms

class Highscore:
    def __init__(self,highscore_id, name,date, level_id):
        self.highscore_id = highscore_id
        self.name = name
        self.date = date
        self.level_id = level_id


class ORM:
    def __init__(self, file_name):
        self.connection = sqlite3.connect(file_name)
        self.cursor = self.connection.cursor()

    def get_levels(self):
        levels2 = []
        sequencen = []
        
        self.response = self.cursor.execute('''SELECT * FROM level''')
       
        for item in self.response:
            
            neu_level= Level(item[(0)],item[(1)],item[(2)])
            levels2.append(neu_level.sequence.split(","))
        
        #levels2 = levels[0].sequence.split(","), levels[1].sequence.split(","), levels[2].sequence.split(","), levels[3].sequence.split(","), levels[4].sequence.split(","), levels[5].sequence.split(","), levels[6].sequence.split(","), levels[7].sequence.split(","),levels[8].sequence.split(","),levels[9].sequence.split(",")
        for leveln in levels2:
             
             for sequence in leveln:
                  sequencen.append(int(sequence))
        
        return sequencen
            
    def get_highscores(self):
        highscores = []
        response1 = self.cursor.execute('''SELECT * FROM highscore ORDER BY level_id DESC''')

        for item in response1:
            neu_highscore = Highscore(item[0],item[1],item[2], item[3])
            highscores.append(neu_highscore)  
        return highscores
    
    def save_highscore(self, highscore):
        date = highscore.date
        name = highscore.name
        level_id = highscore.level_id
        sql = f"""INSERT INTO highscore(name, date, level_id) VALUES
        ("{name}","{date}",{level_id})
      """
        
        self.cursor.execute (sql)
        self.cursor.connection.commit()


class alien:
    def __init__(self, image, scalex, scaley, rect_x, rect_y, leben):
        self.image = image
        self.alien = pygame.image.load(self.image).convert_alpha()
        self.alien = pygame.transform.scale(self.alien,(scalex,scaley))
        self.leben = leben
        self.rect = self.alien.get_rect()
        self.rect.x = rect_x
        self.rect.y = rect_y
        self.pruf = True
        self.speed = 5 
    
    
    def alien_bewegungen(self):
        self.rect.x += self.speed        
        if self.rect[0] == 160:
            self.speed = 0
            self.rect.y -= 5
            if self.rect[1] == 380:
                self.alien = pygame.transform.rotate(self.alien, 90) # Drehung um 90 Grad im Uhrzeigersinn
                self.rect = self.alien.get_rect(center=self.rect.center)
        if self.rect[1] == 165:
            self.speed = 5
            if self.rect[0] == 380:
                self.alien = pygame.transform.rotate(self.alien, 270) # Drehung um 270 Grad im Uhrzeigersinn
                self.rect = self.alien.get_rect(center=self.rect.center)
            if self.rect[0] == 180:
                self.alien = pygame.transform.rotate(self.alien, 270) 
                self.rect = self.alien.get_rect(center=self.rect.center)
        if self.rect[0] == 400:
            self.speed = 0
            self.rect.y += 5
            if self.rect[1] == 470:
                self.alien = pygame.transform.rotate(self.alien, 90) 
                self.rect = self.alien.get_rect(center=self.rect.center)
        if self.rect[1] == 490:
            self.speed = 5
            if self.rect[0] == 720:
                self.alien = pygame.transform.rotate(self.alien, 90) 
                self.rect = self.alien.get_rect(center=self.rect.center)
        if self.rect[0] == 720:
            self.speed = 0
            self.rect.y -= 5
            if self.rect[1] == 325:
                self.alien = pygame.transform.rotate(self.alien, 270) 
                self.rect = self.alien.get_rect(center=self.rect.center)
            if self.rect[1] == 325:
                self.speed = 5
             
class defenders:
    def __init__(self, image,scalex, scaley, dauer, dmg):
        self.image = image
        self.scalex = scalex
        self.scaley = scaley
        self.dauer = dauer
        self.dmg = dmg
        self.defender = pygame.image.load(image).convert_alpha()
        self.defender = pygame.transform.scale(self.defender,(scalex,scaley))
        self.rect = self.defender.get_rect()
        self.rect.x = 10000
        self.creation_time = pygame.time.get_ticks()
        self.dauer = dauer
        self.leben2 = 80
        self.circles = []
        self.defender_surface = pygame.Surface((scalex, scaley))
        self.neue_richtung = "links"
        pygame.mixer.init()
        self.sound4 = pygame.mixer.Sound("leser3.mp3")
        self.sound4.set_volume(0.1)
        self.rotat_pruf = True
        self.rotat_pruf2 = False
        
    
        
        
class Game:
    def __init__(self):
        self.geld = 1000
        self.font = pygame.font.SysFont('Stencil', 30)
        
        self.background_image = pygame.image.load('background.png')
        self.background_image = pygame.transform.scale(self.background_image, (width, height))
        self.defenders5 = pygame.image.load('defender3 .2.png')
        self.defenders5 = pygame.transform.scale(self.defenders5, (70,70))
        self.defenders7 = pygame.image.load('defender1.2.png')
        self.defenders7 = pygame.transform.scale(self.defenders7, (70,70))
        self.defenders6 = pygame.image.load('defender2 .2.png')
        self.defenders6 = pygame.transform.scale(self.defenders6, (60,60))
        
        
        self.alien1 = [alien("alien2.png", 70, 70, 0, 400,50), alien("alien3.png", 70, 70, 0, 400,100), alien("alien4.png", 70, 70, 0, 400,200)]
        #self.defender = defenders("defender.1.png", 100, 80, 20)
        self.aliens = []
        self.defenders = []
        self.defenders2 = [defenders("defender2.png",50, 50, 20000, 50), defenders("defender3.png",70, 70, 20000,100), defenders("defender1.png",70, 70, 20000, 200)]
        self.defenders3 = [defenders("defender1.png",70, 70, 20000, 200)]
        self.display_message = False
        self.display_message2 = [pygame.time.get_ticks(), 3000, True]
        self.invisible_rect_list = [pygame.Rect(720, 320, 480, 80),pygame.Rect(720, 400, 80, 160),pygame.Rect(480, 480, 240, 80),pygame.Rect(400, 165, 80, 390),pygame.Rect(160, 165, 240, 80),pygame.Rect(160, 245, 80, 240),pygame.Rect(0, 400, 160, 80), pygame.Rect(200, 660, 265, 95)]
        self.display_message_timer =0
        self.text3 = self.font.render('Du kanst nicht ein defender nicht hier platzieren', True, (255, 255, 255))
        
        self.defenders3 = [defenders("defender1.png",70, 70, 20000, 200)]
        self.defenders4 = [defenders("defender2.png",50, 50, 20000, 50)]
       
        self.check_bool = []
        self.leser = [pygame.image.load("1.1.png"), pygame.image.load("1.2.png")]
        self.leser11 = [pygame.image.load("1.1.png"), pygame.image.load("1.2.png")]
        self.leser2 = [pygame.image.load("2.1.png"), pygame.image.load("2.2.png")]
        self.leser3 = [pygame.image.load("3.1.png"), pygame.image.load("3.2.png")]
        self.frame = 0
        self.highscore_list = []
        
    def check_collision1(self, defender, alien):  
            if defender.colliderect(alien.rect):
                return True
            return False
                   
   
    def add_circle(self, x, y, radius):
        if self.defenders:
            for defender in self.defenders:
                circle = pygame.draw.circle(screen, (255, 0, 0, 0), (x, y), radius)
                defender.circles.append(circle)

    
    
        
    def check_collision(self, defender_rect):
        for rect2 in self.invisible_rect_list:
            #pygame.draw.rect(screen, (255, 0, 0), rect2)
            if defender_rect.colliderect(rect2):
                self.display_message_timer = pygame.time.get_ticks() + 5000
                return True
        return False


    
    def run(self):
        invisible_rect_list = [pygame.Rect(720, 320, 480, 80),pygame.Rect(720, 400, 80, 160),pygame.Rect(480, 480, 240, 80),pygame.Rect(400, 165, 80, 390),pygame.Rect(160, 165, 240, 80),pygame.Rect(160, 245, 80, 240),pygame.Rect(0, 400, 160, 80)]
        self.clock = pygame.time.Clock()
        m_pressed = False
        n_pressed = False
        b = False
        ist_schön_da = False
        geld = True
        red = (255, 0, 0)
        self.liste = []
        transparent_gray = (128, 128, 128, 128)
        orm = ORM("ITA21a_Senso")
        pygame.init()
        TIMER_EVENT = pygame.USEREVENT + 3
        pygame.time.set_timer(TIMER_EVENT, 3000)
        sequencen =  [orm.get_levels()]
        level_id = 0
        level_id2 = 0
        
        sound1 = pygame.mixer.music.load("game_music.mp3")
        # Hinweis: Herr Adms dieser sound"Za Warudo" ist von ein Anime charackter und er kann der zeit stoppen :) !
        soundstop = pygame.mixer.Sound("ZaWarudo.mp3")
        soundstop.set_volume(0.2)
        sound2 = pygame.mixer.Sound("error.mp3")
        sound2.set_volume(1.0)
        sound3 = pygame.mixer.Sound("tank1.wav")
        sound3.set_volume(0.3)
        sound12 = pygame.mixer.Sound("Victory Tone.mp3")
        sound6 = pygame.mixer.Sound("GAME OVER.mp3")
        sound13 = pygame.mixer.Sound("Victory.mp3")
        sound5 = pygame.mixer.Sound("GAME OVER MUSIC.mp3")
        pygame.mixer.music.play(1,0.0)
        pygame.mixer.music.set_volume(0.5)
        
        self.verloren = True
        self.leben_spieler = 11
        self.rotate_leser = False
        sound_playing = False
        sound_played = False
        BLACK = (0, 0, 0)

        eingabe1 = ""
        eingabe2 = ""

        save = True
        stop = False
        pruf = False
        pruf2 = False
        pruf3 = True
        start = False
        start2 = True

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif self.leben_spieler <= 0 or level_id2 >= 64:
                     if event.type == KEYDOWN:
                	    
                        if event.key == K_RETURN:
        
                            print("Eingabe:", eingabe1)
                            eingabe1 = ""  
                        elif event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
                            eingabe2  = eingabe1
                        elif event.key == K_BACKSPACE:
                            # Löschen des letzten Zeichens im Text-Buffer
                            eingabe1 = eingabe1[:-1]
                        else:
                
                            eingabe1 += event.unicode

                     
                elif event.type == TIMER_EVENT:
                    for sequence in sequencen:
                        #print(len(sequence))
                        if not level_id2 == 64 and start:
                                level_id2 += 1
                            #print(level_id2)
                        if not level_id > 60 and start:
                            if stop == False:
                                #print(sequence[level_id])
                                if sequence[level_id] == 0:
                                    self.aliens.append(alien("alien2.png", 70, 70, 0, 400, 50))
                                if sequence[level_id] == 1:
                                    self.aliens.append(alien("alien3.png", 70, 70, 0, 400, 100))
                                if sequence[level_id] == 2:
                                    self.aliens.append(alien("alien4.png", 70, 70, 0, 400, 200))
                                level_id += 1
                                #print(level_id)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_k:
                     start = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_s and start:
                     if stop == True:
                          stop = False
                     else: 
                          stop = True
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_n and start and start2:
                    print("n gedrückt")
                    n_pressed = True
                    ist_schön_da = True
                
                elif event.type == pygame.MOUSEBUTTONDOWN and n_pressed == True and ist_schön_da == True:
                        n_pressed = False
                        print("mousge")
                        self.pos = pygame.mouse.get_pos()
                        
                        if self.geld > 0:
                                
                                self.defenders.append(defenders("defender2.png",50, 50, 20000, 1))
                                self.defenders[-1].rect.x = self.pos[0] -35
                                self.defenders[-1].rect.y = self.pos[1] -35
                                geld = True
                                print("defender gespawnt")
                                self.geld -= 100
                                
                                sound3.play()
                                self.add_circle(self.defenders[-1].rect.x +25,self.defenders[-1].rect.y + 25 , 100)
                        else:
                            geld = False    
                            geld += 100
                            ist_schön_da = True
                            self.geld -= 100

            
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_m and start and start2:
                    print("m gedrückt")
                    m_pressed = True
                    ist_schön_da = True
                    
                elif event.type == pygame.MOUSEBUTTONDOWN and m_pressed == True and ist_schön_da == True:
                        m_pressed = False
                        print("mousge")
                        self.pos = pygame.mouse.get_pos()
                        
                        if self.geld >= 350:
                                
                                self.defenders.append(defenders("defender3.png",70, 70, 20000, 2))
                                self.defenders[-1].rect.x = self.pos[0] -35
                                self.defenders[-1].rect.y = self.pos[1] -35
                                geld = True
                                print("defender gespawnt")
                                self.geld -= 350
                                sound3.play()
                                self.add_circle(self.defenders[-1].rect.x +25,self.defenders[-1].rect.y + 25 , 100)
                        else:
                            geld = False    
                            geld += 100
                            ist_schön_da = True
                            


                
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    self.geld += 1000
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_b and start and start2:
                    print("n gedrückt")
                    b = True
                    ist_schön_da = True
                elif event.type == pygame.MOUSEBUTTONDOWN and b == True and ist_schön_da == True:
                        b = False
                        print("mousge")
                        self.pos = pygame.mouse.get_pos()
                        
                        if self.geld > 0:
                                
                                self.defenders.append(defenders("defender1.png",70, 70, 20000, 1))
                                self.defenders[-1].rect.x = self.pos[0] -35
                                self.defenders[-1].rect.y = self.pos[1] -35
                                geld = True
                                print("defender gespawnt")
                                self.geld -= 200
                                sound3.play()
                                self.add_circle(self.defenders[-1].rect.x +25,self.defenders[-1].rect.y + 25 , 100)
                        else:
                            geld = False    
                            geld += 100
                            ist_schön_da = True
                            self.geld -= 100
                screen.fill(BLACK)

       
            self.frame += 1
            if self.frame > 1:
                self.frame = 0
                
        
            screen.blit(self.background_image, (0, 0))       
            condition = True

            if n_pressed:
                circle_surface = pygame.Surface((200, 200), pygame.SRCALPHA) 
                pygame.draw.circle(circle_surface, transparent_gray, (100, 100), 100)
                self.pos = pygame.mouse.get_pos()
                self.defenders2[0].rect.x = self.pos[0] -35
                self.defenders2[0].rect.y = self.pos[1] -35
                    
                    
                screen.blit(circle_surface, (self.defenders2[0].rect.x - 70, self.defenders2[0].rect.y - 70))
                screen.blit(self.defenders2[0].defender, self.defenders2[0].rect)
            if m_pressed:
                circle_surface = pygame.Surface((200, 200), pygame.SRCALPHA) 
                pygame.draw.circle(circle_surface, transparent_gray, (100, 100), 100)
                self.pos = pygame.mouse.get_pos()
                self.defenders2[1].rect.x = self.pos[0] -35
                self.defenders2[1].rect.y = self.pos[1] -35
                    
                    
                screen.blit(circle_surface, (self.defenders2[1].rect.x - 70, self.defenders2[1].rect.y - 70))
                screen.blit(self.defenders2[1].defender, self.defenders2[1].rect)
   
            if b:
                circle_surface = pygame.Surface((200, 200), pygame.SRCALPHA) 
                pygame.draw.circle(circle_surface, transparent_gray, (100, 100), 100)
                self.pos = pygame.mouse.get_pos()
                self.defenders3[0].rect.x = self.pos[0] -35
                self.defenders3[0].rect.y = self.pos[1] -35
                    
                    
                screen.blit(circle_surface, (self.defenders3[0].rect.x - 70, self.defenders3[0].rect.y - 70))
                screen.blit(self.defenders3[0].defender, self.defenders3[0].rect)


            if self.aliens and self.verloren:
                for alien33 in self.aliens:

                    if alien33.rect.x > 1200:
                        self.aliens.remove(alien33)
                        
                    screen.blit(alien33.alien, alien33.rect)
                    if stop == False:
                        alien33.alien_bewegungen()
                        
                    
                for defender1 in self.defenders.copy():
                        
                    for defender2 in self.defenders:
                        if defender1 != defender2 and defender1.rect.colliderect(defender2.rect):
                            defender2.rect.x = 0 + len(self.defenders * 100)
                            defender2.rect.y = 10000
                            self.display_message = True
                            self.display_message_timer = pygame.time.get_ticks() + 3000  # 3000 ms = 3 sec
                            if defender1.image == "defender2.png":
                                self.geld += 100
                            if defender1.image == "defender3.png":
                                self.geld += 350
                            if defender1.image == "defender1.png":
                                self.geld += 200
                            sound2.play()
                            sound3.stop()
                                

            for defender1 in self.defenders:
                if self.check_collision(defender1.rect):
        
                    self.display_message = True
                    self.defenders.remove(self.defenders[-1])
                    
                    if defender1.image == "defender2.png":
                        self.geld += 100
                    if defender1.image == "defender3.png":
                        self.geld += 350
                    if defender1.image == "defender1.png":
                        self.geld += 200
                    sound2.play()
                    screen.blit(self.text3, (0, 0))
                    if self.display_message and pygame.time.get_ticks() < self.display_message_timer:
                        screen.blit(self.text3, (0, 0))
                    sound3.stop()
                
            if self.display_message and pygame.time.get_ticks() < self.display_message_timer:
                screen.blit(self.text3, (0, 0))
                
                    
            else:
                    self.display_message = False

                    self.display_message_timer = 0

            if geld > 0:
                    text_geld = self.font.render(f"Geld: {self.geld}", True, (255, 255, 255))
            else:
                    text_geld = self.font.render(f"Geld: {0}", True, (255, 255, 255))
                    self.geld = 0
                    geld = True
                
            if level_id2 == 55 and start:
                 level_id2 += 1
                 sound13.play()                        

            if self.defenders:
                    
                    for defender8 in self.defenders.copy():
                            screen.blit(defender8.defender, defender8.rect)
                            if self.defenders:
                                        if pygame.time.get_ticks() - defender8.creation_time >= defender8.dauer:
                                                self.defenders.remove(self.defenders[0])
                                        # self.circeles.remove(self.circeles[0])
                                        defender8.image

            if self.defenders:
                        for defender in self.defenders.copy():
                            for invisible_rect in invisible_rect_list:
                                    if self.defenders:
                                            if not pygame.time.get_ticks() - defender.creation_time >= defender.dauer:

                                                defender.leben2 -= 0.01
                                           
                                                leben_rect = pygame.Rect(defender.rect[0]+10, defender.rect[1] + 60, defender.leben2, 5)
                                                pygame.draw.rect(screen, red, leben_rect)
                                                self.liste.append("1")
                            if self.geld < 0:
                                text = self.font.render('Not enough money to buy defenders!', True, (255, 255, 255))
                                screen.blit(text, (0,500))
                                self.geld = 0
                                geld = 0


                        for alien333 in self.aliens:
                            for defender in self.defenders:     
                                if self.check_collision1(defender.circles[0], alien333):
                                        
                                        if stop == True:
                                            defender.sound4.stop()
                                        if defender.image == "defender3.png" and stop == False:
                                            defender.sound4.play()
                                            self.leser2[self.frame] = pygame.transform.scale(self.leser2[self.frame],(80,30))
                                            screen.blit(self.leser2[self.frame], (defender.rect.x -70,defender.rect.y + 5))
                                            screen.blit(self.leser2[self.frame], (defender.rect.x -70,defender.rect.y + 30))
                                        if defender.image == "defender1.png" and stop == False:
                                            self.leser3[self.frame] = pygame.transform.scale(self.leser3[self.frame],(80,30))
                                            screen.blit(self.leser3[self.frame], (defender.rect.x -70,defender.rect.y + 17))
                                            defender.sound4.play()
                                        if defender.image == "defender2.png" and stop == False:
                                            self.leser[self.frame] = pygame.transform.scale(self.leser[self.frame],(80,30))
                                            screen.blit(self.leser[self.frame], (defender.rect.x -80,defender.rect.y + 9))
                                            defender.sound4.play()
                                        
                                        self.check_collision1(defender.circles[0], alien333)
                                        
                                        if stop == False:
                                            alien333.leben -= defender.dmg
                                        if alien333.leben < 0:
                                                if self.aliens:
                                                    print(alien333.image)
                                                    if alien333 in self.aliens:
                                                        self.aliens.remove(alien333)
                                                if alien333.image == "alien2.png":
                                                    pruf2 = True
                                                    sound7 = pygame.mixer.Sound("bom1.mp3")
                                                    sound7.set_volume(0.3)
                                                    self.geld += 50
                                                    
                                                    
                                                if alien333.image == "alien3.png":
                                                    pruf2 = True
                                                    sound7 = pygame.mixer.Sound("bom2.mp3")
                                                    sound7.set_volume(0.3)
                                                    self.geld += 50
                                                    
                                                if alien333.image == "alien4.png":
                                                    pruf2 = True
                                                    sound7 = pygame.mixer.Sound("bom3.mp3")
                                                    sound7.set_volume(0.5)
                                                    self.geld += 50
                                                defender.sound4.stop()
                                   
            
            
            if pruf2 == True:
                sound7.play() 
                pruf2 = False
                
                
            
                                       
            if stop == True:
                if pruf == False:
                    soundstop.play()
                pruf = True
                pygame.mixer.music.pause()
                
            if stop == False and pruf == True:
                 pruf = False
                 soundstop.stop()
                 pygame.mixer.music.unpause()
            for alien3333 in self.aliens:
                    if alien3333.rect.x > 1200:
                        self.leben_spieler -= 1
                

            font = pygame.font.SysFont(None, 30)
            font.set_underline(True)
            self.text_spieler_leben = self.font.render(f"Leben: {self.leben_spieler}HP", True, (255, 255, 255))
            self.text5 = font.render("350", True, (0, 0, 0))
            self.text6 = font.render("M", True, (0, 0, 0))
            self.text7 = font.render("100", True, (0, 0, 0))
            self.text8 = font.render("N", True, (0, 0, 0))
            self.text9 = font.render("200", True, (0, 0, 0))
            self.text10 = font.render("B", True, (0, 0, 0))
            self.text11 = font.render("STOP", True, (0, 0, 0))
            self.text12 = font.render("CONTINUE", True, (0, 0, 0))
            self.text13 = font.render("S: STOP/CONTINUE", True, (0, 0, 0))
            screen.blit(self.text_spieler_leben, (500,30)) 
            screen.blit(self.defenders5, (300, 650)) 
            screen.blit(self.text5, (318,714))   
            screen.blit(self.text6, (325,737))    
            screen.blit(self.defenders6, (200, 650))
            screen.blit(self.text7, (213,714))   
            screen.blit(self.text8, (222,737)) 
            screen.blit(self.defenders7, (400, 650))
            screen.blit(self.text9, (418,713)) 
            screen.blit(self.text10, (428,735))                  
            screen.blit(text_geld, (0,100)) 
            screen.blit(self.text13, (0,40))
            if stop == True:
                 screen.blit(self.text11, (0,70)) 
            if stop == False:
                 screen.blit(self.text12, (0,70)) 
            
            if start == False:
                soundstop.stop()
                transparent_surface = pygame.Surface((1300, 900), pygame.SRCALPHA)
                transparent_surface.fill((0, 0, 0, 128))
                pygame.draw.rect(transparent_surface, (255, 0, 0), (0, 0, 0, 0), level_id)
                screen.blit(transparent_surface, (0, 0))
                transparent_surface2 = pygame.Surface((190, 40), pygame.SRCALPHA)
                transparent_surface2.fill((0, 0, 0, 128))
                pygame.draw.rect(transparent_surface2, (255, 0, 0), (0, 0, 0, 0), level_id)
                screen.blit(transparent_surface2, (495, 190))
                pygame.mixer.music.pause()
                sound2.stop()
                self.tex15 = font.render("Press (K) to start :)", True, (255,255,255))
                screen.blit(self.tex15, (500,200))  
            if start == True and pruf3:
                 pruf3 = False
                 pygame.mixer.music.unpause()

            if level_id2 >= 64:
                start2 = False
                soundstop.stop()
                eingabe3 = font.render("name: " + eingabe1, True, (255, 255, 255))
                self.verloren = False
                transparent_surface = pygame.Surface((1300, 900), pygame.SRCALPHA)
                transparent_surface.fill((0, 0, 0, 128))
                pygame.draw.rect(transparent_surface, (255, 0, 0), (0, 0, 0, 0), 2)
                screen.blit(transparent_surface, (0, 0))
                font2 = pygame.font.SysFont("Stencil",60)
                self.text11 = font2.render("Victory", True, (240, 180, 0))
                screen.blit(self.text11, ((width / 2)-150, (height / 2)-150))    
                pygame.mixer.music.stop()
                sound2.stop()
                screen.blit(eingabe3, (450, 350))
                self.text21 = font.render("Press (ESC) to enter you name in the Highscore list", True, (255, 255, 255))
                screen.blit(self.text21, (450,325))
                aktuelles_datum = datetime.now()
                datum = str(aktuelles_datum.year)+ "," + str(aktuelles_datum.month) + ","+ str(aktuelles_datum.day)
                if eingabe2 != "" and save:
                    
                    orm.save_highscore(Highscore(1,eingabe2, datum, level_id))
                    
                    highscorenn = orm.get_highscores()
                    for highscores in highscorenn:
                        liste = [highscores.highscore_id, highscores.name, highscores.date, highscores.level_id]
                        self.highscore_list.append(liste)
                    print(self.highscore_list)    
                    save = False
                    
                if self.highscore_list:
                    top = [self.highscore_list[0],self.highscore_list[1],self.highscore_list[2],self.highscore_list[3], self.highscore_list[4], self.highscore_list[5]]
                
                    top1 = "1) "+top[0][1]+" ¦ " + datum +" ¦ " + "gegener Panzern:" + str(top[0][3])
                    top2 = "2) "+top[1][1]+" ¦ " + datum +" ¦ " + "gegener Panzern:" + str(top[1][3])
                    top3 = "3) "+top[2][1]+" ¦ " + datum +" ¦ " + "gegener Panzern:" + str(top[2][3])
                    top4 = "4) "+top[3][1]+" ¦ " + datum +" ¦ " + "gegener Panzern:" + str(top[3][3])
                    top5 = "5) "+top[4][1]+" ¦ " + datum +" ¦ " + "gegener Panzern:" + str(top[4][3])
                    top6 = "6) "+top[5][1]+" ¦ " + datum +" ¦ " + "gegener Panzern:" + str(top[5][3])
                    surf = font.render(top1, True, (255, 255, 255))
                    screen.blit(surf, ((450,400)))
                    surf1 = font.render(top2, True, (255, 255, 255))
                    screen.blit(surf1, ((450,420)))
                    surf2 = font.render(top3, True, (255, 255, 255))
                    screen.blit(surf2, ((450,440)))
                    surf3 = font.render(top4, True, (255, 255, 255))
                    screen.blit(surf3, ((450,460)))
                    surf4 = font.render(top5, True, (255, 255, 255))
                    screen.blit(surf4, ((450,480)))
                    surf5 = font.render(top6, True, (255, 255, 255))
                    screen.blit(surf5, ((450,500)))

                if condition and not sound_played:
                    sound12.play()    
                    sound_playing = True
                    sound_played = True
                    
            
            if self.leben_spieler <= 0: 
                start2 = False
                soundstop.stop()
                eingabe3 = font.render("name: " + eingabe1, True, (255, 255, 255))
                
                self.verloren = False
                
                transparent_surface = pygame.Surface((1300, 900), pygame.SRCALPHA)
                transparent_surface.fill((0, 0, 0, 128))
                pygame.draw.rect(transparent_surface, (255, 0, 0), (0, 0, 0, 0), level_id)
                screen.blit(transparent_surface, (0, 0))
                font2 = pygame.font.SysFont("Stencil",60)
                self.text11 = font2.render("GAME OVER", True, (0, 0, 0))
                screen.blit(self.text11, ((width / 2)-150, (height / 2)-150))    
                self.leben_spieler = 0#
                self.text21 = font.render("Press (ESC) to enter you name in the Highscore list", True, (255, 255, 255))
                screen.blit(self.text21, (450,325))
                pygame.mixer.music.stop()
                sound2.stop()
                screen.blit(eingabe3, (450, 350))
                
                aktuelles_datum = datetime.now()
                datum = str(aktuelles_datum.year)+ "," + str(aktuelles_datum.month) + ","+ str(aktuelles_datum.day)
                
                if eingabe2 != "" and save:
                    
                    orm.save_highscore(Highscore(1,eingabe2, datum, level_id))
                    
                    highscorenn = orm.get_highscores()
                    for highscores in highscorenn:
                        liste = [highscores.highscore_id, highscores.name, highscores.date, highscores.level_id]
                        self.highscore_list.append(liste)
                    print(self.highscore_list)    
                    save = False
                    
                if self.highscore_list:
                    top = [self.highscore_list[0],self.highscore_list[1],self.highscore_list[2],self.highscore_list[3], self.highscore_list[4], self.highscore_list[5]]
                
                    top1 = "1) "+top[0][1]+" ¦ " + datum +" ¦ " + "gegener Panzern:" + str(top[0][3])
                    top2 = "2) "+top[1][1]+" ¦ " + datum +" ¦ " + "gegener Panzern:" + str(top[1][3])
                    top3 = "3) "+top[2][1]+" ¦ " + datum +" ¦ " + "gegener Panzern:" + str(top[2][3])
                    top4 = "4) "+top[3][1]+" ¦ " + datum +" ¦ " + "gegener Panzern:" + str(top[3][3])
                    top5 = "5) "+top[4][1]+" ¦ " + datum +" ¦ " + "gegener Panzern:" + str(top[4][3])
                    top6 = "6) "+top[5][1]+" ¦ " + datum +" ¦ " + "gegener Panzern:" + str(top[5][3])
                    surf = font.render(top1, True, (255, 255, 255))
                    screen.blit(surf, ((450,400)))
                    surf1 = font.render(top2, True, (255, 255, 255))
                    screen.blit(surf1, ((450,420)))
                    surf2 = font.render(top3, True, (255, 255, 255))
                    screen.blit(surf2, ((450,440)))
                    surf3 = font.render(top4, True, (255, 255, 255))
                    screen.blit(surf3, ((450,460)))
                    surf4 = font.render(top5, True, (255, 255, 255))
                    screen.blit(surf4, ((450,480)))
                    surf5 = font.render(top6, True, (255, 255, 255))
                    screen.blit(surf5, ((450,500)))
                    
                if condition and not sound_played:
                    sound6.play()
                    sound5.play()     
                    sound_playing = True
                    sound_played = True
                elif not condition and sound_playing:
                    sound6.stop()
                    sound_playing = False
            pygame.display.update()

            self.clock.tick(60)
            
            
               
        
                
                
                


game = Game()        
game.run()
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 10:24:19 2024

@author: ikowa
"""

import pygame, simpleGE, random

class Charlie(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("Charlie.png")
        self.setSize(25,25)
        self.position = (320,400)
        self.moveSpeed = 5
    
    def process(self):
        if self.isKeyPressed(pygame.K_LEFT):
            self.x -= self.moveSpeed
        if self.isKeyPressed(pygame.K_RIGHT):
            self.x += self.moveSpeed
        if self.isKeyPressed(pygame.K_UP):
            self.y -= self.moveSpeed
        if self.isKeyPressed(pygame.K_DOWN):
            self.y += self.moveSpeed
            """
            while keepGoing:
                if self.y == 316:
                    while keepGoing:
                        if self.y < 320:
                            self.y += 1
                        else: 
                            keepGoing = False
                            
                            while keepGoing:
                                if self.y > 315:
                                    self.y -= 1
                                else:
                                    keepGoing = False
                     # I was initially trying to make charlie "jump". Couldn't get it to work'
            """
                        
                    
           
            """
            while keepGoing:
                if self.y == 315:
                    self.y -= self.moveSpeed
                elif self.y > 315:
                    self.y -= self.moveSpeed
                else:
                    
                    keepGoing = False
            """
class Coin(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("Coin.png")
        self.setSize(25,25)
        self.minSpeed= 3
        self.maxSpeed = 8
        self.reset()
        
    def reset(self):
        self.y = 10
        self.x = random.randint(0, self.screenWidth)
        self.dy = random.randint(self.minSpeed,self.maxSpeed)
        
    def checkBounds(self):
        if self.bottom > self.screenHeight:
            self.reset()
class Hurt(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("hurtCharlie.png")
        self.setSize(25,25)
        self.minSpeed= 5
        self.maxSpeed = 8
        self.reset()
        
    def reset(self):
        self.y = 10
        self.x = random.randint(0, self.screenWidth)
        self.dy = random.randint(self.minSpeed,self.maxSpeed)
        
    def checkBounds(self):
        if self.bottom > self.screenHeight:
            self.reset()
class LblScore(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Score: 0"
        self.center =  (100,30)
class LblTime(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Time Left: 10"
        self.center = (500, 30)
        
class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.setImage("backgroundV1.png")
        self.sndCoin = simpleGE.Sound("pickupCoin.wav")
        self.sndHurt = simpleGE.Sound("hurtNoise.wav")
        self.numCoins = 10
        self.numHurt = 4
        self.score = 0
        self.charlie = Charlie(self)
        self.timer = simpleGE.Timer()
        self.timer.totalTime = 10
        self.lblTime = LblTime()
        self.lblscore = LblScore()
        self.coins = []
        self.hurts = []
        for i in range(self.numCoins):
            self.coins.append(Coin(self))
        for i in range(self.numHurt):
            self.hurts.append(Hurt(self))
        self.sprites = [self.charlie,
                        self.coins,
                        self.hurts,
                        self.lblscore,
                        self.lblTime]
    def setPrevScore(self, prevScore):
        self.prevScore = prevScore
        self.lblScore.text = f":Last score: {self.prevScore}"
        #48:39 start video here, last score needs to be fixed
    def process(self):
        for coin in self.coins:
            """
            if self.charlie.collidesWith(self.coin):
                self.sndCoin.play()
                self.coin.reset()
            """
            if coin.collidesWith(self.charlie):
                coin.reset()
                self.sndCoin.play()
                self.score += 1
                self.lblscore.text = f"Score = {self.score}"
        for hurt in self.hurts:
            
            if hurt.collidesWith(self.charlie):
                hurt.reset()
                self.sndHurt.play()
                self.score -= 1
                self.lblscore.text = f"Score = {self.score}"
        self.lblTime.text = f"Time left: {self.timer.getTimeLeft():.2f}"
        if self.timer.getTimeLeft() < 0:
            print(f"Score: {self.score} temporary")
            self.stop()
class Instructions(simpleGE.Scene):
    def __init__(self, prevScore):
        super().__init__()
        self.prevScore = prevScore
        self.setImage("Coin.png")
        self.response = "Quit"
        #self.prevScore = 0
        self.directions = simpleGE.MultiLabel()
        self.directions.textLines = [
            "Here is a line with some directions",
            "I hope I can come up with a fun scene",
            "get all the coins fast or whatever",
            "",
            "does this work"]
        #self.response = ("Play")
        self.directions.center = (320,240)
        self.directions.size = (500,250)
        self.btnPlay = simpleGE.Button()
        self.btnPlay.text = "Play"
        self.btnPlay.center = (100,400)
        self.btnQuit = simpleGE.Button()
        self.btnQuit.text = "Quit"
        self.btnQuit.center = (540,400)
        self.lblScore = simpleGE.Label()
        
        self.lblScore.center = (320,400)
        self.lblScore.text = f"Last Score: {self.prevScore}"
        self.sprites = [self.directions,
                        self.btnPlay,
                        self.btnQuit,
                        self.lblScore]
    def process(self):
        if self.btnPlay.clicked:
            self.response = "Play"
            self.stop()
        if self.btnQuit.clicked:
            self.response = "Quit"
            self.stop()
            
def main():
    keepGoing = True
    lastScore = 0
    while keepGoing:
        #lastScore = 0
        instructions = Instructions(lastScore)
        #instructions.setPrevScore(lastScore)
        instructions.start()
        #print(instructions.response)
        if instructions.response == "Play":
            game = Game()
            game.start()
            lastScore = game.score
        else:
            keepGoing = False
    
if __name__ == "__main__":
    main()
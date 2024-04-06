# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 10:24:19 2024

@author: ikowa
"""

import pygame, simpleGE, random

class Charlie(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("Mug.png")
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
class Coin(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("Orange.png")
        self.setSize(25,25)
        self.minSpeed= 3
        self.maxSpeed = 8
        self.minNegative = -3
        self.maxNegative = -8
        self.reset()
        
    def reset(self):
        chooseSpot = random.randint(1,4)
        if chooseSpot == int(1):
            #top
            self.y = 10
            self.x = random.randint(0, self.screenWidth)
            self.dy = random.randint(self.minSpeed,self.maxSpeed)
        if chooseSpot == int(2):
            #right
            self.y = random.randint(0, self.screenHeight)
            self.x = 640
            self.dx = random.randint(self.maxNegative, self.minNegative)
        if chooseSpot == int(3):
           #bottom
           self.y = 450
           self.x = random.randint(0, self.screenWidth)
           self.dy = random.randint(self.maxNegative, self.minNegative)
        if chooseSpot == int(4):
            #left, i' do this first cause  I knwo y = 0
            self.y = random.randint(0, self.screenHeight)
            self.x = 0
            self.dx = random.randint(self.minSpeed,self.maxSpeed)
    def checkBounds(self):
        if self.bottom > self.screenHeight:
            self.reset() 
        elif self.y < 0:
            self.reset()
        elif self.x > 640:
            self.reset()
        elif self.x < 0:
            self.reset()
class Hurt(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("Spider.png")
        self.setSize(25,25)
        self.minSpeed= 5
        self.maxSpeed = 8
        self.minNegative = -3
        self.maxNegative = -8
        self.reset()
        
    def reset(self):
        
        chooseSpot = random.randint(1,4)
        if chooseSpot == int(1):
            #top
            self.y = 10
            self.x = random.randint(0, self.screenWidth)
            self.dy = random.randint(self.minSpeed,self.maxSpeed)
        if chooseSpot == int(2):
            #right
            self.y = random.randint(0, self.screenHeight)
            self.x = 640
            self.dx = random.randint(self.maxNegative, self.minNegative)
        if chooseSpot == int(3):
            #bottom
            self.y = 450
            self.x = random.randint(0, self.screenWidth)
            self.dy = random.randint(self.maxNegative, self.minNegative)
        if chooseSpot == int(4):
            #left, i' do this first cause  I knwo y = 0
            self.y = random.randint(0, self.screenHeight)
            self.x = 0
            self.dx = random.randint(self.minSpeed,self.maxSpeed)
        
    def checkBounds(self):
        if self.bottom > self.screenHeight:
            self.reset()
        
        elif self.y < 0:
            self.reset()
        elif self.x > 640:
            self.reset()
        elif self.x < 0:
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
        self.setImage("diningRoom.png")
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
            print(f"Score: {self.score} ")
            self.stop()
class Instructions(simpleGE.Scene):
    def __init__(self, prevScore):
        super().__init__()
        self.prevScore = prevScore
        self.setImage("diningRoom.png")
        self.response = "Quit"
        #self.prevScore = 0
        self.directions = simpleGE.MultiLabel()
        self.directions.textLines = [
            "You live in BSU housing, which you didn't clean",
            "Now, spiders are crawling around in the morning",
            "Catch oranges in your mug, but not spiders!",
            "",
            "If there are spiders in my morning OJ",
            "My day is ruined and I will cry"]
        #self.response = ("Play")
        self.directions.center = (320,240)
        self.directions.size = (500,250)
        self.btnPlay = simpleGE.Button()
        self.btnPlay.text = "Play"
        self.btnPlay.fgColor = ("Purple")
        self.btnPlay.clearBack = True
        self.btnPlay.center = (100,400)
        self.btnQuit = simpleGE.Button()
        self.btnQuit.clearBack = True
        self.btnQuit.text = "Quit"
        self.btnQuit.fgColor = ("red")
        self.btnQuit.center = (540,400)
        self.lblScore = simpleGE.Label()
        
        self.lblScore.center = (320,400)
        self.lblScore.text = f"Last Score: {self.prevScore}"
        self.lblScore.clearBack = True
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
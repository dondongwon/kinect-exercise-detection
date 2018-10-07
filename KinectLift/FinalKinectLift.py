#BodyGame from GitHub draws skeletons (https://github.com/Kinect/PyKinect2/blob/master/examples/PyKinectBodyGame.py)

from pykinect2 import PyKinectV2, PyKinectRuntime
from pykinect2.PyKinectV2 import *

import ctypes
import _ctypes
import pygame
import sys
import math
import copy
import time

arnold = pygame.image.load("arnold.bmp")

# colors for drawing different bodies 
SKELETON_COLORS = [pygame.color.THECOLORS["red"], 
                  pygame.color.THECOLORS["blue"], 
                  pygame.color.THECOLORS["green"], 
                  pygame.color.THECOLORS["orange"], 
                  pygame.color.THECOLORS["purple"], 
                  pygame.color.THECOLORS["yellow"], 
                  pygame.color.THECOLORS["violet"]]

def text_objects(text,font, color = (0,0,0)):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def mousePressed(event,self):
        (x,y) = event.pos
        if self.startScreen == True:
            if x in range(int(self.screen_width/2)//2-100, (int(self.screen_width/2)//2 +100)):
                if y in range(int(self.screen_height - self.screen_height/4-100)//2,(int(self.screen_height - self.screen_height/4)+100)//2): 
                    self.startScreen = False
                    self.currPress = "Main"
                if y in range(int(self.screen_height - self.screen_height/8-100)//2,(int(self.screen_height - self.screen_height/8)+100)//2): 
                    self.startScreen = False
                    self.currPress = "Saved"
        elif self.currPress == "Main":

            if y in range(int(self.screen_height/4)//2 - 50,(int(self.screen_height/4)//2+50)):
                 if x in range(int(self.screen_width/2)//2-75, (int(self.screen_width/2)//2 + 25)):
                    self.profile = "Left"
                 if x in range(int(self.screen_width/2 + 150)//2, (int(self.screen_width/2 +150)//2 +100)):
                    self.profile = "Right"
            if y in range(int(self.screen_height - self.screen_height/4)//2,(int(self.screen_height - self.screen_height/4)+100)//2):
                 if x in range(int(self.screen_width/5)//2, (int(self.screen_width/5)//2 +100)):
                    self.currPress = "Squat"
                 if x in range(int(self.screen_width/5), (int(self.screen_width/5) +100)):
                    self.currPress = "Bench Press"
                 if x in range(int(self.screen_width/5 * 1.5), int(self.screen_width/5 * 1.5) +100):
                    self.currPress = "Help"
                 if x in range(int(self.screen_width/5 * 2), int(self.screen_width/5 * 2) +100):
                    self.startScreen = True
        elif self.currPress == "Saved":
            if (x in range(int(self.screen_width - self.screen_width/6.5)//2 - 100, int(self.screen_width - self.screen_width/6.5)//2 + 100)
               and y in range(int(self.screen_height/10)//2-100, int(self.screen_height/10)//2 + 100)):
                writeFile('saved.txt', "")
            else:
                self.startScreen = True
                self.currPress = "Main"
        elif self.currPress == "Help":
            if x in range(0, self.screen_width):
                self.startScreen = True
                self.currPress = "Main"
        elif self.currPress == "SquatSummary":
            if (x in range(int(self.screen_width - self.screen_width/6.5)//2 - 100, int(self.screen_width - self.screen_width/6.5)//2 + 100)
               and y in range(int(self.screen_height/10)//2-100, int(self.screen_height/10)//2 + 100)):
                updateSaved(self.time + "     Squat" + ":" + "   " + str(self.squatSummaryList) + ".")
            else:
                self.startScreen = True
                self.currPress = "Main"
        elif self.currPress == "BenchSummary":
            if (x in range(int(self.screen_width - self.screen_width/6.5)//2 - 100, int(self.screen_width - self.screen_width/6.5)//2 + 100)
               and y in range(int(self.screen_height/10)//2-100, int(self.screen_height/10)//2 + 100)):
                updateSaved(self.time + "     Bench" + ":" + "   " + str(self.summaryList) + ".")
            else:
                self.startScreen = True
                self.currPress = "Main"
        elif self.currPress != "Main" and self.currPress != "SquatSummary" and self.currPress != "BenchSummary" and self.moveDetected == True and self.jointDetected == True:
             if y in range(int(self.screen_height - self.screen_height/4)//2,(int(self.screen_height - self.screen_height/4)+100)//2):
                 if x in range(int(self.screen_width/5)//2, (int(self.screen_width/5)//2 +100)):
                    self.currPress = "Main"
                 if x in range(int(self.screen_width/5), (int(self.screen_width/5) +100)):
                    if self.currPress == "Bench Press":     
                        self.currPress = "BenchSummary"
                    elif self.currPress == "Squat":
                        self.currPress = "SquatSummary"
                    self.moveDetected = False
                    self.jointDetected = False

def updateSaved(list, path = 'saved.txt'):
    prev = readFile('saved.txt')
    writeFile('saved.txt', prev + str(list))

def readFile(path):
    with open(path, "rt") as f:
        return f.read()

def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)

class GameRuntime(object):
    def __init__(self):
        pygame.init()
        self.startScreen = True
        self.mainScreen = False 
        self.time = time.strftime("%H:%M") + " " + time.strftime("%d/%m/%Y")
        self.moveNames = ["Squat", "Bench", "Help", "Start"]

        self.currPress = "Main"

        self.screen_width = 1920 

        self.screen_height = 1080 

        self.profile = "Left"

        self.squatSummaryList = []
        self.summaryList = []
        self.wristXList = []
        self.wristYList = []
        self.elbowList = []
        self.feetList = []
        self.kneeYList = []
        self.kneeXList = []
        self.spineBaseYList = []
        self.hipYList = []
        self.minspineBaseY = None
        self.maxspineBaseY = None
        self.minKneeY = None
        self.maxKnee = None
        self.minWristX = None
        self.maxWristX = None
        self.minWristY = None
        self.maxWristY = None
        self.minElbowX = None
        self.maxElbowX = None
        self.minFeetY = None
        self.maxFeetY = None
        self.minHipY = None
        self.maxHipY = None 
        self.minKneeX = None
        self.maxKneeX = None
        self.curX = (None, None)
        self.curY = (None, None)
        
        self.moveDetected = False
        self.jointDetected = False


        # Used to manage how fast the screen updates
        self._clock = pygame.time.Clock()

        # Set the width and height of the window [width/2, height/2]
        self._screen = pygame.display.set_mode((960,540), pygame.HWSURFACE|pygame.DOUBLEBUF, 32)

        # Loop until the user clicks the close button.
        self._done = False

        # Kinect runtime object, we want color and body frames 
        self._kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Body)

        # back buffer surface for getting Kinect color frames, 32bit color, width and height equal to the Kinect color frame size
        self._frame_surface = pygame.Surface((self._kinect.color_frame_desc.Width, self._kinect.color_frame_desc.Height), 0, 32)

        # here we will store skeleton data 
        self._bodies = None

    def initialize(self):
        self.squatSummaryList = ["Partial rep"]
        self.summaryList = []
        self.wristXList = []
        self.wristYList = []
        self.elbowList = []
        self.feetList = []
        self.kneeYList = []
        self.kneeXList = []
        self.spineBaseYList = []
        self.hipYList = []
        self.minspineBaseY = None
        self.maxspineBaseY = None
        self.minKneeY = None
        self.maxKnee = None
        self.minWristX = None
        self.maxWristX = None
        self.minWristY = None
        self.maxWristY = None
        self.minElbowX = None
        self.maxElbowX = None
        self.minFeetY = None
        self.maxFeetY = None
        self.minHipY = None
        self.maxHipY = None 
        self.minKneeX = None
        self.maxKneeX = None
        self.curX = (None, None)
        self.curY = (None, None)
        
        self.moveDetected = False
        self.jointDetected = False

    def draw_title(self):
        self._frame_surface.blit(arnold, (0,0))
        
        text = pygame.font.Font("freesansbold.ttf",200)
        textSurf, textRect = text_objects("KinectLift", text, (255,255,255))
        textRect.center = (int(self.screen_width/2),int(self.screen_height/2))
        self._frame_surface.blit(textSurf,textRect)

        text1 = pygame.font.Font("freesansbold.ttf",100)
        textSurf1, textRect1 = text_objects("Start", text1, (255,255,255))
        textRect1.center = (int(self.screen_width/2),int(self.screen_height - self.screen_height/4))
        self._frame_surface.blit(textSurf1,textRect1)

        text1 = pygame.font.Font("freesansbold.ttf",80)
        textSurf1, textRect1 = text_objects("Saved Data", text1, (255,255,255))
        textRect1.center = (int(self.screen_width/2),int(self.screen_height - self.screen_height/8))
        self._frame_surface.blit(textSurf1,textRect1)


    def draw_helpPage(self):
        self._frame_surface.blit(arnold, (0,0))
        pygame.draw.rect(self._frame_surface, (255,255,255), (int(self.screen_width/40),int(self.screen_height/40),int(self.screen_width/40)*38,int(self.screen_height/40)*38))
        text = pygame.font.Font("freesansbold.ttf",50)
        textSurf, textRect = text_objects("Help", text)
        textRect.center = (int(self.screen_width/2),int(self.screen_height)/10)
        self._frame_surface.blit(textSurf,textRect)

        text = pygame.font.Font("freesansbold.ttf",30)
        count = 3
        for summary in readFile('help.txt').split("|"):
            textSurf1, textRect1 = text_objects(summary, text)
            textRect1.center = (int(self.screen_width/2),int(self.screen_height/15)*count)
            count += 1
            self._frame_surface.blit(textSurf1,textRect1)

        text = pygame.font.Font("freesansbold.ttf",30)
        textSurf1, textRect1 = text_objects("Click to return to main menu..", text)
        textRect1.center = (int(self.screen_width - self.screen_width/6.5),int(self.screen_height - self.screen_height/20))
        self._frame_surface.blit(textSurf1,textRect1)

    def draw_saved(self):
        self._frame_surface.blit(arnold, (0,0))

        pygame.draw.rect(self._frame_surface, (255,255,255), (int(self.screen_width/40),int(self.screen_height/40),int(self.screen_width/40)*38,int(self.screen_height/40)*38))
        text = pygame.font.Font("freesansbold.ttf",50)
        textSurf, textRect = text_objects("Saved", text)
        textRect.center = (int(self.screen_width/2),int(self.screen_height)/10)
        self._frame_surface.blit(textSurf,textRect)

        text = pygame.font.Font("freesansbold.ttf",30)
        textSurf1, textRect1 = text_objects("Reset Saved", text)
        textRect1.center = (int(self.screen_width - self.screen_width/6.5),int(self.screen_height/10))
        self._frame_surface.blit(textSurf1,textRect1)

        text = pygame.font.Font("freesansbold.ttf",30)
        count = 3
        for summary in readFile('saved.txt').split("."):
            textSurf1, textRect1 = text_objects(summary, text)
            textRect1.center = (int(self.screen_width/2),int(self.screen_height/15)*count)
            count += 1
            self._frame_surface.blit(textSurf1,textRect1)

        text = pygame.font.Font("freesansbold.ttf",30)
        textSurf1, textRect1 = text_objects("Click to return to start screen..", text)
        textRect1.center = (int(self.screen_width - self.screen_width/6.5),int(self.screen_height - self.screen_height/20))
        self._frame_surface.blit(textSurf1,textRect1)

    def draw_MainScrbuttons(self): 
        text = pygame.font.Font("freesansbold.ttf",100)
        textSurf, textRect = text_objects("Select an orientation", text)
        textRect.center = (int(self.screen_width/1.8),int(self.screen_height/6))
        self._frame_surface.blit(textSurf,textRect)

        text1 = pygame.font.Font("freesansbold.ttf",100)
        textSurf1, textRect1 = text_objects("Which Move?", text1)
        textRect1.center = (int(self.screen_width/2.8),int(self.screen_height - self.screen_height/3))
        self._frame_surface.blit(textSurf1,textRect1)

        text1 = pygame.font.Font("freesansbold.ttf",100)
        textSurf1, textRect1 = text_objects("Options", text1)
        textRect1.center = (int(3* self.screen_width/4),int(self.screen_height - self.screen_height/3))
        self._frame_surface.blit(textSurf1,textRect1)

        mouse = pygame.mouse.get_pos()
        pygame.draw.rect(self._frame_surface, (255,255,255), (int(self.screen_width/5),int(self.screen_height - self.screen_height/4),200,100))
        pygame.draw.rect(self._frame_surface, (255,255,255), (int(self.screen_width/5) *2 ,int(self.screen_height - self.screen_height/4),200,100))
        pygame.draw.rect(self._frame_surface, (255,255,255), (int(self.screen_width/5) *3,int(self.screen_height - self.screen_height/4),200,100))
        pygame.draw.rect(self._frame_surface, (255,255,255), (int(self.screen_width/5) *4,int(self.screen_height - self.screen_height/4),200,100))

        text = pygame.font.Font("freesansbold.ttf",50)

        for i in range(len(self.moveNames)):
            move = self.moveNames[i]
            textSurf2, textRect2 = text_objects(move, text)
            textRect2.center = (int(self.screen_width/5)*(i+1)+100,int(self.screen_height - self.screen_height/4)+50)
            self._frame_surface.blit(textSurf2,textRect2)

    def draw_summaryPage(self):
        self._frame_surface.blit(arnold, (0,0))
        pygame.draw.rect(self._frame_surface, (255,255,255), (int(self.screen_width/100),int(self.screen_height/100),int(self.screen_width/100)*98,int(self.screen_height/100)*98))
        text = pygame.font.Font("freesansbold.ttf",50)
        textSurf, textRect = text_objects("Summary", text)
        textRect.center = (int(self.screen_width/2),int(self.screen_height)/10)
        self._frame_surface.blit(textSurf,textRect)

        text = pygame.font.Font("freesansbold.ttf",30)
        textSurf1, textRect1 = text_objects("Save Summary", text)
        textRect1.center = (int(self.screen_width - self.screen_width/6.5),int(self.screen_height/10))
        self._frame_surface.blit(textSurf1,textRect1)

        if self.summaryList == []:
            text = pygame.font.Font("freesansbold.ttf",30)
            textSurf, textRect = text_objects("If there are no comments below, good job! KinectLift has not detected any flaws in your impeccable form!", text)
            textRect.center = (int(self.screen_width/2),int(self.screen_height)/3)
            self._frame_surface.blit(textSurf,textRect)


        text = pygame.font.Font("freesansbold.ttf",30)
        textSurf1, textRect1 = text_objects("Click to return to main menu..", text)
        textRect1.center = (int(self.screen_width - self.screen_width/6.5),int(self.screen_height - self.screen_height/20))
        self._frame_surface.blit(textSurf1,textRect1)

        for i in range(len(self.summaryList)):
            move = self.summaryList[i]
            if move == "Linear bar path":
                move = "Great benchers press the bar in a J-curve, creating horizontal movement to provide maximum leverage."
            if move == "Partial rep":
                move = "This is detected when your wrists don’t go as low as your chest, leading to a partial rep. Focus on going lower and deeper."
            if move == "Tuck in shoulders":
                move = " You flared out your shoulders, placing excessive amount of stress on the rotator cuffs. Tuck in the shoulders!"
            if move == "Unstable feet":
                move = "A lot of rookies wiggle their feet. Keep the core stable by locking in with your heels and tightening your glutes"
            textSurf1, textRect1 = text_objects(move, text)
            textRect1.center = (int(self.screen_width/2),100 +int(self.screen_height/6)+100*i)
            self._frame_surface.blit(textSurf1,textRect1)

    def draw_squatSummaryPage(self):
        self._frame_surface.blit(arnold, (0,0))
        pygame.draw.rect(self._frame_surface, (255,255,255), (int(self.screen_width/40),int(self.screen_height/40),int(self.screen_width/40)*38,int(self.screen_height/40)*38))
        text = pygame.font.Font("freesansbold.ttf",50)
        textSurf, textRect = text_objects("Summary", text)
        textRect.center = (int(self.screen_width/2),int(self.screen_height)/10)
        self._frame_surface.blit(textSurf,textRect)

        if self.squatSummaryList == []:
            text = pygame.font.Font("freesansbold.ttf",30)
            textSurf, textRect = text_objects("If there are no comments below, good job! KinectLift has not detected any flaws in your impeccable form!", text)
            textRect.center = (int(self.screen_width/2),int(self.screen_height)/3)
            self._frame_surface.blit(textSurf,textRect)

        text = pygame.font.Font("freesansbold.ttf",30)
        textSurf1, textRect1 = text_objects("Save Summary", text)
        textRect1.center = (int(self.screen_width - self.screen_width/6.5),int(self.screen_height/10))
        self._frame_surface.blit(textSurf1,textRect1)

        text = pygame.font.Font("freesansbold.ttf",30)
        textSurf1, textRect1 = text_objects("Click to return to main menu..", text)
        textRect1.center = (int(self.screen_width - self.screen_width/6.5),int(self.screen_height - self.screen_height/20))
        self._frame_surface.blit(textSurf1,textRect1)

        for i in range(len(self.squatSummaryList)):
            move = self.squatSummaryList[i]
            if move == "Knee came too forward":
                move = "Your knees shoudn't pass over your toes for knee-joint health. Try sitting back more into the squat and emphasize flexibility!"
            if move == "Partial rep":
                move = "Your hips didn’t go as low as the height of your knees, leading to a partial rep! Next time, focus on going lower and deeper."
            if move == "Bar is not in line with feet":
                move = "Your feet needs to be parallel to the bar. This ensures you are not leaning too far back/forwards, preventing spinal injuries."
            textSurf1, textRect1 = text_objects(move, text)
            textRect1.center = (int(self.screen_width/2),100 +int(self.screen_height/6)+100*i)
            self._frame_surface.blit(textSurf1,textRect1)

    def draw_moveScr(self): 
        text = pygame.font.Font("freesansbold.ttf",100)
        textSurf, textRect = text_objects(self.currPress, text)
        textRect.center = (int(self.screen_width/2),int(self.screen_height/6))
        self._frame_surface.blit(textSurf,textRect)
        
        text1 = pygame.font.Font("freesansbold.ttf",50)
        textSurf1, textRect1 = text_objects("No rep detected", text1)
        textRect1.center = (int(self.screen_width/2),int(1.5* self.screen_height/6))
        self._frame_surface.blit(textSurf1,textRect1)

        if self.jointDetected == False:
            text2 = pygame.font.Font("freesansbold.ttf",50)
            textSurf2, textRect2 = text_objects("No joints detected", text1)
            textRect2.center = (int(self.screen_width/2),int(2* self.screen_height/6))
            self._frame_surface.blit(textSurf2,textRect2)
        else:
            text2 = pygame.font.Font("freesansbold.ttf",50)
            textSurf2, textRect2 = text_objects("Joints detected!", text1)
            textRect2.center = (int(self.screen_width/2),int(2* self.screen_height/6))
            self._frame_surface.blit(textSurf2,textRect2)

    def draw_movebuttons(self): 
        text = pygame.font.Font("freesansbold.ttf",50)
        textSurf, textRect = text_objects(self.currPress, text)
        textRect.center = (int(self.screen_width/2),int(self.screen_height/6))
        self._frame_surface.blit(textSurf,textRect)

        text1 = pygame.font.Font("freesansbold.ttf",100)
        textSurf1, textRect1 = text_objects("Rep & Joints detected!", text1)
        textRect1.center = (int(self.screen_width/2),int(1.5* self.screen_height/6))
        self._frame_surface.blit(textSurf1,textRect1)

        pygame.draw.rect(self._frame_surface, (255,255,255), (int(self.screen_width/4.8),int(self.screen_height - self.screen_height/4),225,100))
        pygame.draw.rect(self._frame_surface, (255,255,255), (int(self.screen_width/4.8) *2,int(self.screen_height - self.screen_height/4),260,100))
       
        text = pygame.font.Font("freesansbold.ttf",50)
        list = ["Main", "Summary"]
        for i in range(len(list)):
            move = list[i]
            textSurf, textRect = text_objects(move, text)
            textRect.center = (int(self.screen_width/4.6)*(i+1)+100,int(self.screen_height - self.screen_height/4)+50)
            self._frame_surface.blit(textSurf,textRect)

    def draw_body_bone(self, joints, jointPoints, color , joint0, joint1):
        joint0State = joints[joint0].TrackingState;
        joint1State = joints[joint1].TrackingState;

        # both joints are not tracked
        if (joint0State == PyKinectV2.TrackingState_NotTracked) or (joint1State == PyKinectV2.TrackingState_NotTracked): 
            return

        # both joints are not *really* tracked
        if (joint0State == PyKinectV2.TrackingState_Inferred) and (joint1State == PyKinectV2.TrackingState_Inferred):
            return

        # ok, at least one is good 
        start = (jointPoints[joint0].x, jointPoints[joint0].y)
        end = (jointPoints[joint1].x, jointPoints[joint1].y)

        try:
            pygame.draw.line(self._frame_surface, color, start, end, 8)
        except: # need to catch it due to possible invalid positions (with inf)
            pass

    def draw_orientation(self): 
        
        if self.profile == "Left":
            pygame.draw.rect(self._frame_surface, (102,102,102), (int(self.screen_width/2) - 150,int(self.screen_height/4),200,100))
            pygame.draw.rect(self._frame_surface, (255,255,255), (int(self.screen_width/2) + 150,int(self.screen_height/4),200,100))
        else:
            pygame.draw.rect(self._frame_surface, (255,255,255), (int(self.screen_width/2) - 150,int(self.screen_height/4),200,100))
            pygame.draw.rect(self._frame_surface, (102,102,102), (int(self.screen_width/2) + 150,int(self.screen_height/4),200,100))

        text = pygame.font.Font("freesansbold.ttf",50)

        textSurf, textRect = text_objects("Left", text)
        textRect.center = (int(self.screen_width/2)- 150+100, self.screen_height/4 +50)
        self._frame_surface.blit(textSurf,textRect)

        textSurf1, textRect1 = text_objects("Right", text)
        textRect1.center = (int(self.screen_width/2)+ 150+100, self.screen_height/4+50)
        self._frame_surface.blit(textSurf1,textRect1)

    def draw_body(self, joints, jointPoints, color):
        # Torso
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_Head, PyKinectV2.JointType_Neck);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_Neck, PyKinectV2.JointType_SpineShoulder);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineShoulder, PyKinectV2.JointType_SpineMid);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineMid, PyKinectV2.JointType_SpineBase);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineShoulder, PyKinectV2.JointType_ShoulderRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineShoulder, PyKinectV2.JointType_ShoulderLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineBase, PyKinectV2.JointType_HipRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineBase, PyKinectV2.JointType_HipLeft);
    
        # Right Arm    
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ShoulderRight, PyKinectV2.JointType_ElbowRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ElbowRight, PyKinectV2.JointType_WristRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_WristRight, PyKinectV2.JointType_HandRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_HandRight, PyKinectV2.JointType_HandTipRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_WristRight, PyKinectV2.JointType_ThumbRight);

        # Left Arm
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ShoulderLeft, PyKinectV2.JointType_ElbowLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ElbowLeft, PyKinectV2.JointType_WristLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_WristLeft, PyKinectV2.JointType_HandLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_HandLeft, PyKinectV2.JointType_HandTipLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_WristLeft, PyKinectV2.JointType_ThumbLeft);

        # Right Leg
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_HipRight, PyKinectV2.JointType_KneeRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_KneeRight, PyKinectV2.JointType_AnkleRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_AnkleRight, PyKinectV2.JointType_FootRight);

        # Left Leg
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_HipLeft, PyKinectV2.JointType_KneeLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_KneeLeft, PyKinectV2.JointType_AnkleLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_AnkleLeft, PyKinectV2.JointType_FootLeft);


    def draw_color_frame(self, frame, target_surface):
        target_surface.lock()
        address = self._kinect.surface_as_array(target_surface.get_buffer())
        ctypes.memmove(address, frame.ctypes.data, frame.size)
        del address
        target_surface.unlock()


    def run(self):
        # -------- Main Program Loop -----------
        while not self._done:
            # --- Main event loop
            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    self._done = True # Flag that we are done so we exit this loop
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mousePressed(event,self)

            # We have a color frame. Fill out back buffer surface with frame's data 
            if self._kinect.has_new_color_frame():
                frame = self._kinect.get_last_color_frame()
                self.draw_color_frame(frame, self._frame_surface)
                frame = None
           

            # We have a body frame, so can get skeletons
            if self._kinect.has_new_body_frame() and self.currPress != "Main": 
                self._bodies = self._kinect.get_last_body_frame()

                if self._bodies is not None: 
                    for i in range(0, self._kinect.max_body_count):
                        body = self._bodies.bodies[i]
                        if not body.is_tracked: 
                            continue 

                        joints = body.joints 
                        # convert joint coordinates to color space 
                        joint_points = self._kinect.body_joints_to_color_space(joints)
                        self.draw_body(joints, joint_points, SKELETON_COLORS[i])

                        joints = body.joints 
                        # save the hand positions
                        if self.currPress == "Squat":
                            rightWristY = joints[PyKinectV2.JointType_WristRight].Position.y
                            leftWristY  = joints[PyKinectV2.JointType_WristLeft].Position.y
                            rightWristX = joints[PyKinectV2.JointType_WristRight].Position.x
                            leftWristX  = joints[PyKinectV2.JointType_WristLeft].Position.x
                            rightKneeX = joints[PyKinectV2.JointType_KneeRight].Position.x
                            leftKneeX = joints[PyKinectV2.JointType_KneeLeft].Position.x
                            rightKneeY = joints[PyKinectV2.JointType_KneeRight].Position.y
                            leftKneeY = joints[PyKinectV2.JointType_KneeLeft].Position.y
                            leftFootX = joints[PyKinectV2.JointType_AnkleLeft].Position.x
                            rightFootX = joints[PyKinectV2.JointType_AnkleRight].Position.x
                            rightHipY = joints[PyKinectV2.JointType_HipRight].Position.y
                            leftHipY = joints[PyKinectV2.JointType_HipLeft].Position.y
                            spineBaseY = joints[PyKinectV2.JointType_SpineBase].Position.y
                            spineBaseX = joints[PyKinectV2.JointType_SpineBase].Position.x
                            spineShouldY =joints[PyKinectV2.JointType_SpineShoulder].Position.y
                            if ((self.profile == "Left") and (joints[PyKinectV2.JointType_SpineBase].TrackingState != PyKinectV2.TrackingState_NotTracked) and (joints[PyKinectV2.JointType_HipLeft].TrackingState != PyKinectV2.TrackingState_NotTracked)
                                and (joints[PyKinectV2.JointType_KneeLeft].TrackingState != PyKinectV2.TrackingState_NotTracked)):
                                self.jointDetected = True
                                self.curX = (leftWristX, leftKneeX)        
                                self.curY = (leftWristY, leftFootX)
                                if (abs(leftWristY -spineBaseY) >= 0.3):
                                    self.moveDetected = True
                                    if  abs(leftWristX - rightWristX) < 0.1:
                                        self.wristXList.append(self.curX[0])
                                    self.wristYList.append(self.curY[0])
                                    self.kneeXList.append(self.curX[1])
                                    self.feetList.append(self.curY[1])                                   
                                    if leftHipY > leftKneeY +.10: 
                                        self.hipYList.append(leftHipY)
                                    self.kneeYList.append(leftKneeY)
                                if len(self.wristXList) != 0 and len(self.wristYList) != 0 and len(self.kneeYList) != 0 and len(self.kneeXList) != 0 and len(self.feetList) != 0 and len(self.hipYList) != 0 and (abs(leftWristY -spineBaseY) >= 0.3):
                                    (self.minWristX, self.maxWristX) = min(self.wristXList), max(self.wristXList)
                                    (self.minWristY, self.maxWristY) = min(self.wristYList), max(self.wristYList)
                                    (self.minKneeX, self.maxKneeX) = min(self.kneeXList), max(self.kneeXList)
                                    (self.minKneeY, self.maxKneeY) = min(self.kneeYList), max(self.kneeYList)
                                    (self.minHipY, self.maxHipY) = min(self.hipYList), max(self.hipYList)   
                                    if (abs(self.feetList[0] - self.maxKneeX)) > 0.3:
                                        fix = "Knee came too forward"
                                        if fix not in self.squatSummaryList:
                                            self.squatSummaryList.append(fix) 
                                    if (self.maxKneeY - .10> self.minHipY):
                                        fix = "Partial rep"
                                        if fix in self.squatSummaryList:
                                            self.squatSummaryList.remove(fix) 
                                    if  abs((self.maxWristX + self.minWristX)/2 - min(self.feetList)) > 0.25:
                                        fix = "Bar is not in line with feet"
                                        if fix not in self.squatSummaryList:
                                            self.squatSummaryList.append(fix) 
                                   
                            if ((self.profile == "Right") and (joints[PyKinectV2.JointType_SpineBase].TrackingState != PyKinectV2.TrackingState_NotTracked) and (joints[PyKinectV2.JointType_HipRight].TrackingState != PyKinectV2.TrackingState_NotTracked)
                                and (joints[PyKinectV2.JointType_KneeRight].TrackingState != PyKinectV2.TrackingState_NotTracked)):
                                self.jointDetected = True
                                self.curX = (rightWristX, rightKneeX)        
                                self.curY = (rightWristY, rightFootX)
                                if (abs(rightWristY -spineBaseY) >= 0.3):
                                    self.moveDetected = True
                                    if  abs(leftWristX - rightWristX) < 0.1:
                                        self.wristXList.append(self.curX[0])
                                    self.wristYList.append(self.curY[0])
                                    self.kneeXList.append(self.curX[1])
                                    self.feetList.append(self.curY[1])                                   
                                    if rightHipY > rightKneeY +.10: 
                                        self.hipYList.append(rightHipY)
                                    self.kneeYList.append(rightKneeY)
                                if len(self.wristXList) != 0 and len(self.wristYList) != 0 and len(self.kneeYList) != 0 and len(self.kneeXList) != 0 and len(self.feetList) != 0 and len(self.hipYList) != 0:
                                    (self.minWristX, self.maxWristX) = min(self.wristXList), max(self.wristXList)
                                    (self.minWristY, self.maxWristY) = min(self.wristYList), max(self.wristYList)
                                    (self.minKneeX, self.maxKneeX) = min(self.kneeXList), max(self.kneeXList)
                                    (self.minKneeY, self.maxKneeY) = min(self.kneeYList), max(self.kneeYList)
                                    (self.minHipY, self.maxHipY) = min(self.hipYList), max(self.hipYList)   
                                    if ((self.feetList[0]) - self.maxKneeX) < 0.3:
                                        fix = "Knee came too forward"
                                        if fix not in self.squatSummaryList:
                                            self.squatSummaryList.append(fix) 
                                    if (self.maxKneeY - .10> self.minHipY):
                                        fix = "Partial rep"
                                        if fix in self.squatSummaryList:
                                            self.squatSummaryList.remove(fix) 
                                    if  abs(min(self.feetList) - (self.maxWristX + self.minWristX)/2) > 0.25:
                                        fix = "Bar is not in line with feet"
                                        if fix not in self.squatSummaryList:
                                            self.squatSummaryList.append(fix) 
                        if self.currPress == "Bench Press":
                            spineY = joints[PyKinectV2.JointType_SpineMid].Position.y
                            rightHipY = joints[PyKinectV2.JointType_HipRight].Position.y
                            leftHipY = joints[PyKinectV2.JointType_HipLeft].Position.y
                            rightWristY = joints[PyKinectV2.JointType_WristRight].Position.y
                            leftWristY  = joints[PyKinectV2.JointType_WristLeft].Position.y
                            rightWristX = joints[PyKinectV2.JointType_WristRight].Position.x
                            leftWristX  = joints[PyKinectV2.JointType_WristLeft].Position.x
                            rightElbowX = joints[PyKinectV2.JointType_ElbowRight].Position.x
                            leftElbowX = joints[PyKinectV2.JointType_ElbowLeft].Position.x
                            leftFootY = joints[PyKinectV2.JointType_AnkleLeft].Position.y
                            rightFootY = joints[PyKinectV2.JointType_AnkleRight].Position.y 
                            spineMidY = joints[PyKinectV2.JointType_SpineShoulder].Position.y
                            spineMidX = joints[PyKinectV2.JointType_SpineShoulder].Position.x
                            if ((self.profile == "Left") and (joints[PyKinectV2.JointType_WristLeft].TrackingState != PyKinectV2.TrackingState_NotTracked)):
                                self.jointDetected = True
                                self.curX = (leftWristX, leftElbowX)        
                                self.curY = (leftWristY, leftFootY)
                                if (abs(spineY - rightHipY) <= 0.1):
                                    self.moveDetected = True
                                    if len(self.wristXList) == 0:
                                        self.wristXList.append(self.curX[0])
                                    if len(self.wristYList) == 0:
                                        self.wristYList.append(self.curY[0])
                                    if len(self.elbowList) == 0:
                                        self.elbowList.append(self.curX[1])
                                    if len(self.feetList) == 0:
                                        self.feetList.append(self.curY[1])
                                    if abs(self.wristXList[len(self.wristXList)-1] - self.curX[0]) <= 0.05:
                                        self.wristXList.append(self.curX[0])
                                    if abs(self.wristYList[len(self.wristYList)-1] - self.curY[0]) <= 0.05:
                                        self.wristYList.append(self.curY[0])
                                    if abs(self.elbowList[len(self.elbowList)-1] - self.curX[1]) <= 0.05:
                                        self.elbowList.append(self.curX[1])
                                    if abs(self.feetList[len(self.feetList)-1] - self.curY[1]) <= 0.05:
                                        self.feetList.append(self.curY[1])
                                if len(self.wristXList) != 0 and len(self.wristYList) != 0 and len(self.elbowList) != 0 and len(self.feetList) != 0:
                                    (self.minWristX, self.maxWristX) = min(self.wristXList), max(self.wristXList)
                                    (self.minWristY, self.maxWristY) = min(self.wristYList), max(self.wristYList)
                                    (self.minElbowX, self.maxElbowX) = min(self.elbowList), max(self.elbowList)
                                    (self.minFeetY, self.maxFeetY) = min(self.feetList), max(self.feetList)
                                    if abs(self.minWristX - self.maxWristX) < 0.10:
                                        fix = "Linear bar path"
                                        if fix not in self.summaryList:
                                            self.summaryList.append(fix)                                       
                                        #self.linearpath = True 
                                    if abs(self.minWristX - self.maxWristX) > 0.10:
                                        fix = "Linear bar path"
                                        if fix in self.summaryList:
                                            self.summaryList.remove(fix) 
                                    if abs(self.minWristY - spineMidY) > 0.08:
                                        fix = "Partial rep"
                                        if fix not in self.summaryList:
                                            self.summaryList.append(fix) 
                                        #self.halfrep = True
                                    if abs(self.minWristY) - abs(spineMidY) < 0.08:
                                        fix = "Partial rep"
                                        if fix in self.summaryList:
                                            self.summaryList.remove(fix) 
                                        #self.halfrep = True
                                    if abs(self.maxElbowX- spineMidX) <0.38:
                                        fix = "Tuck in shoulders"
                                        if fix not in self.summaryList:
                                            self.summaryList.append(fix) 
                                        #self.incshould = True
                                    if abs(self.maxElbowX- spineMidX) > 0.38:
                                        fix = "Tuck in shoulders"
                                        if fix in self.summaryList:
                                            self.summaryList.remove(fix)
                                    if abs(self.minFeetY - self.maxFeetY) > 0.1: 
                                        fix = "Unstable feet"
                                        if fix not in self.summaryList:
                                            self.summaryList.append(fix) 
                                        #self.unstable = True 
                                    if abs(self.minFeetY - self.maxFeetY) < 0.1: 
                                        fix = "Unstable feet"
                                        if fix in self.summaryList:
                                            self.summaryList.remove(fix) 
                            if ((self.profile == "Right") and (joints[PyKinectV2.JointType_WristRight].TrackingState != PyKinectV2.TrackingState_NotTracked)):
                                self.jointDetected = True
                                self.curX = (rightWristX, rightElbowX)
                                self.curY = (rightWristY, rightFootY)
                                if (abs(spineY - rightHipY) <= 0.1):
                                    self.moveDetected = True
                                    if len(self.wristXList) == 0:
                                        self.wristXList.append(self.curX[0])
                                    if len(self.wristYList) == 0:
                                        self.wristYList.append(self.curY[0])
                                    if len(self.elbowList) == 0:
                                        self.elbowList.append(self.curX[1])
                                    if len(self.feetList) == 0:
                                        self.feetList.append(self.curY[1])
                                    if abs(self.wristXList[len(self.wristXList)-1] - self.curX[0]) <= 0.05:
                                        self.wristXList.append(self.curX[0])
                                    if abs(self.wristYList[len(self.wristYList)-1] - self.curY[0]) <= 0.05:
                                        self.wristYList.append(self.curY[0])
                                    if abs(self.elbowList[len(self.elbowList)-1] - self.curX[1]) <= 0.05:
                                        self.elbowList.append(self.curX[1])
                                    if abs(self.feetList[len(self.feetList)-1] - self.curY[1]) <= 0.05:
                                        self.feetList.append(self.curY[1])
                                if len(self.wristXList) != 0 and len(self.wristYList) != 0 and len(self.elbowList) != 0 and len(self.feetList) != 0:
                                    (self.minWristX, self.maxWristX) = min(self.wristXList), max(self.wristXList)
                                    (self.minWristY, self.maxWristY) = min(self.wristYList), max(self.wristYList)
                                    (self.minElbowX, self.maxElbowX) = min(self.elbowList), max(self.elbowList)
                                    (self.minFeetY, self.maxFeetY) = min(self.feetList), max(self.feetList)
                                    if abs(self.minWristX - self.maxWristX) < 0.10:
                                        fix = "Linear bar path"
                                        if fix not in self.summaryList:
                                            self.summaryList.append(fix)                                       
                                        #self.linearpath = True 
                                    if abs(self.minWristX - self.maxWristX) > 0.10:
                                        fix = "Linear bar path"
                                        if fix in self.summaryList:
                                            self.summaryList.remove(fix) 
                                    if abs(self.minWristY - spineMidY) > 0.08:
                                        fix = "Partial rep"
                                        if fix not in self.summaryList:
                                            self.summaryList.append(fix) 
                                        #self.halfrep = True
                                    if abs(self.minWristY - spineMidY) < 0.08:
                                        fix = "Partial rep"
                                        if fix in self.summaryList:
                                            self.summaryList.remove(fix) 
                                        #self.halfrep = True
                                    if abs(self.maxElbowX- spineMidX) <0.38:
                                        fix = "Tuck in shoulders"
                                        if fix not in self.summaryList:
                                            self.summaryList.append(fix) 
                                        #self.incshould = True
                                    if abs(self.maxElbowX- spineMidX) > 0.38:
                                        fix = "Tuck in shoulders"
                                        if fix in self.summaryList:
                                            self.summaryList.remove(fix)
                                    if abs(self.minFeetY - self.maxFeetY) > 0.1: 
                                        fix = "Unstable feet"
                                        if fix not in self.summaryList:
                                            self.summaryList.append(fix) 
                                        #self.unstable = True 
                                    if abs(self.minFeetY - self.maxFeetY) < 0.1: 
                                        fix = "Unstable feet"
                                        if fix in self.summaryList:
                                            self.summaryList.remove(fix) 
                                
                                
            # Draw graphics
            if self.startScreen == True:
                self.draw_title()
            elif self.currPress == "Main":
                self.draw_MainScrbuttons()
                self.draw_orientation()
            elif self.currPress != "Main":
                if self.currPress == "Help":
                    self.draw_helpPage()
                elif self.currPress == "Saved":
                    self.draw_saved()
                elif self.currPress == "BenchSummary":
                    self.draw_summaryPage()
                elif self.currPress == "SquatSummary":
                    self.draw_squatSummaryPage()
                elif self.moveDetected:
                    self.draw_movebuttons()
                else:
                    self.draw_moveScr()

            # Optional debugging text
            #font = pygame.font.Font(None, 36)
            #text = font.render(str(self.flap), 1, (0, 0, 0))
            #self._frame_surface.blit(text, (100,100))

            # --- copy back buffer surface pixels to the screen, resize it if needed and keep aspect ratio
            # --- (screen size may be different from Kinect's color frame size) 
            h_to_w = float(self._frame_surface.get_height()) / self._frame_surface.get_width()
            target_height = int(h_to_w * self._screen.get_width())
            surface_to_draw = pygame.transform.scale(self._frame_surface, (self._screen.get_width(), target_height));
            self._screen.blit(surface_to_draw, (0,0))
            surface_to_draw = None
            pygame.display.update()

            # --- Limit to 60 frames per second
            self._clock.tick(60)

        # Close our Kinect sensor, close the window and quit.
        self._kinect.close()
        pygame.quit()

game = GameRuntime();
game.run();

import random
from gl import Renderer
import math
from obj import *
from mathcou import *
from shader import *
from collections import namedtuple




V2 = namedtuple('Point2', ['x', 'y'])




windoWidth = 1920
windowHeight = 1080
scale= 1
viewportWidth= windoWidth*scale
viewportHeight= windowHeight *scale
viewportX=0
viewportY=0
# light= [0.1,0.8,0.2]
light= normalize([-0.5,1,-0.2])
outputFileName="output.bmp"





myRenderer = Renderer(windoWidth, windowHeight,light)
myRenderer.glViewPort(viewportX,viewportY,viewportWidth,viewportHeight)

# OPCIONES DE SHADEERS: TOON, SMOOTH, FLAT, BLACKANDWHITE,BLACKANDWHITEFLAT, FRESNEL, GLOW



shaderName3= "FLAT"
objectFilename3="./assets/witchkingcentered.obj"
textureFilename3= "./assets/Metal1.bmp"
rotate3=[0,150,0]
transform3=[850,500,-70]
scale3=[100,100,100]
myRenderer.glLoadObject(objectFilename3,textureFilename3,shaderName3,transform3,scale3,rotate3)


shaderName3= "SMOOTH"
objectFilename3="./assets/witchkingcentered.obj"
textureFilename3= "./assets/Metal1.bmp"
rotate3=[0,180,0]
transform3=[850,500,200]
scale3=[200,200,200]
# myRenderer.glLoadObject(objectFilename3,textureFilename3,shaderName3,transform3,scale3,rotate3)








# shaderName3= "FLAT"
# objectFilename3="./assets/witchkingcentered.obj"
# textureFilename3= "./assets/Metal1.bmp"
# rotate3=[0,125,0]
# transform3=[250,500,-70]
# scale3=[100,100,100]
# myRenderer.glLoadObject(objectFilename3,textureFilename3,shaderName3,transform3,scale3,rotate3)



# myRenderer.glSetColor(255,25,50)
# shaderName3= "SMOOTH"
# objectFilename3="./assets/witchkingcentered.obj"
# textureFilename3= "./assets/Metal1.bmp"
# rotate3=[0,250,0]
# transform3=[1500,500,-70]
# scale3=[100,100,100]
# myRenderer.glLoadObject(objectFilename3,textureFilename3,shaderName3,transform3,scale3,rotate3)





myRenderer.glRender()
myRenderer.glFinish(outputFileName)




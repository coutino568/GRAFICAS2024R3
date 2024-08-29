
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
outputFileName="output2.bmp"





myRenderer = Renderer(windoWidth, windowHeight,light,"./assets/BACKGROUND.bmp")
myRenderer.glViewPort(viewportX,viewportY,viewportWidth,viewportHeight)
# myRenderer.setbackgroundTexture("/assets/BACKGROUND.bmp")
myRenderer.glClear()

# OPCIONES DE SHADEERS: TOON, SMOOTH, FLAT, BLACKANDWHITE,BLACKANDWHITEFLAT, FRESNEL, GLOW, UNLIT

offset= [400,-100,-500]

# shaderName3= "UNLIT"
# objectFilename3="./assets/terrain.obj"
# textureFilename3= "./assets/COLOR_TERRAIN.bmp"
# rotate3=[0,30,0]
# transform3=[-687+offset[0],-3+offset[1],579+offset[2]]
# scale3=[200,200,200]
# myRenderer.glLoadObject(objectFilename3,textureFilename3,shaderName3,transform3,scale3,rotate3)


shaderName3= "SMOOTH"
objectFilename3="./assets/minas2.obj"
textureFilename3= "./assets/PLASTER1.bmp"
rotate3=[0,30,0]
transform3=[0+offset[0],98+offset[1],0+offset[2]]
scale3=[200,200,200]
myRenderer.glLoadObject(objectFilename3,textureFilename3,shaderName3,transform3,scale3,rotate3)




shaderName3= "SMOOTH"
objectFilename3="./assets/mountains2.obj"
textureFilename3= "./assets/COLOR_TERRAIN.bmp"
rotate3=[0,30,0]
transform3=[-691+offset[0],72+offset[1],580+offset[2]]
scale3=[200,200,200]
myRenderer.glLoadObject(objectFilename3,textureFilename3,shaderName3,transform3,scale3,rotate3)



shaderName3= "SMOOTH"
objectFilename3="./assets/doom.obj"
textureFilename3= "./assets/COLOR_TERRAIN.bmp"
rotate3=[0,0,0]
transform3=[1300+offset[0],100+offset[1],9000+offset[2]]
scale3=[300,300,300]
myRenderer.glLoadObject(objectFilename3,textureFilename3,shaderName3,transform3,scale3,rotate3)



shaderName3= "SMOOTH"
objectFilename3="./assets/witchkingcentered.obj"
textureFilename3= "./assets/Metal1.bmp"
rotate3=[0,-45,0]
transform3=[1000+offset[0],500+offset[1],50+offset[2]]
scale3=[100,100,100]
myRenderer.glLoadObject(objectFilename3,textureFilename3,shaderName3,transform3,scale3,rotate3)



shaderName3= "SMOOTH"
objectFilename3="./assets/nazgulbodycentered.obj"
textureFilename3= "./assets/Fabric2.bmp"
rotate3=[0,-45,0]
transform3=[1000+offset[0],500+offset[1],50+offset[2]]
scale3=[100,100,100]
myRenderer.glLoadObject(objectFilename3,textureFilename3,shaderName3,transform3,scale3,rotate3)









myRenderer.glRender()
myRenderer.glFinish(outputFileName)




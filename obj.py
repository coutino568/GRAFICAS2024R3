from os import read
from texture import *
from mathcou import *
import math
import struct
from collections import namedtuple
#CLASE PARA LEER Y DEFINIR LOS COMPONENTES QUE CONFORMAN AL OBJETO EN LA ESCENA
V3 = namedtuple('Point3', ['x', 'y', 'z'])

class Object() :
    def __init__(self, filename,textureFileName ,shaderName="SMOOTH", translate = V3(0,0,0), scale = V3(1,1,1), rotate = V3(0,0,0)) :
        
        
        self.filename = filename
        self.vertices =[]
        self.faces = []
        self.normals = []
        self.texcoords = []
        self.textureFilename= textureFileName
        self.shaderName= shaderName
        self.transform= translate
        self.rotate=rotate
        self.scale=scale
        self.objectmatrix= [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
        self.transformedVertices =[]
        self.transformedNormals =[]
        
        
        with open(filename, "r") as file:
            self.lines= file.read().splitlines()
        self.readFile()
        # self.printMe()
        if textureFileName !=None:
            self.texture= Texture(self.textureFilename)
            
        # self.printMe()
        self.createObjectMatrix()
        self.transformVertices()
        self.transformNormals()
        
        
    def printMe(self):
        # print("Mis "+str(len(self.vertices))+" vertices son :\n" + str(self.vertices))
        # print("Mis "+str(len(self.faces))+" caras son son :\n" + str(self.faces))
        # print("Mis "+str(len(self.normals))+" normales son :\n" + str(self.normals))
        # print("Mis "+str(len(self.texcoords))+" textcoord son :\n" + str(self.texcoords))
        
        print("Tengo estos vertices  "+str(len(self.vertices)))
        print("tengo estas caras "+str(len(self.faces)) )
        print("tengo estas normales "+str(len(self.normals)))
        print("tengo estas text coords "+str(len(self.texcoords)))
    
        
        
        
    def readFile(self):
        for line in self.lines:
            if line:
                    #divide cada linea en prefijo y contenido
                try:
                        prefix, value = line.split(' ', 1)
                except:
                    continue
                    #clasifica segun prefijos
                    #Vertices
                if prefix == 'v':
                    self.vertices.append(list(map(float, value.split(' '))))
                    #texcoor
                elif prefix == 'vt': 
                    self.texcoords.append(list(map(float, value.split(' '))))
                    #vertex normals
                elif prefix == 'vn': 
                    self.normals.append(list(map(float, value.split(' '))))
                    #faces
                elif prefix == 'f': 
                    self.faces.append( [ list(map(int, vert.split('/'))) for vert in value.split(' ')] )

    #Define la operacion de traslacion de una matriz.
    def transformObject(self,movementX,movementY,movementZ):
        transformationMatrix = [[1,0,0,movementX],[0,1,0,movementY],[0,0,1,movementZ],[0,0,0,1]]
        self.objectmatrix = matrixMultiplication(transformationMatrix,self.objectmatrix )
        # print("Transform matrix created : "+ str(transformationMatrix))
        
        
    
    #Define la operacion de escala de una matriz.
    def scaleObject(self,scaleX,scaleY,scaleZ):
        scaleMatrix = [[scaleX,0,0,0],[0,scaleY,0,0],[0,0,scaleZ,0],[0,0,0,1]]
        # self.objectmatrix = matrixMultiplication(self.objectmatrix, scaleMatrix)
        self.objectmatrix = scaleMatrix
        
        # print("Scale matrix created : " + str(scaleMatrix))
        
    #Define la operacion de traslacion de una matriz.
    def rotateObject(self,rotationX,rotationY,rotationZ):
        pitch = degreesToRad(rotationX)
        yaw = degreesToRad(rotationY)
        roll= degreesToRad(rotationZ)
        
        RotationMatrixX = [[1,0,0,0],[0,math.cos(pitch),-math.sin(pitch),0,0],[0,math.sin (pitch),math.cos(pitch),0],[0,0,0,1]]
        RotationMatrixY = [[math.cos(yaw),0,math.sin(yaw),0],[0,1,0,0],[-math.sin(yaw),0,math.cos(yaw),0],[0,0,0,1]]
        RotationMatrixZ = [[math.cos(roll),-math.sin(roll),0,0],[math.sin(roll),math.cos(roll),0,0],[0,0,1,0],[0,0,0,1]]

        # print(RotationMatrixY)
        # print(RotationMatrixX)
        res1 = matrixMultiplication(RotationMatrixX,RotationMatrixY )
        # print(res1)
        self.RotationMatrix = matrixMultiplication(res1,RotationMatrixZ,)
        self.objectmatrix = matrixMultiplication(self.RotationMatrix,self.objectmatrix)
        # print("Rotation matrix created : " + str(self.RotationMatrix))
        
    def createObjectMatrix(self):
        
        scale= self.scale
        rotate=self.rotate
        transform=self.transform
        self.scaleObject (scale[0],scale[1],scale[2])
        self.rotateObject(rotate[0],rotate[1],rotate[2])
        self.transformObject(transform[0],transform[1],transform[2])
        # print("Object matrix created" + str(self.objectmatrix))
        
        
        
    def transformVertices(self):
        
        for x in range(0, len(self.vertices)):
            #print(str(self.vertices[x]))
            vt = [self.vertices[x][0],self.vertices[x][1],self.vertices[x][2], 1]
            res1= matrixVectorMultiplication(self.objectmatrix, vt)
            # print(res1)
            result = [res1[0]/vt[3],res1[1]/vt[3],res1[2]/vt[3]]
            #print(result)
            self.transformedVertices.append(result)
        print("Vertices transformados")
        
    def transformNormals(self):
        
        
        
        for x in range(0, len(self.normals)):
            #print(str(self.vertices[x]))
            
            vn = [self.normals[x][0],self.normals[x][1],self.normals[x][2], 1]
            res1= matrixVectorMultiplication(self.RotationMatrix, vn)
            # print(res1)
            result = [res1[0]/vn[3],res1[1]/vn[3],res1[2]/vn[3]]
            #print(result)
            self.transformedNormals.append(result)
        print("Normales transformados")
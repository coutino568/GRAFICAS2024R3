import struct

from collections import namedtuple
from obj import *
from  math import *
from mathcou import *
from texture import *

from shader import *

V2 = namedtuple('Point2', ['x', 'y'])
V3 = namedtuple('Point3', ['x', 'y', 'z'])
V4 = namedtuple('Point4', ['x', 'y', 'z', 'w'])


def char(c):
    # used to reduce it to 1 byte

    return struct.pack('=c', c.encode('ascii'))

def word(w):
    # used to reduce it to 2 byte
    return struct.pack('=h',w)

def dword(d):
    # used to reduce it to 4 byte
    return struct.pack('=l',d)

def color(r ,g ,b ):
    #takes input from 0 to 1
    return bytes ([ int(b *255), int(g *255), int(r*255)])



class Renderer(object):
    def __init__(self,width , height, globalLight):
        self.black = color(0,0,0)
        self.bgColor = color(0,0,0)
        self.viewportBgColor = color(0,0,0)
        self.mainColor = color(0,0,1)
        self.glCreateWindow( width, height)
        self.glViewPort(0,0,self.width,self.height)
        self.vertexBuffer = []
        self.objetos =[]
        self.light= globalLight
        self.activeObjectIndex=0
        



    def glCreateWindow (self, width, height):
        self.width = int(width)
        self.height = int(height)
        self.glClear()    
    

    def glViewPort(self, x = 0, y=0, width=1, height = 1):
        self.viewportW = int(width)
        self.viewportH = int(height)
        self.viewportX = int(x)
        self.viewportY = int(y)
        # print("Viewport is defined from : " + str(x) + " , " + str(y) )
        # print("To :  " + str(x+width) + " , " + str(y+height) )
        self.glClear()
        self.glClearviewport()
        


    def pickForegroundColor( self, r,g,b):
        self.mainColor = color(r,g,b)

    def glClear(self):
        self.matrix = [[self.bgColor for x in range(self.width)] for y in range(self.height)]
        self.zBuffer = [[float('inf') for x in range(self.width)] for y in range(self.height)]


    def glClearviewport(self):

        for x in range (self.viewportX, self.viewportX+ self.viewportW):
            for y in range (self.viewportY, self.viewportY+self.viewportH):
                self.matrix[y][x] = self.viewportBgColor

        


    def glClearColor (self, r,g,b):
        self.bgColor = color(r,g,b)

    def glVertex(self,x,y):
        x=int(x)
        y=int(y)
        if (x>= self.viewportX and x <= (self.viewportX+self.viewportW)  and   y>= self.viewportY and y <= self.viewportY+self.viewportH) :
            self.matrix[y][x] = self.mainColor
        # else :
        #     print("point out of viewport")


    def glSetColor(self, r,g,b):
        if(max(r,g,b,1)>1):
            self.mainColor = color(r/255,g/255,b/255)
        else:
            self.mainColor = color(r,g,b)
            
            
    def SetProjectionMatrix(self, nearPlane = 0.1, farPlane = 1000, fov = 60 ):
        top = tan((fov * math.pi / 180) / 2) * nearPlane
        right = top * self.vpWidth / self.vpHeight

        self.projectionMatrix = [[nearPlane/right, 0, 0, 0],
                                           [0, nearPlane/top, 0, 0],
                                           [0, 0, -(farPlane+nearPlane)/(farPlane-nearPlane), -(2*farPlane*nearPlane)/(farPlane-nearPlane)],
                                           [0, 0, -1, 0]]
        
        
    def SetViewMatrix(self, translate = V3(0,0,0), rotate = V3(0,0,0)):
        self.camMatrix = self.glCreateObjectMatrix(translate,V3(1,1,1),rotate)
        self.viewMatrix = matrixInverse(self.camMatrix)
        

    ### es/deberia ser un metodo propio de la clase objeto, pero para la transformacion de la camara es necesario poder acceder a esto como una funcion
    def scaleMatrix(self,scaleX,scaleY,scaleZ):
        scaleMatrix = [[scaleX,0,0,0],[0,scaleY,0,0],[0,0,scaleZ,0],[0,0,0,1]]
        self.cameraMatrix = scaleMatrix
        
    ### es/deberia ser un metodo propio de la clase objeto, pero para la transformacion de la camara es necesario poder acceder a esto como una funcion
    def transformMatrix(self,movementX,movementY,movementZ):
        transformationMatrix = [[1,0,0,movementX],[0,1,0,movementY],[0,0,1,movementZ],[0,0,0,1]]
        self.cameraMatrix = matrixMultiplication(transformationMatrix,self.cameraMatrix )
        
        
    #es un metodo propio de la clase objeto, pero para la transformacion de la camara es necesario poder acceder a esto como una funcion
    def rotateMatrix(self,rotationX,rotationY,rotationZ):
        pitch = degreesToRad(rotationX)
        yaw = degreesToRad(rotationY)
        roll= degreesToRad(rotationZ)
        
        RotationMatrixX = [[1,0,0,0],[0,math.cos(pitch),-math.sin(pitch),0,0],[0,math.sin (pitch),math.cos(pitch),0],[0,0,0,1]]
        RotationMatrixY = [[math.cos(yaw),0,math.sin(yaw),0],[0,1,0,0],[-math.sin(yaw),0,math.cos(yaw),0],[0,0,0,1]]
        RotationMatrixZ = [[math.cos(roll),-math.sin(roll),0,0],[math.sin(roll),math.cos(roll),0,0],[0,0,1,0],[0,0,0,1]]

        res1 = matrixMultiplication(RotationMatrixX,RotationMatrixY )
        RotationMatrix = matrixMultiplication(res1,RotationMatrixZ,)
        self.cameraMatrix = matrixMultiplication(RotationMatrix,self.cameraMatrix)
        
    
    
    
    ## Esta funcion es igual a la de la calse objeto
    def createObjectMatrix(self, scale = (1,1,1), rotation = (0,0,0), transformation = (0,0,0)):
        
        self.scaleMatrix (scale[0],scale[1],scale[2])
        self.rotateMatrix(rotation[0],rotation[1],rotation[2])
        self.transformMatrix(transformation[0],transformation[1],transformation[2])
        #el resultado de estas transformaciones se guardaran en camera matrix
        
    
    
    
    
    
    def glCameraTransform( self, vertex ):
        augmentedVertex = V4(vertex[0], vertex[1], vertex[2], 1)
        res1 = matrixMultiplication(self.viewportMatrix,self.projectionMatrix)
        res2 = matrixMultiplication(res1,self.viewMatrix)
        transformedVertex = matrixMultiplication(res2,augmentedVertex)
        
        transformedVertex = transformedVertex.tolist()[0]

        transformedVertex = V3(transformedVertex[0] / transformedVertex[3],
                         transformedVertex[1] / transformedVertex[3],
                         transformedVertex[2] / transformedVertex[3])

        return transformedVertex
    
    
    
    
    def glLine(self, x0,y0,x1, y1):

        x0 = int(x0)
        y0 = int(y0)
        x1 = int(x1)
        y1 = int(y1)
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        steep = (dy > dx)
        offset = 0
        limit = 0.1
        
        
        
        

        #para pendientes mayores a 1
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1
            

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        y = y0
        try:
            m = dy/dx
        except:
            m= 0

        for x in range(x0, x1 + 1):
            if (steep):
                self.glVertex(y, x)
            else:
                self.glVertex(x, y )

            offset += m
            if offset >= limit:
                y += 1 if y0 < y1 else -1
                limit += 1
                
                
    def glLine2(self, x0,y0,x1, y1):
        pixeles = []
        x0 = int(x0)
        y0 = int(y0)
        x1 = int(x1)
        y1 = int(y1)
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        steep = (dy > dx)
        offset = 0
        limit = 0.1
        
        
        
        

        #para pendientes mayores a 1
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1
            

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        y = y0
        try:
            m = dy/dx
        except:
            m= 0

        for x in range(x0, x1 + 1):
            if (steep):
                pixeles.append([y,x])
            else:
                pixeles.append([x,y])
                

            offset += m
            if offset >= limit:
                y += 1 if y0 < y1 else -1
                limit += 1
        return pixeles


        

    def glTriangle(self, x1,y1,x2,y2,x3,y3):

        x1=x1
        x2=x2
        x3=x3
        y1=y1
        y2=y2
        y3=y3


        self.glLine(x1,y1,x2,y2)
        self.glLine(x1,y1,x3,y3)
        self.glLine(x2,y2,x3,y3)
        return

    def glTriangle2(self, vertex1,vertex2,vertex3):

        x1=vertex1[0]
        x2=vertex2[0]
        x3=vertex3[0]
        y1=vertex1[1]
        y2=vertex2[1]
        y3=vertex3[1]


        self.glLine(x1,y1,x2,y2)
        self.glLine(x1,y1,x3,y3)
        self.glLine(x2,y2,x3,y3)
        return


    colorA=(0,1,0)
    colorB=(1,0,0)
    colorC=(0,0,1)
    
    
    def glTriangle3(self,shaderName, A,B,C,textCoord =[[0.00000,0.000003],[0.5003,0.99000],[0.999001,0.002361]] , normals = []):
        
        minx= max(min(A[0],B[0],C[0]),0)
        maxx= min(max(A[0],B[0],C[0]),self.width)
        miny=max (min(A[1],B[1],C[1]),0)
        maxy= min(max(A[1],B[1],C[1]),self.height)
        
        r,g,b=[1,1,1]
        b/= 255
        g/= 255
        r/= 255
        textureCoordinates = textCoord
        
        
        
        
        for x in range(minx, maxx):
            for y in range(miny, maxy):
                thispoint=[x,y]
                # print(thispoint)
                u,v,w = baricentricCoordinates(A,B,C,thispoint)
                
                
                #Si el punto esta dentro del triangulo, entonces debe obtener el color de la textura  
                if(0<=u<=1 and 0<=v<=1 and 0<=w<=1  and isclose(u+v+w,1.0)):
                  
                    
                    
                    #si mi z es mas cercano al zbuffer en esa posicion, actualizar y pintar . si no , no hacer nada
                    z= u *A[2] + v * B[2] + w*C[2]
                    if  z< self.zBuffer[y][x] :
                        self.zBuffer[y][x] =z
                        
                        
                        # shader="FLAT"
                        
                        #La idea de que el shader retorne textureusage es que se le tenga que enviar informacion de textura al sahder para que despues la regres, mejor solo acceder a la textura directamente, si es necesario
                        ShaderR,ShaderG,ShaderB ,textureUsage= shaderHandler(shaderName,A,B,C,normals, self.light,u,v,w)
                        
                        if textureUsage== True:
                            tA=textureCoordinates[0]
                            tB=textureCoordinates[1]
                            tC=textureCoordinates[2]
                            tx = tA[0] * u + tB[0] * v + tC[0] * w
                            ty = tA[1] * u + tB[1] * v + tC[1] * w
                            if 0<=tx<1 and 0<=ty<1:
                                texColor = self.objetos[self.activeObjectIndex].texture.getColor(tx, ty)
                            
                            else:
                                texColor=[1,1,1]
                        
                            
                            b = (texColor[2] *ShaderB)
                            g = (texColor[1] *ShaderG)
                            r =(texColor[0]  *ShaderR)
                        else:
                            b = (ShaderB)
                            g = (ShaderG)
                            r =(ShaderR)
                        
                        # if flat == True:
                        #     triangleNormal = cross(subtract(B,A),subtract(C,A))
                        #     triangleNormal = normalize(triangleNormal)
                        #     intensity = dotProduct(light,triangleNormal)
                        # else:
                            
                        #     intensity1= dotProduct(light,normals[0])
                        #     intensity2= dotProduct(light,normals[1])
                        #     intensity3=dotProduct(light,normals[2])
                            
                        #     intensity = intensity1*u +intensity2*v+ intensity3*w
                        
                        # if intensity > 0.05 :
                        #     if texColor:
                        #         b = (texColor[2] *intensity)
                        #         g = (texColor[1] *intensity)
                        #         r =(texColor[0]  *intensity)
                        #         # print("intensity: " + str(intensity) + "b:" + str(b) + " g: "+ str(g) + " r : " + str(r))
                        #     else : 
                        #         b,g,r = [0,0,0]
                        # else : 
                        #         b = (texColor[2] *0.05) 
                        #         g = (texColor[1] *0.05)
                        #         r =(texColor[0]  *0.05)
                        #print("Y SI ESTOY ASIGNANDO : "+str(r)+";"+str(g)+";"+str(b))
                        
                        self.glSetColor(r,g,b)
                        self.glVertex(x,y)
                        
      
    def glTrinagleOutside(self,A,B,C):
        
        
        self.glLine(A[0],A[1],B[0],B[1])
        self.glLine(A[0],A[1],C[0],C[1])
        self.glLine(C[0],C[1],B[0],B[1])
                      
                    
    #recibe  un objeto y lo agrega a la escena       
    def glLoadObject(self,filename,texturefilename,shaderName, translate=[0,0,0],scale=[0,0,0],rotate=[0,0,0]):
        # print("recibi que transform es:" + str(translate))
        # print("recibi que rotate es:" + str(rotate))
        # print("recibi que scale es:" + str(scale))
        newObject = Object(filename,texturefilename,shaderName,translate,scale,rotate)
        self.objetos.append(newObject)
        print("Nuevo objeto [" + filename+"] agregado")
        
        
        
        
                
        
        
    def glRender(self):
        for objeto in self.objetos:
            # objeto.createObjectMatrix()
            # objeto.transformVertices()
            
            
            for i in range (0,len (objeto.faces)):
                # print("HARE UN TRIANGULO CON ESTOS VERTICES :"+ str(face))
                ##accede a los vertices indicados por cada cara
                vert1= objeto.transformedVertices[objeto.faces[i][0][0]-1]
                vert2= objeto.transformedVertices[objeto.faces[i][1][0]-1]
                vert3= objeto.transformedVertices[objeto.faces[i][2][0]-1]
                
                
                textcoord1= objeto.texcoords[objeto.faces[i][0][1]-1]
                textcoord2= objeto.texcoords[objeto.faces[i][1][1]-1]
                textcoord3= objeto.texcoords[objeto.faces[i][2][1]-1]
                
                vn1 = objeto.transformedNormals[objeto.faces[i][0][2]-1]
                vn2 = objeto.transformedNormals[objeto.faces[i][1][2]-1]
                vn3 = objeto.transformedNormals[objeto.faces[i][2][2]-1]
                
                
               
                # De una manera muy ineficiente le manda los vertices de cada uno de los triangulos (aun sin transformar, solo redondeado ) y las coordenadas de textura de cada uno de los vertices
                vertices =[[math.floor(vert1[0]), math.floor(vert1[1]) ,math.floor(vert1[2]) ],[math.floor(vert2[0]), math.floor(vert2[1]),math.floor(vert2[2])],[math.floor(vert3[0]), math.floor(vert3[1]) , math.floor(vert3[2])]]
                textCoord= [[textcoord1[0],textcoord1[1]],[textcoord2[0],textcoord2[1]],[textcoord3[0],textcoord3[1]]]
                normals = [[vn1[0],vn1[1],vn1[2]],[vn2[0],vn2[1],vn2[2]],[vn3[0],vn3[1],vn3[2]]]
                
            
                # MAS ADELANTE SE USARA ESTE METODO PARA PASARLE A LA FUNCION tirnagle 3 la respuesta del shader
                self.glTriangle3(objeto.shaderName,vertices[0],vertices[1],vertices[2],textCoord, normals)
                
                # self.glSetColor(1,1,1)
                #self.glTrinagleOutside(vert1,vert2,vert3)
                
            self.activeObjectIndex +=1


    def glFinish(self,filename):
        with open(filename, "wb") as file:
            file.write(bytes('B'.encode('ascii')))
            file.write(bytes('M'.encode('ascii')))
            file.write(dword(14 + 40 + (self.width * self.height * 3)))
            file.write(dword(0))
            file.write(dword(14 + 40))
            
            
            file.write(dword(40))
            file.write(dword(self.width))
            file.write(dword(self.height))
            file.write(word(1))
            file.write(word(24))
            file.write(dword(0))
            file.write(dword(self.width * self.height * 3))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            for y in range(self.height):
                for x in range(self.width):
                    file.write(self.matrix[y][x])
    
    
    def fillTriangle(self, vertex1, vertex2, vertex3):
        #linea de A a B
        self.glLine(vertex1[0],vertex1[1], vertex2[0],vertex2[1])
        #linea de B a C
        self.glLine(vertex2[0],vertex2[1], vertex3[0],vertex3[1])
        #linea de A a C
        self.glLine(vertex1[0],vertex1[1], vertex3[0],vertex3[1])
        #coleccionar todos los puntos sobre el trazo A a C
        #coleccionar todos los puntos sobre el trazo B a C
        #coleccionar todos los puntos sobre el trazo A a B
        puntos = self.glLine2(vertex1[0],vertex1[1], vertex3[0],vertex3[1])
        puntos2= self.glLine2(vertex2[0],vertex2[1], vertex3[0],vertex3[1])
        puntos3= self.glLine2(vertex1[0],vertex1[1], vertex2[0],vertex2[1])
        #lanzar una linea de B a toda la coleccion de puntos en la linea AC.
        # print(puntos)
        for punto in puntos:
            self.glLine(vertex2[0],vertex2[1],punto[0],punto[1])
        #lanzar una linea de A a toda la coleccion de puntos en la linea BC.
        for punto in puntos2:
            self.glLine(vertex1[0],vertex1[1],punto[0],punto[1])
        #lanzar una linea de C a toda la coleccion de puntos en la linea AB.
        for punto in puntos3:
            self.glLine(vertex3[0],vertex3[1],punto[0],punto[1])
        
        
        
    
        
    def polygonGeneral(self, vertices, caras):
        
        for vert in vertices:
            self.glVertex(vert[0],vert[1])
        for cara in caras:
            self.fillTriangle(vertices[cara[0]],vertices[cara[1]],vertices[cara[2]])

    def show(self):
        for x in range(self.height):
            print(self.matrix[x])
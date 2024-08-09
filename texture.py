import struct
from mathcou import *

class Texture(object):
    def __init__(self, filename):
        
        if filename != None:    
            with open(filename, "rb") as image:
                image.seek(10)
                headerSize = struct.unpack('=l',image.read(4))[0]
                
                image.seek(18)
                self.width = struct.unpack('=l',image.read(4))[0]
                self.height = struct.unpack('=l',image.read(4))[0]
                
                image.seek(headerSize)
                self.pixels = []
                
                ##lectura de filas de pixeles dentro de la textura
                for y in range (self.height):
                    pixelsrow = []
                    for x in range(self.width):
                        b = ord(image.read(1)) /255
                        g= ord(image.read(1)) /255
                        r= ord(image.read(1)) /255
                        pixelsrow.append([r,g,b])
                        #print("PIXEL ROW APPENDED: (" + str(r)+" ; "+str(g)+" ; "+str(b)+" )")
                    self.pixels.append(pixelsrow)
                    
        
                
    def getColor(self, u, v):
        if 0<=u<1 and 0<=v<1:
            x =int(v*(self.width-1))
            y = int(u*(self.height-1))
            #print("GET COLOR DEVUELVE:")
            #print(x)
            #print(y)
            #print(self.pixels[y][x])
            # print(self)
            if 0<=x<len(self.pixels[0]) and 0<=y<len(self.pixels):
                return self.pixels[y][x]
            else:
                print("ERROR: SE TRATO DE RETORNAR EL PIXEL DE TEXTURA: \n")
                print(" X : " + str(x)+" ; Y: "+ str(y))
                return None
                
        
        else :
            return None
            
            
    #este metodo deberia retornar los colores basados en las coordinadas uv del triangulo y basado en su uvw
    def getColor2(self,Vertex1x,Vertex1y,Vertex2x,Vertex2y,Vertex3x,Vertex3y,u,v,w) :             
        
        
        myx= 1
        myy=1
        
        pass
    
    def getWidth(self):
        return self.width
    
    def getHeight(self):
        return self.height
        
        
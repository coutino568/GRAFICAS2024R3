scale = 50
from mathcou import *



# def vertexShader(vertex,**kwargs):
# 	# print(vertex)
# 	transformedVertex= [vertex[0]*scale, vertex[1]*scale,vertex[2]*scale]
# 	# print("transformed")
# 	# print(transformedVertex)
# 	return transformedVertex

# def fragmentShader(**kwargs):
# 	color = (1,1,1)
# 	return color


# def blue(shader,A,B,C):
    
#     return 0,0,1




def shaderHandler(shaderName,A,B,C,normals, light,u,v,w):
    r =0
    g=0
    b=0
    if shaderName=="FLAT":
        r,g,b,colorUsage = flat(A,B,C,light)
        return r,g,b,colorUsage
    
    
    elif shaderName=="WIREFRAME":
        r,g,b,colorUsage = wireFrame(A,B,C)
        return r,g,b,colorUsage
        # print("USARE EL SMOOTH SHADER")
        
        
    elif shaderName=="SMOOTH":
        r,g,b,colorUsage = smooth(normals,light,u,v,w)
        return r,g,b,colorUsage
        # print("USARE EL SMOOTH SHADER")
    elif shaderName =="BLACKANDWHITE":
        r,g,b,colorUsage = smooth(normals,light,u,v,w)
        
        return r, g,b, False
    elif shaderName =="BLACKANDWHITEFLAT":
        r,g,b,colorUsage = flat(A,B,C,light)
        
        return r, g,b, False
    
    elif shaderName =="TOON":
        r,g,b,colorUsage = toon(normals,light,u,v,w)
        return r,g,b,colorUsage
    
    elif shaderName =="FRESNEL":
        r,g,b,colorUsage = fresnel(normals,u,v,w)
        return r,g,b,colorUsage
    elif shaderName =="GLOW":
        r,g,b,colorUsage = glow(normals,u,v,w,light)
        return r,g,b,colorUsage
        
        
    else:
        r,g,b,colorUsage = smooth(normals,light,u,v,w)
        return r, g,b, False
        
        
    
def wireFrame(A,B,C):
    
    r = 1
    g = 1
    b= 1
    
    return r,g,b, False
    
    
    
    
    

def flat(A,B,C,light):
    
    triangleNormal = cross(subtract(B,A),subtract(C,A))
    triangleNormal = normalize(triangleNormal)
    intensity = dotProduct(light,triangleNormal)
    
    
    r= max(0.05, intensity)
    g= max(0.05, intensity)
    b= max(0.05, intensity)
    colorUsage=True
    
    return r,g,b,colorUsage
    
def smooth(normals,light,u,v,w):
    colorUsage= True
    intensity1= dotProduct(light,normals[0])
    intensity2= dotProduct(light,normals[1])
    intensity3= dotProduct(light,normals[2])
                            
    intensity = intensity1*u +intensity2*v+ intensity3*w
    if intensity> 0.05:
        return intensity,intensity,intensity,colorUsage
    else:
        return 0.05,0.05,0.05,colorUsage
    
    
    
def toon(normals,light,u,v,w):
    colorUsage= True
    intensity1= dotProduct(light,normals[0])
    intensity2= dotProduct(light,normals[1])
    intensity3= dotProduct(light,normals[2])
                            
    intensity = intensity1*u +intensity2*v+ intensity3*w
    if intensity>0.8:
        return 0.9,0.9,0.9,colorUsage
    elif intensity>0.4:
        return 0.6,0.6,0.6,colorUsage
    if intensity>0.2:
        return 0.4,0.4,0.4,colorUsage    
    if intensity> 0.05:
        return 0.2,0.2,0.2,colorUsage
    else:
        return 0.05,0.05,0.05,colorUsage
    

def fresnel(normals,u,v,w):
    colorUsage= False
    camera= [0,0,-1]
    intensity1= dotProduct(camera,normals[0])
    intensity2= dotProduct(camera,normals[1])
    intensity3= dotProduct(camera,normals[2])
                            
    intensity = intensity1*u +intensity2*v+ intensity3*w
    if intensity>0.9:
        return (1-intensity)*0.05,(1-intensity)*0.05,(1-intensity)*0.05,colorUsage
    elif intensity>0.4:
        return (1-intensity)*0.3,(1-intensity)*0.3,(1-intensity)*0.3,colorUsage
       
    if intensity> 0.2:
        return 1-intensity,1-intensity,1-intensity,colorUsage
    else:
        return 0.05,0.05,0.05,colorUsage
    
    
    
# talvez para este si hace sentido pasarle la informacion de textura
def glow(normals,u,v,w,light):
    color= [0,1,0.5]
    r,g,b, res = fresnel(normals,u,v,w)
    if r<0.3:
        
        r,g,b,colorUsage = smooth(normals,light,u,v,w)
        colorUsage= True
        return r,g,b,colorUsage
        
    else:
        colorUsage= False
        return color[0],color[1],color[2],colorUsage
    
    
    
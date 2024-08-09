
import numpy as np

import math

#para multiplicaciones de dos matrices
def matrixMultiplication(matrix1, matrix2):
    
    result =  [[0 for x in range(len(matrix1))] for y in range(len(matrix2[0]))]
    
    if(len(matrix1[0])== len(matrix2)):
        #print("Tamaño valido")
        
        for i in range(0, len(matrix1)):
            for j in range(len(matrix2[0])):
                for k in range(len(matrix2)):
                    result[i][j] += matrix1[i][k] * matrix2[k][j]
                
        return result     
        
    
    else:
        print("Tamaño Invalido")
    
def degreesToRad(angle):
    return (math.pi*angle) / 180

def vectorAndScalarMultiplication (Vector, Scalar):
    result= []
    for i in range (0,len(Vector)):
        result.append(Vector[i]*Scalar)
    return result


#para operacion de un vectori y una matriz
def matrixVectorMultiplication (matrix, vector):
    result2= [0 for t in  range(len(matrix))]
    
    # print(result)
    
    if(len(vector)==len(matrix[0])):
        #print("Tamaño valido")
        
        for i in range(len(matrix)):
            #rowresult=0
            temp =0
            for j in range(len(matrix[0])):
                temp= temp+ (matrix[i][j]*vector[j])
            result2[i] = temp
            
        return result2       
                
        # print(result)        
    else:
        print("Tamaño invlaido")
        

def matrixInverse(matrix):
    if len(matrix[0])==4  and len(matrix)==4:
        #es una matriz de 4 x4
        result= [[0 for x in  range(len(matrix)*2)] for y in range (len(matrix[0]))]
        augmentedMatrix= [[0 for x in  range(len(matrix))] for y in range (len(matrix[0]))]
        identity = [[ 1 if x==y else  0  for x in  range(len(matrix))] for y in range (len(matrix[0]))]
        
        
        
    print(result)
    print(identity)
        
    pass
    


def dotProduct (Vector1, Vector2):
    if len(Vector1) == len(Vector2):
        result = 0
        for i in range(len(Vector1)):
            result += Vector1[i]*Vector2[i]
        
        return result
        
    else:
        return []
    
    
# print(dotProduct([1,3],[5,4]))

def subtract(Vector1, Vector2) :
    if len(Vector1) == len(Vector2):
        result = []
        for i in range(len(Vector1)):
            result.append(Vector1[i]-Vector2[i])
        return result
        
    else:
        return []

##solo funcionara para vectorees de 2 o 3
def cross(Vector1,Vector2):
    if len(Vector1) == len(Vector2):
        
        if len(Vector1)==2:
            result = (Vector1[0]*Vector2[1]) - (Vector1[1]*Vector2[0])
            
            return result
        else:
            if len(Vector1)==3:
                result = [(Vector1[1]*Vector2[2] - Vector1[2]*Vector2[1]),(Vector1[2]*Vector2[0] - Vector1[0]*Vector2[2]), (Vector1[0]*Vector2[1] - Vector1[1]*Vector2[0])]
                return result
        
        
        
    else:
        return []
    


def baricentricCoordinates(A, B, C, P):
    
    ABC_Area = getAreaOfTiangle(A,B,C)
    PBC_Area= getAreaOfTiangle(P,B,C)
    APC_Area= getAreaOfTiangle(A,P,C)
    ABP_Area= getAreaOfTiangle(A,B,P)
    
    
    if ABC_Area ==0:
        u= 0
        v= 0
        w= 0
        return u,v,w
    
    if PBC_Area ==0 :
        u= 0
        v= APC_Area/ABC_Area
        w=  ABP_Area/ ABC_Area
        return u,v,w
    
    
    if ABP_Area ==0:
        u= PBC_Area/ABC_Area
        v= APC_Area/ABC_Area
        w=  0
        return u,v,w
    
    if APC_Area ==0: 
        u= PBC_Area/ABC_Area
        v= 0
        w= ABP_Area/ ABC_Area  
        return u,v,w
        
    
        
    else :
        u= PBC_Area/ABC_Area
        v= APC_Area/ABC_Area
        w=  ABP_Area/ ABC_Area
    
    
    return u,v,w
    
    
    
def normalize(Vector):
    magnitude= 0
    if(len(Vector)==1):
        return Vector[0]
    elif len(Vector)==2:
        magnitude= math.sqrt(Vector[0]*Vector[0] +Vector[1]*Vector[1])
        return [Vector[0]/ magnitude, Vector[1]/magnitude]
    elif len(Vector)==3:
        magnitude= math.sqrt(Vector[0]*Vector[0] +Vector[1]*Vector[1] +Vector[2]*Vector[2])
        return [Vector[0]/ magnitude, Vector[1]/magnitude,Vector[2]/magnitude]
    
def getmagnitude(Vector):
    magnitude= 0
    if(len(Vector)==1):
        return Vector[0]
    elif len(Vector)==2:
        return math.sqrt(Vector[0]*Vector[0] +Vector[1]*Vector[1])
         
    elif len(Vector)==3:
        return math.sqrt(Vector[0]*Vector[0] +Vector[1]*Vector[1] +Vector[2]*Vector[2])
    
    
def getAreaOfTiangle(A,B,C):
    # print (A)
    # print (B)
    # print(C)
    result = 0.5*((A[0]*B[1])+(B[0]*C[1])+(C[0]*A[1]))- 0.5*((A[1]*B[0])+(B[1]*C[0])+(C[1]*A[0]))
    
    
    
    return result



# matrix = [[5,6,8,10],[10,-5,8,5],[5,8,10,5],[0,0,0,1]]

# matrixInverse(matrix)
from PIL import Image
from Circle import *
import math
from random import randint
from tqdm import tqdm
from joblib import Parallel, delayed



def isHexa(hexa):
    if len(hexa)!= 6 and len(hexa)!= 7:
        return False

    if len(hexa) == 7 and hexa[0] != '#':
        return False
    if len(hexa)==7:
        hexa = hexa[1:]
    possibleChar = 'aAbBcCdDeEfF0123456789'
    for i in hexa:
        if i not in possibleChar:
            return False
    return True

def normalizeMask(mask):
    temp = max(mask)
    return [mask[0]/temp, mask[1]/temp, mask[2]/temp]

def saveImg(img, name=None):
    nameToSave = input("Choose the file name to save the image, including the extension : ") if name is None else name
    img = img.save("samples/"+nameToSave)



def createUniformImageWithHexa(hexa, largeur, hauteur):
    if not isHexa(hexa):
        print("Wrong hexadecimal format.")
        return isHexa(hexa)
    
    if len(hexa)==7:
        hexa = hexa[1:]

    hexaInInt = list(map(lambda x : int(x, 16), [hexa[0:2],hexa[2:4], hexa[4:]]))

    img = Image.new('RGB', (largeur,hauteur), color = (int(hexaInInt[0]),int(hexaInInt[1]),int(hexaInInt[2])))
    
    return img


def is_point_in_circle(i, j, circle : Circle):

    distance = math.sqrt((i - circle.x)**2 + (j - circle.y)**2)
    return distance <= circle.radius

def filterNegative(img):
    (largeur,hauteur)=img.size
    newImg = Image.new('RGB', (largeur,hauteur), color = (0, 0, 0))
    for i in range (largeur):
        for j in range (hauteur):
            p=img.getpixel((i,j))
            newImg.putpixel((i,j),((255-p[0]),(255-p[1]),(255-p[2])))
    return newImg



def addCircleInMatrix(circle, matrix, opacity=128):

    (largeur,hauteur)=len(matrix), len(matrix[0])
    for i in range (circle.x - circle.radius - 1, min(circle.x + circle.radius + 1, largeur)):
        for j in range (circle.y - circle.radius - 1, min(circle.y + circle.radius + 1, hauteur)):
            if is_point_in_circle(i,j,circle):
                p=matrix[i][j]
                new_color = (
                    min(255, (circle.color[0]) + p[0]//circle.z),
                    min(255, (circle.color[1]) + p[1]//circle.z),
                    min(255, (circle.color[2]) + p[2]//circle.z),
                )
                blended_color = (
                    (p[0] * (255 - opacity) + new_color[0] * opacity) // 255,
                    (p[1] * (255 - opacity) + new_color[1] * opacity) // 255,
                    (p[2] * (255 - opacity) + new_color[2] * opacity) // 255,
                )
                matrix[i][j] =  blended_color
    
    return matrix

def getMatrixFromImage(img):
    matrixPixel = []
    (largeur,hauteur)=img.size
    for i in range (largeur):
        line = []
        for j in range (hauteur):
            line.append(img.getpixel((i,j)))
        matrixPixel.append(line)
    return matrixPixel

def getImageFromMatrix(matrix):
    largeur, hauteur = len(matrix), len(matrix[0])
    img = Image.new('RGB', (largeur,hauteur), color = (0, 0, 0))
    for i in range (largeur):
        for j in range (hauteur):
            p=matrix[i][j]
            img.putpixel((i,j),(p[0],p[1],p[2]))
    return img


def addLayerOfCircles(matrix, nbCircle, numLayer, para=False):

    newMatrix = deepCopyMatrix(matrix)

    (largeur,hauteur)=len(newMatrix), len(newMatrix[0])
    maxRadius = (largeur+hauteur)//2 // 10
    minRadius = (largeur+hauteur)//2 // 20

    circles = []

    for _ in range (nbCircle):
        color = [randint(0, 255),randint(0, 255),randint(0, 255)]
        circle = Circle(
            x=randint(0,largeur), 
            y=randint(0,hauteur), 
            z=numLayer+1,
            radius=randint(minRadius, maxRadius), 
            color=color)
        circles.append(circle)

    if not para :

        progress_bar = tqdm(total=len(circles), desc="Processing")
        for c in range(len(circles)):
            newMatrix = addCircleInMatrix(circles[c], newMatrix)
            progress_bar.update(1)

        progress_bar.close()
    else:
        for c in range(len(circles)):
            newMatrix = addCircleInMatrix(circles[c], newMatrix)
    
    return newMatrix


def multipleLayers(largeur, hauteur, nbCircle, nbLayer, hexa="#FFFFFF"):

    img = createUniformImageWithHexa(hexa, largeur, hauteur)

    matrix = getMatrixFromImage(img)
    for i in range(1, nbLayer+1):
        matrix = addLayerOfCircles(matrix, nbCircle, i)
        
    newImg = getImageFromMatrix(matrix)
    return newImg

def applyMatrixOnMatrix(frontMatrix, backMatrix, z, opacity=12):

    newMatrix = deepCopyMatrix(backMatrix)

    (largeur,hauteur)=len(backMatrix), len(backMatrix[0])
    for i in range (largeur):
        for j in range (hauteur):
            back=backMatrix[i][j]
            front = frontMatrix[i][j]
            new_color = (
                min(255, ((front[0])*z + back[0]*(z-1)) //(2*z-1)),
                min(255, ((front[1])*z + back[1]*(z-1)) //(2*z-1)),
                min(255, ((front[2])*z + back[2]*(z-1)) //(2*z-1)),
            )
            
            newMatrix[i][j] =  new_color
    
    return newMatrix

def multipleLayersParallel(largeur, hauteur, nbCircle, nbLayer, z=2, hexa="#FFFFFF"):
    img = createUniformImageWithHexa(hexa, largeur, hauteur)

    firstMatrix = getMatrixFromImage(img)


    allMatrix = Parallel(n_jobs=-1)(delayed(addLayerOfCircles)(firstMatrix, nbCircle, i, True) for i in range(1, nbLayer + 1))
    newMatrix = deepCopyMatrix(firstMatrix)

   

    for i in range(len(allMatrix)):
        newMatrix = applyMatrixOnMatrix(allMatrix[i], newMatrix, 10)
    newImg = getImageFromMatrix(newMatrix)
    
    return newImg        


def deepCopyMatrix(matrix):
    newMatrix = []
    for i in range(len(matrix)):
        line = []
        for j in range(len(matrix[i])):
            line.append(matrix[i][j])
        newMatrix.append(line)

    return newMatrix
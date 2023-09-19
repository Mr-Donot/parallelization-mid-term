from PIL import Image
from Circle import *
import math
from random import randint
from tqdm import tqdm

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

def saveImg(img):
    nameToSave = input("Choose the file name to save the image, including the extension : ")
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


def addCircleInImg(img, circle : Circle, deepFactor=1, opacity = 128):

    (largeur,hauteur)=img.size
    for i in range (circle.x - circle.radius - 1, min(circle.x + circle.radius + 1, largeur)):
        for j in range (circle.y - circle.radius - 1, min(circle.y + circle.radius + 1, hauteur)):
            if is_point_in_circle(i,j,circle):
                p=img.getpixel((i,j))
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
                img.putpixel((i, j), blended_color)

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


def addMultipleCircle(img, nbCircle):

    (largeur,hauteur)=img.size
    maxRadius = (largeur+hauteur)//2 // 10
    minRadius = (largeur+hauteur)//2 // 20
    circles = []
    for _ in range (nbCircle):
        color = [randint(0, 255),randint(0, 255),randint(0, 255)]
        circle = Circle(
            x=randint(0,largeur), 
            y=randint(0,hauteur), 
            z=randint(1, 5), 
            radius=randint(minRadius, maxRadius), 
            color=color)
        circles.append(circle)

    sorted_circles = sorted(circles, key=lambda circle: circle.z)
    progress_bar = tqdm(total=len(sorted_circles), desc="Processing")
    for c in range(len(sorted_circles)) :
        progress_bar.update(1)
        addCircleInImg(img, sorted_circles[c], 2)
    progress_bar.close()
    return img
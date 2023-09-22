from utils import *
import time


if __name__ == '__main__':

    largeur = 192
    hauteur = 108
    nbCircle = 50
    nbLayer = 5
    initHexa = "#FFFFFF"
    z=2

    t0 = time.time()

    img = multipleLayersParallel(largeur, hauteur, nbCircle, nbLayer, z, initHexa)
    t1 = time.time()

    

    i2 = multipleLayers(largeur, hauteur, nbCircle, nbLayer, initHexa)
    t2 = time.time()

    print(f"temps para : {t1-t0}")
    print(f"temps non-para : {t2-t1}")

    img.show()
    i2.show()    



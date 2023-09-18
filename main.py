from utils import *

largeur = 500
hauteur = 500
img = createUniformImageWithHexa("#FFFFFF", largeur, hauteur)

nbCircle = 100

img = addMultipleCircle(img, nbCircle)


img.show()
#filterNegative(img).show()


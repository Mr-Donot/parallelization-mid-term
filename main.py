from utils import *

largeur = 500
hauteur = 500
img = createUniformImageWithHexa("#FFFFFF", largeur, hauteur)

nbCircle = 100
modPrint = 50

img = addMultipleCircle(img, nbCircle)


img.show()
#filterNegative(img).show()

#idee de parallelisation : 
    #- 1
    #- trier les cercles par z croissant
    #- pour chaque "étage" (z), dessinez les cercles en para, puis go to next etage

    #- 2
    #-paralléliser le changement de couleurs de chaque pixels du cercle, mais un cercle par un

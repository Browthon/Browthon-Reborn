def majdb(fichier, versionacc, versioncompa):
    while versionacc < versioncompa:
        eval("majdbto" + str(versionacc + 1) + "(" + fichier + ")")
        versionacc += 1
    return versionacc

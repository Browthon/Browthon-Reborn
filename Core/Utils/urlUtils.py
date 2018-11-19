def getGoodUrl(db, url):
    if "http://" in url or "https://" in url:
        return url
    elif "." in url:
        return "http://"+url
    else:
        return searchMoteur(db, url)

def searchMoteur(db, url):
    moteur = db.executeWithReturn("""SELECT moteur FROM parameters""")[0][0]
    if moteur == "Google":
        return "http://google.fr/?gws_rd=ssl#q="+url

def getgoodurl(db, url):
    if "http://" in url or "https://" in url:
        return url
    elif "." in url:
        return "http://"+url
    else:
        return searchmoteur(db, url)


def searchmoteur(db, url):
    moteur = db.executewithreturn("""SELECT moteur FROM parameters""")[0][0]
    if moteur == "Google":
        return "http://google.fr/?gws_rd=ssl#q="+url
    elif moteur == "Duckduckgo":
        return "https://duckduckgo.com/?q="+url
    elif moteur == "Ecosia":
        return "https://www.ecosia.org/search?q="+url
    elif moteur == "Yahoo":
        return "https://fr.search.yahoo.com/search?p="+url
    elif moteur == "Bing":
        return "https://www.bing.com/search?q="+url

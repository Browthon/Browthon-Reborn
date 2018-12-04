def getgoodurl(db, url):
    raccourcis = db.executewithreturn("""SELECT * FROM raccourcis""")
    for i in raccourcis:
        if i[1] == url:
            url = i[2]
    sessions = db.executewithreturn("""SELECT * FROM sessions""")
    for i in sessions:
        if i[1] == url:
            return i[2], "SESSION"

    if "http://" in url or "https://" in url:
        return url, "NP"
    elif "." in url:
        return "http://"+url, "NP"
    else:
        return searchmoteur(db, url), "NP"


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

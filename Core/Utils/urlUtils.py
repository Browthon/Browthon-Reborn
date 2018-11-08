def getGoodUrl(url):
    if "http://" in url or "https://" in url:
        return url
    elif "." in url:
        return "http://"+url
    else:
        return "http://google.fr/?gws_rd=ssl#q="+url
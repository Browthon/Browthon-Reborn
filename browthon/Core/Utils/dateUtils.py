from datetime import datetime


def getdate():
    now = datetime.now()
    return str(now.day)+" / "+str(now.month)+" / "+str(now.year)

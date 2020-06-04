import praw
import instabot
import json
import os
import requests

rusername=""
rpassword=""
subreddit=""
rclient_secret=""
rclient_id=""
instauser = ""
instapass = ""
savingthis = ""
img_count = 1
pictitle = ""
count = 0
def instainit(picname):
    global instauser,instapass,pictitle
    bot = instabot.Bot()
    bot.login(username=instauser,password=instapass)
    bot.upload_photo(picname,caption=pictitle)
    bot.logout()
def fixname(name):
    fixname = name
    prohibited = ["<",">",":","/","\\","|","?","*"]
    for chr in prohibited:
        fixname = fixname.replace(chr,"_")
    print(fixname)
    return fixname
def saveimg(piclink,name,ext):
    global count,img_count,instauser,instapass,savingthis,pictitle
    if count != img_count:
        image = requests.get(piclink)
        print(piclink)
        if image.status_code == 200:
            try:
                saveithere = os.getcwd() + "\\pics\\"
                savingthis = saveithere+name+ext
                if os.path.exists(saveithere) != True:
                    os.mkdir(saveithere)
                if os.path.isfile(savingthis) == False:
                    saving_handler = open(savingthis,mode="bx")
                    saving_handler.write(image.content)
                    count +=1
                    print("[+] "+name)
                    savingthis = saveithere+name+ext
                    instainit(savingthis)
            except Exception as e:
                print(e)
                exit(0)
                pass
    else:
        pass
def getsettings():
    global rusername,rpassword,subreddit,rclient_secret,rclient_id,instauser,instapass
    f = open("config.json",mode="r")
    data = json.load(f)
    rusername = data["rusername"]
    rpassword = data["rpassword"]
    subreddit = data["subreddit"]
    rclient_secret = data["client_secret"]
    rclient_id = data["client_id"]
    instauser = data["instauser"]
    instapass = data["instapass"]
def init_reddit(rusername,rpassword,subreddit,rclient_secret,rclient_id):
    global pictitle
    reddit = praw.Reddit(username=rusername,password=rpassword,client_secret=rclient_secret,client_id=rclient_id,user_agent='redditsub get pics v2')
    subreddi = reddit.subreddit(subreddit)
    for sub in subreddi.top(limit=None):
        if sub.url.endswith(".jpg"):
            saveimg(sub.url,fixname(sub.title),".jpg")
            pictitle = sub.title
            pass
        elif sub.url.endswith(".png"):
            saveimg(sub.url,fixname(sub.title),".png")
            pictitle = sub.title
            pass
        elif sub.url.endswith(".jpeg"):
            saveimg(sub.url,fixname(sub.title),".jpeg")
            pictitle = sub.title
            pass
        else:
            pass
def main():
    global rusername,rpassword,subreddit,rclient_secret,rclient_id
    getsettings()
    while True:
        init_reddit(rusername,rpassword,subreddit,rclient_secret,rclient_id)
        time.sleep(18000)
    pass

if __name__ == "__main__":
    main()
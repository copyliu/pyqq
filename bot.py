#!/usr/bin/env python3
#coding=utf-8
#
# Author: maplebeats
#
# gtalk/mail: maplebeats@gmail.com
#
# Last modified:	2012-08-23 18:41
#
# Filename:		bot.py
#
# Description: SB机器人
#
from StringIO import StringIO
import os
import uuid

import MultipartPostHandler
import json
import urllib as parse
import urllib2 as request
import cookielib as cookiejar
import re
import time
#import sqlite3
import datetime
from PIL import Image,ImageDraw,ImageFont
def _(string):
    try:
        return string.encode("u8")
    except:
        return string


def numberformat(number,unit="ISK"):
    if float(number)<0:
        return u"暂无出价"
    s=format(number,',.2f')
    if unit:
        return s+" "+unit
    else:
        return s


class Bot:

    def _request(self, url, data=None, opener=request.build_opener()):
        if data:
            data = parse.urlencode(data).encode('utf-8')
            rr = request.Request(url,data,self._headers)
        else:
            rr = request.Request(url=url, headers=self._headers)
        fp = opener.open(rr)
        try:
            res = fp.read().decode('utf-8')
        except:
            res = fp.read()
        fp.close()
        return res

    def __init__(self):
        self._headers = {
                                 "User-Agent":"A QQBOT!",
                                 "Accept-Language":"zh-cn,en;q=0.8,en-us;q=0.5,zh-hk;q=0.3",
                                 "Accept-Encoding":"deflate",
                }
        #self.simi_init()

        self.help = re.compile(r"^\.help$")


    def makepic(self,msg):
        im=Image.new("RGB", (275,100),"#FFFFFF")
        draw = ImageDraw.Draw(im)
        font = ImageFont.truetype("ml.ttf", 12,encoding="unic")
        y_text = h = w = 0
        lines=msg.split("\n")
        for line in lines:
            width, height = font.getsize(line)
            draw.text((0, y_text), line.decode("utf8"), font = font, fill = "rgb(0,0,0)")
            y_text += height
        fname=str(uuid.uuid4())
        f = open(fname+".png","wb")
        im.save(f, "PNG")
        f.close()
        f=open(fname+".png","rb")
        url="http://up.web2.qq.com/cgi-bin/cface_upload?time=%s"%int(time.time())
        opener=request.build_opener(MultipartPostHandler.MultipartPostHandler)
        data={"from":"control","f":"EQQ.Model.ChatMsg.callbackSendPicGroup","vfwebqq":str(self.qqlogin["vfwebqq"]),"field":"3",
              "custom_face":f}

        response=opener.open(url, data).read().decode("utf8")
        jsonstart,jsonend = response.find("{"), response.find("}")+1
        s=response[jsonstart:jsonend]
        s=s.replace("'",'"')
        pic=json.loads(s)
        f.close()
        os.remove(fname+".png")
        return "\n",_(pic["msg"].split(" ")[0])

    def reply(self,msg,msg_time=datetime.datetime.now(),buddy_name=None,buddy_num=None,qun_name=None,qun_num=None):
        msg=msg.strip()
        l = self.help.search(msg)
        if l :
            return self.makepic("幫助信息")

        return None,None


    def gettime(self):
        import datetime
        return datetime.datetime.today().strftime('%Y年%m月%d日%H:%M:%S')

    @staticmethod
    def gettitle(link):
        pass

    def simi_init(self):
        simi_Jar = cookiejar.CookieJar()
        self.simi_opener = request.build_opener(request.HTTPCookieProcessor(simi_Jar))
        self._headers = {
                         "User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:14.0) Gecko/20100101 Firefox/14.0.1",
                         "Accept-Language":"zh-cn,en;q=0.8,en-us;q=0.5,zh-hk;q=0.3",
                         "Accept-Encoding":"deflate",
                         "Referer":"http://www.simsimi.com/talk.htm"
        }
        urlv = "http://www.simsimi.com/func/req?%s" % parse.urlencode({"msg": "hi", "lc": "zh"})
        self._request(url=urlv,opener=self.simi_opener)

    def simi_bot(self,req):
        pu = parse.urlencode({"msg": req, "lc": "zh"})
        urlv = "http://www.simsimi.com/func/req?%s" % pu
        res = self._request(urlv,opener=self.simi_opener)
        if res =="{}":
            return False
        else:
            return _(json.loads(res)['response'])

    def hito_bot(self):
        urlv = "http://api.hitokoto.us/rand"
        res = request.urlopen(urlv).read().decode()
        hit = json.loads(res)
        return _(hit['hitokoto'])

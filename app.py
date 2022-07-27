from flask import Flask, request, render_template
import pandas as pd
from regex import L
from scipy.__config__ import show
from TikTokAPI import TikTokAPI
import re
import requests
from utils import random_key, build_get_url, get_req_json, get_req_content, get_req_text
from tiktok_browser import TikTokBrowser
import random
import string
import urllib
from datetime import datetime
import json
import pprint
import sys
import TiktokCvox
sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')
from TiktokCvox import *



app=Flask(__name__)

#Tiktok library
Api = Tiktok()

def truncate(num):
    return re.sub(r'^(\d+\.\d{,2})\d*$',r'\1',str(num))

def send_get_request( url, params, extra_headers=None):
        url = build_get_url(url, params)
        did = ''.join(random.choice(string.digits) for num in range(19))
        url = build_get_url(url, {did_key: did}, append=True)
        signature = tiktok_browser.fetch_auth_params(url, language=language)
        url = build_get_url(url, {signature_key: str(signature)}, append=True)
        if extra_headers is None:
            headers = header
        else:
            headers = {}
            for key, val in extra_headers.items():
                headers[key] = val
            for key, val in headers.items():
                headers[key] = val
        data = get_req_json(url, params=None, headers=headers)
        return data

headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36 OPR/72.0.3815.378'}
jsn = json.load(open("cookie.json", "r", encoding="utf-8"))
api = TikTokAPI(jsn)

counttiktok = pd.DataFrame(columns = ['Likes', 'Comment', 'Share'])
cookie=None

user_agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0"
browser_lang = "en-US"
timezone = "Asia/Kolkata"
region='IN'
language='en'
did_key = "did"
tiktok_browser = TikTokBrowser(user_agent)
signature_key = "_signature"

if cookie is None:
    cookie = {}
verifyFp = cookie.get("s_v_web_id", "verify_kjf974fd_y7bupmR0_3uRm_43kF_Awde_8K95qt0GcpBk")
tt_webid = cookie.get("tt_webid", "6913027209393473025")

header= {
            'Host': 't.tiktok.com',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0',
            'Referer': 'https://www.tiktok.com/',
            'Cookie': 'tt_webid_v2={}; tt_webid={}'.format(tt_webid, tt_webid)
        }

default_params = {
            "aid": "1988",
            "app_name": "tiktok_web",
            "device_platform": "web",
            "referer": "",
            "user_agent": urllib.parse.quote_plus(user_agent),
            "cookie_enabled": "true",
            "screen_width": "1920",
            "screen_height": "1080",
            "browser_language": browser_lang,
            "browser_platform": "Linux+x86_64",
            "browser_name": "Mozilla",
            "browser_version": "5.0+(X11)",
            "browser_online": "true",
            "timezone_name": timezone,
            "page_referer": "https://www.tiktok.com/foryou?lang=en",
            "priority_region": region,

            "appId": "1180",
            "region": region,
            "appType": "t",

            "isAndroid": "false",
            "isMobile": "false",
            "isIOS": "false",
            "OS": "linux",
            "tt-web-region": region,

            "language": language,
            "verifyFp": verifyFp
        }



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index.html')
def home():
    return render_template('index.html')

@app.route('/login.html')
def login():
    return render_template('login.html')

@app.route('/tiktok' , methods = ["POST","GET"])
def tiktok():
    usrname = str(request.form.get("usrname"))
    print(usrname)
    
    #get 15 feeds

    url = 'https://tiktok.com/@%s' % usrname
    Api.openBrowser(url, True)
    limit = 30
    count = 0
    first = True
    flag = 0
    cursor = 0
    secUid = ''
    vid_id = []
    while True:
        if first == True:
            data = Api.getUserFeed(first=first)
            for x in data['ItemModule']:
                video_id = data['ItemModule'][x]['id']
                vid_id.append(video_id)
                count += 1
                if count == limit:
                    flag = 1
                    break
            if not data['ItemList']['user-post']['hasMore']:
                break
            cursor = data['ItemList']['user-post']['cursor']
            secUid = data['UserPage']['secUid']
        else:
            data = Api.getUserFeed(secUid=secUid, cursor=cursor, first=first)
            for x in data['itemList']:
                video_id = str(x['id'])
                count += 1
                if count == limit:
                    flag = 1
                    break
            if not data['hasMore']:
                break
            cursor = data['cursor']
        if flag == 1:
            break
        first = False
    Api.closeBrowser()
    print(len(vid_id))
    out = []
    url = "https://t.tiktok.com/node/share/user/@" + usrname
    params = {
            "uniqueId": usrname,
            "validUniqueId": usrname,
        }
    for key, val in default_params.items():
        params[key] = val
    retval = send_get_request(url=url, params=params)
    
    user_obj = retval["userInfo"]["user"]
    user_id = user_obj["id"]
    secUid = user_obj["secUid"]
    # url = "https://t.tiktok.com/api/post/item_list/"
    req_default_params = {
            "type": "1",
            "maxCursor": "0",
            "minCursor": "0",
            "sourceType": "8",
        }
    params = {
            "id": user_id,
            "secUid": secUid,
            "count": str(28)
        }
    for key, val in req_default_params.items():
            params[key] = val
    for key, val in default_params.items():
        params[key] = val
    # feed = send_get_request(url, params)
    
    # print(user, " || " , retval,  " || ", retval['statusCode'])
    try:
        Link = retval['userInfo']['user']['bioLink']['link']
    except:
        Link = ""
    if retval['statusCode'] == 10000:
        out = [['maintenance','maintenance','maintenance'],['maintenance','maintenance','maintenance'],['maintenance','maintenance','maintenance']]
    else:
        Name = retval['userInfo']['user']['nickname']
        Bio = retval['userInfo']['user']['signature']
        # Link = retval['userInfo']['user']['bioLink']['link']
        Profile_pict = retval['userInfo']['user']['avatarLarger']
        Total_followers = retval['userInfo']['stats']['followerCount']
        Total_post = retval['userInfo']['stats']['videoCount']
        Total_like = retval['userInfo']['stats']['heartCount']
        Evg_like = int(Total_like) / int(Total_post)
        showdata = [Name,Bio,Link,Profile_pict,Total_followers,Total_post, Evg_like]
    
    #get more data tiktok
    user = retval['userInfo']
    param = {
            "type": 1,
            "secUid": "",
            "id": user['user']['id'],
            "count": int(retval['userInfo']['stats']['videoCount']),
            "minCursor": 0,
            "maxCursor": 0,
            "shareUid": "",
            "lang": "",
            "verifyFp": "",
            }
    Like, Comment, Share, Views, caption , linkpost , erp, cover= [], [], [], [], [], [], [], []
    for id in range(29,14,-1):
        url = 'https://www.tiktok.com/node/share/video/@tiktok/' + vid_id[id]
        print(url)
        data = requests.get(url, params=param, headers=headers)
        print(data)
        data = data.json() #error "json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)"
        
        filename = 'user.json'
        with open(filename, 'w') as file_object:  #open the file in write mode
                json.dump(data, file_object)
        file = open('user.json')
        dataTik = json.load(file)
        # print(dataTik)
        ER = (int(dataTik['itemInfo']['itemStruct']['stats']['diggCount']) 
              + int(dataTik['itemInfo']['itemStruct']['stats']['commentCount'])
              + int(dataTik['itemInfo']['itemStruct']['stats']['shareCount']))
        ERP = (ER / int(dataTik['itemInfo']['itemStruct']['stats']['playCount']))*100
        Like.append(dataTik['itemInfo']['itemStruct']['stats']['diggCount'])
        Comment.append(dataTik['itemInfo']['itemStruct']['stats']['commentCount'])
        Share.append(dataTik['itemInfo']['itemStruct']['stats']['shareCount'])
        Views.append(dataTik['itemInfo']['itemStruct']['stats']['playCount'])
        caption.append(dataTik['itemInfo']['itemStruct']['desc'])
        linkpost.append("https://www.tiktok.com/@cretivox/video/" + vid_id[id])
        erp.append(("%.2f" % ERP))
        cover.append(dataTik['itemInfo']['itemStruct']['video']['dynamicCover'])
        
           
        # print(Like)
    
    ER  = (sum(Like) + sum(Comment) + sum(Share))
    Profile_ER = (ER / Total_followers)*100
    Views_ER = (ER / sum(Views))*100
    showdata.extend((Profile_ER,Views_ER))
    print(showdata)
    

    return render_template('index.html',
                           name = showdata[0],
                           bio = showdata[1],
                           link = showdata[2],
                           pict = showdata[3],
                           follower = (f"{showdata[4]:,}"),
                           post = (f"{showdata[5]:,}"),
                           like = ("%.2f" % showdata[6] ),
                           ER_pro = ("%.2f" % showdata[7]) + "%",
                           ER_view = ("%.2f" % showdata[8]) + "%",
                           
                           #1
                           post_1 = cover[0],
                           caption_1 = caption[0],
                           link_1 = linkpost[0],
                           like_1 = (f"{Like[0]:,}"),
                           comment_1 = (f"{Comment[0]:,}"),
                           view_1 = (f"{Views[0]:,}"),
                           erp_1 = ("%.2f" % float(erp[0])) + "%",
                           
                           #2
                           post_2 = cover[1],
                           caption_2 = caption[1],
                           link_2 = linkpost[1],
                           like_2 = (f"{Like[1]:,}"),
                           comment_2 = (f"{Comment[1]:,}"),
                           view_2 = (f"{Views[1]:,}"),
                           erp_2 = ("%.2f" % float(erp[1])) + "%",
                           
                           #3
                           post_3 = cover[2],
                           caption_3 = caption[2],
                           link_3 = linkpost[2],
                           like_3 = (f"{Like[2]:,}"),
                           comment_3 = (f"{Comment[2]:,}"),
                           view_3 = (f"{Views[2]:,}"),
                           erp_3 = ("%.2f" % float(erp[2])) + "%",
                           
                           #4
                           post_4 = cover[3],
                           caption_4 = caption[3],
                           link_4 = linkpost[3],
                           like_4 = (f"{Like[3]:,}"),
                           comment_4 = (f"{Comment[3]:,}"),
                           view_4 = (f"{Views[3]:,}"),
                           erp_4 = ("%.2f" % float(erp[3])) + "%",
                           
                           #5
                           post_5 = cover[4],
                           caption_5 = caption[4],
                           link_5 = linkpost[4],
                           like_5 = (f"{Like[4]:,}"),
                           comment_5 = (f"{Comment[4]:,}"),
                           view_5 = (f"{Views[4]:,}"),
                           erp_5 = ("%.2f" % float(erp[4])) + "%",
                           
                           #6
                           post_6 = cover[5],
                           caption_6 = caption[5],
                           link_6 = linkpost[5],
                           like_6 = (f"{Like[5]:,}"),
                           comment_6 = (f"{Comment[5]:,}"),
                           view_6 = (f"{Views[5]:,}"),
                           erp_6 = ("%.2f" % float(erp[5])) + "%",
                           
                           #7
                           post_7 = cover[6],
                           caption_7 = caption[6],
                           link_7 = linkpost[6],
                           like_7 = (f"{Like[6]:,}"),
                           comment_7 = (f"{Comment[6]:,}"),
                           view_7 = (f"{Views[6]:,}"),
                           erp_7 = ("%.2f" % float(erp[6])) + "%",
                           
                           #8
                           post_8 = cover[7],
                           caption_8 = caption[7],
                           link_8 = linkpost[7],
                           like_8 = (f"{Like[7]:,}"),
                           comment_8 = (f"{Comment[7]:,}"),
                           view_8 = (f"{Views[7]:,}"),
                           erp_8 = ("%.2f" % float(erp[7])) + "%",
                           
                           #9
                           post_9 = cover[8],
                           caption_9 = caption[8],
                           link_9 = linkpost[8],
                           like_9 = (f"{Like[8]:,}"),
                           comment_9 = (f"{Comment[8]:,}"),
                           view_9 = (f"{Views[8]:,}"),
                           erp_9 = ("%.2f" % float(erp[8])) + "%",
                           
                           #10
                           post_10 = cover[9],
                           caption_10 = caption[9],
                           link_10 = linkpost[9],
                           like_10 = (f"{Like[9]:,}"),
                           comment_10 = (f"{Comment[9]:,}"),
                           view_10 = (f"{Views[9]:,}"),
                           erp_10 = ("%.2f" % float(erp[9])) + "%",
                           
                           #11
                           post_11 = cover[10],
                           caption_11 = caption[10],
                           link_11 = linkpost[10],
                           like_11 = (f"{Like[10]:,}"),
                           comment_11 = (f"{Comment[10]:,}"),
                           view_11 = (f"{Views[10]:,}"),
                           erp_11 = ("%.2f" % float(erp[10])) + "%",
                           
                           #12
                           post_12 = cover[11],
                           caption_12 = caption[11],
                           link_12 = linkpost[11],
                           like_12 = (f"{Like[11]:,}"),
                           comment_12 = (f"{Comment[11]:,}"),
                           view_12 = (f"{Views[11]:,}"),
                           erp_12 = ("%.2f" % float(erp[11])) + "%",
                           
                           #13
                           post_13 = cover[12],
                           caption_13 = caption[12],
                           link_13 = linkpost[12],
                           like_13 = (f"{Like[12]:,}"),
                           comment_13 = (f"{Comment[12]:,}"),
                           view_13 = (f"{Views[12]:,}"),
                           erp_13 = ("%.2f" % float(erp[12])) + "%",
                           
                           #14
                           post_14 = cover[13],
                           caption_14 = caption[13],
                           link_14 = linkpost[13],
                           like_14 = (f"{Like[13]:,}"),
                           comment_14 = (f"{Comment[13]:,}"),
                           view_14 = (f"{Views[13]:,}"),
                           erp_14 = ("%.2f" % float(erp[13])) + "%",
                           
                           #15
                           post_15 = cover[14],
                           caption_15 = caption[14],
                           link_15 = linkpost[14],
                           like_15 = (f"{Like[14]:,}"),
                           comment_15 = (f"{Comment[14]:,}"),
                           view_15 = (f"{Views[14]:,}"),
                           erp_15 = ("%.2f" % float(erp[14])) + "%"
                           
                        )

if __name__ == "__main__":
    app.run(debug=True)
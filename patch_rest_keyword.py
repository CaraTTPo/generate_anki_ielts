import hashlib
from typing import DefaultDict
import urllib
import requests
import csv, json
from pprint import pprint
from lxml import etree
from urllib.parse import urlparse, parse_qs

#  1
#  2
#  3
#  4
#  5
#  6
#  7
#  8
#  9
#  10

filecountlist1 = [
    2,
    3,
    6
]

filecountlist2 = [
    7,
    8,
    9,
    10
]

# 2. 定义和example1和synonyms 
# https://api.dictionaryapi.dev/api/v2/entries/en/strike
# 3. 图片 和 example2
# https://www.youdao.com/w/astronaut/#keyfrom=dict2.top

#issue 样式 名词和分单元



def write_wordlist(filecount):
    countword = 0
    with open('3800_anki_raw_wordlists/3800_anki_wordlist{}.csv'.format(filecount), newline='') as file:

        with open('3800_anki_wordlists/3800_anki_wordlist{}.csv'.format(filecount), 'w', newline='') as write_csvfile:
            writer = csv.DictWriter(write_csvfile, fieldnames=["lid","word","mp3","img","phonetic_en","partOfSpeech","definition","example1","example2","synonyms"])
            writer.writeheader()
            
            #爬虫
            #写文件

            for wordinrow in file:

                word = wordinrow.strip("\n").strip("\r")
                wordinfor = {
                    "lid": int(hashlib.md5(word.encode()).hexdigest()[:10], 16),
                    "word": word,
                    "mp3":'',
                    
                    "img":"", #lid.png
                    "example2":"",

                    "phonetic_en":"",
                    "partOfSpeech":"",
                    "definition":"",
                    "example1":"",
                    "synonyms":"",
                }
                
                try: #测试下
                    wordurl = "https://api.dictionaryapi.dev/api/v2/entries/en/{}".format(word)
                    response = requests.get(wordurl)
                    response_json = response.json()
                    if "No Definitions Found" in response.text:
                        print("{} **** not found in dictionaryapi".format(word))
                    else:
                        response_json = response_json[0]
                        wordinfor['phonetic_en'] = response_json.get('phonetic', "")
                        wordinfor['partOfSpeech'] = response_json['meanings'][0].get('partOfSpeech', "")
                        wordinfor['definition'] = response_json['meanings'][0]['definitions'][0]['definition']
                        wordinfor['example1'] = response_json['meanings'][0]['definitions'][0].get('example', "")
                        wordinfor['synonyms'] = ", ".join(response_json['meanings'][0]['definitions'][0].get('synonyms', [])[0:10])
                except Exception as e:
                    print("***"*10)
                    print('dictionaryapi报错')
                    print(e)
                    print(wordurl)
                    pprint(response_json)
                    print("***"*10)
                


                # 3. 图片 和 example2
                # 图片https://picdict.youdao.com/search?q=advertisement&le=en
                ## 图片
                try:
                    yd_search_url = "https://picdict.youdao.com/search?q={}&le=en".format(word)
                    res = requests.get(yd_search_url)
                    img_res = res.json()
                    url_list = img_res.get('data', {"pic":[]}).get('pic', [])
                    img_url = url_list[0].get("image", "") if url_list else ""
                    if img_url:
                        url = img_url
                        urllib.request.urlretrieve(url, "3800_anki_img/{}".format(wordinfor['lid']))
                        wordinfor["img"] = str(wordinfor['lid'])
                    else:
                        wordinfor["img"] = ""
                except Exception as e:
                    print("***"*10)
                    print("有道图片搜索异常")
                    print(yd_search_url)
                    print(e)
                    print("***"*10)
                
                # https://www.youdao.com/w/abuse/
                ## example2
                try:
                    url = 'https://www.youdao.com/w/{}/'.format(word)
                    res = requests.get(url)
                    html = etree.HTML(res.content)
                    example_raw = html.xpath('//div[@id="authority"]//li')[0].xpath('./p')[0].xpath('.//text()')
                    example_text = ''.join(example_raw)
                    example_text = example_text.rstrip()
                    wordinfor["example2"] = example_text
                except Exception as e:
                    print("***"*10)
                    print("有道找example2报错")
                    print(url)
                    print(e)
                    print("***"*10)

                #写文件
                writer.writerow(wordinfor)
                countword = countword+1
                print("add word: "+str(countword))

# lid,answer,filePath
{
    "lid":203328869, #int(hashlib.md5("advertisment".encode()).hexdigest()[:10], 16)
    "word":"advertisements", #没有list
    "mp3":"203328869.mp3", #可能空测试下 #anki自带
    "img":"203328869.png",#格式jpeg,jpg文件不一定 #搜索
    "phonetic_en":"ədˈvəːtɪzm(ə)nt",
    "partOfSpeech":"noun",
    "definition":"a notice or announcement in a public medium promoting a product, service, or event or publicizing a job vacancy.",
    "example1":"advertisements for alcoholic drinks",
    "example2":"Miss Parrish recently placed an advertisement in the local newspaper.",
    "synonyms": "notice, announcement, bulletin, commercial, promotion, blurb, write-up, display, poster, leaflet"
}


for num in filecountlist2:
    write_wordlist(num)
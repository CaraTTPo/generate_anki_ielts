from typing import DefaultDict
import urllib
import requests
import csv, json
from pprint import pprint
from lxml import etree
from urllib.parse import urlparse, parse_qs


#图片
#名词 72:94+1
#形容词_副词 95:101+1
#吞音_连读 102:128+1
#复数 136:156+1
#缩写 159:161+1
#发音 134:134+1
#语法错觉 162:162+1
#动词 164:165 +1
#专业 163:163+1

#数字和字母 129:131+1
#钱数 157:157+1
#地址 132:133+1
#日期 158:158+1

#section1 334:334+1
#section2 335:335+1
#section3 336:336+1
#section4 337:339+1

kmf_listening_parts_wmf = ["名词", #wmf=with morefeatures means 有定义和example和synonyms和图片
"形容词_副词", 
"吞音_连读", 
"缩写", 
"发音", 
"语法错觉", 
"动词", 
# "数字和字母", 
# "钱数", 
# "地址", 
# "日期", 
"专业", 
"section1", 
"section2", 
"section3", 
"section4"]

kmf_listening_parts_wlf = ["数字和字母",  #wlf = with less features means 没有定义和example和synonyms和图片
"钱数", 
"地址", 
"日期", 
"复数",
]

# 2. 定义和example1和synonyms 
# https://api.dictionaryapi.dev/api/v2/entries/en/strike
# 3. 图片 和 example2
# https://www.youdao.com/w/astronaut/#keyfrom=dict2.top

#issue 样式 名词和分单元
countword = 0
partname = "名词"
with open('kmf_listen_wordlist/kmf_listen_vocab_{}.csv'.format(partname), newline='') as csvfile:

    with open('kmf_listen_anki_wordlist/kmf_listen_vocab_{}.csv'.format(partname), 'w', newline='') as write_csvfile:
        writer = csv.DictWriter(write_csvfile, fieldnames=["lid","word","mp3","img","phonetic_en","partOfSpeech","definition","example1","example2","synonyms"])
        writer.writeheader()
        
        #爬虫
        #写文件

        reader = csv.DictReader(csvfile)
        for wordinrow in reader:
            # if mp3不存在就跳过 否写就可以写
            word = ' '.join(wordinrow['answer']) if isinstance(wordinrow['answer'], list) else wordinrow['answer']
            if 'mp3' not in wordinrow['filePath']:
                print('---'*10)
                print(word+" **** skip for no mp3 in {} part".format(partname))
                print('---'*10)
                continue
            wordinfor = {
                "lid":wordinrow['lid'],
                "word": word,
                "mp3":'{}.mp3'.format(wordinrow['lid']),
                
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
                    print(word+" **** not found in dictionaryapi")
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
                    if "ydschool-online" in img_url:
                        url = img_url
                    elif "ydstatic.com" in img_url:
                        parsed_url = urlparse(img_url)
                        url = parse_qs(parsed_url.query).get("url", img_url)
                        url = url[0] if isinstance(url, list) else url
                    else:
                        url = img_url
                        print("***"*10)
                        print("有道图片链接格式异常")
                        print(img_url)
                        print("***"*10)
                    urllib.request.urlretrieve(url, "kmf_listen_wordsimg/{}".format(wordinfor['lid']))
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
    "lid":203328869,
    "word":"advertisements", #没有list
    "mp3":"203328869.mp3", #可能空测试下
    "img":"203328869.png",#格式jpeg,jpg文件不一定
    "phonetic_en":"ədˈvəːtɪzm(ə)nt",
    "partOfSpeech":"noun",
    "definition":"a notice or announcement in a public medium promoting a product, service, or event or publicizing a job vacancy.",
    "example1":"advertisements for alcoholic drinks",
    "example2":"Miss Parrish recently placed an advertisement in the local newspaper.",
    "synonyms": "notice, announcement, bulletin, commercial, promotion, blurb, write-up, display, poster, leaflet"
}

# 内容 还要通过爬虫更新 要再试下

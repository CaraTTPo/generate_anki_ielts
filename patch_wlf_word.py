import csv

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

countword = 0
partname = "复数"
with open('kmf_listen_wordlist/kmf_listen_vocab_{}.csv'.format(partname), newline='') as csvfile:

    with open('kmf_listen_anki_wordlist/kmf_listen_vocab_{}.csv'.format(partname), 'w', newline='') as write_csvfile:
        writer = csv.DictWriter(write_csvfile, fieldnames=["lid","word","mp3","img","phonetic_en","partOfSpeech","definition","example1","example2","synonyms"])
        writer.writeheader()
        
        #爬虫
        #写文件

        reader = csv.DictReader(csvfile)
        for wordinrow in reader:
            # if mp3不存在就跳过 否写就可以写
            if "[" in wordinrow['answer']:
                word = wordinrow['answer'].replace("', '"," ").strip("['").strip("']").replace(" . ",".").replace(" - ","-")
            else:
                word = wordinrow['answer']
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
            #写文件
            writer.writerow(wordinfor)
            countword = countword+1
            print("add word: "+str(countword))
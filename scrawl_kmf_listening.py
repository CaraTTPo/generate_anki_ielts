import requests
import re,json
import csv


#名词 72:94+1
#形容词_副词 95:101+1
#吞音_连读 102:128+1
#复数 136:156+1
#缩写 159:161+1
#发音 134:134+1
#语法错觉 162:162+1
#动词 164:165 +1
#数字和字母 129:131+1
#钱数 157:157+1
#地址 132:133+1
#日期 158:158+1
#专业 163:163+1
#section1 334:334+1
#section2 335:335+1
#section3 336:336+1
#section4 337:339+1

kmf_listening_parts = (
    ["名词", list(range(72, 94+1))], #[72:95)
    ["形容词_副词", list(range(95, 101+1))],
    ["吞音_连读", list(range(102, 128+1))],
    ["复数", list(range(136, 156+1))],
    ["缩写", list(range(159, 161+1))],
    ["发音", list(range(134, 134+1))],
    ["语法错觉", list(range(162, 162+1))],
    ["动词", list(range(164, 165 +1))],
    ["数字和字母", list(range(129, 131+1))],
    ["钱数", list(range(157, 157+1))],
    ["地址", list(range(132, 133+1))],
    ["日期", list(range(158, 158+1))],
    ["专业", list(range(163, 163+1))],
    ["section1", list(range(334, 334+1))],
    ["section2", list(range(335, 335+1))],
    ["section3", list(range(336, 336+1))],
    ["section4", list(range(337, 339+1))],
)

# https://ielts.kmf.com/vocab/mode?op=trad&type=18 part name
#example part 名词 23个test
#part_test_nums ：1 https://ielts.kmf.com/vocab/pre?id=72
#part_test_nums ：2 https://ielts.kmf.com/vocab/pre?id=73
#part_test_nums ：...
#part_test_nums ：23 https://ielts.kmf.com/vocab/pre?id=94
word_count = 0
for part, part_nums in kmf_listening_parts:

    # 每个part一个列表
    with open('kmf_listen_vocab_{}.csv'.format(part), 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['lid', 'answer', 'filePath'])
        writer.writeheader()

        for part_num in part_nums:
            try:
                url = "https://ielts.kmf.com/vocab/pre?id={}".format(part_num)
                response = requests.get(url)
                wordlist = json.loads(re.findall( 
                    r'var playList = (.*)exam.pr', 
                    response.text,
                    flags=re.DOTALL)[0].strip()[:-1]
                    )
                for wordInfo in wordlist:
                    try:
                        word_count = word_count + 1
                        writer.writerow(wordInfo)
                        mp3_url = wordInfo['filePath']['mp3']
                        doc = requests.get(mp3_url)
                        with open('kmf/{}.mp3'.format(wordInfo['lid']), 'wb') as f:
                            f.write(doc.content)
                    except Exception as ex:
                        print('***'*10)
                        print(wordInfo)
                        print(str(ex))
                        print('***'*10)
            except Exception as ex:
                print('---'*10)
                print(url)
                print(str(ex))
                print('---'*10)

print("word count:{}".format(word_count))






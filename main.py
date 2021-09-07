import genanki
import hashlib, csv

from genanki import package
from os import listdir

def languageCss():
    css = '''.card {
 font-family: Segoe UI;
 font-size: 20px;
 text-align: center;
 color: black;
 background-color: white;
}
.search {
 font-family: Arial;
 font-size: 13px;
 color: blue;
 padding-bottom: 10px;
}
#typeans { font-size:60px !important }
    '''
    return css

def learnWordTemplate():
    question_fmt = '''{{Audio}}
</br>
{{type:Word}}

'''
    answer_fmt = '''{{type:Word}}
</br>
<div style='font-family: Segoe UI; font-size: 40px; color: blue'>{{Word}}</div>
<div style='font-family: Segoe UI; font-size: 25px;'>{{Phonetic symbol}}</div>
</br>
{{Audio}}
</br>

<div class="search">
  <a href="https://www.oxfordlearnersdictionaries.com/definition/english/{{text:Word}}">Oxford词典</a> // 
  <a href="https://www.youdao.com/w/{{text:Word}}">有道词典</a> //  
  <a href="https://www.thefreedictionary.com/{{text:Word}}">The Free Dictionary</a>  //  
  <a href="https://getyarn.io/yarn-find?text={{text:Word}}">Get Yarn</a>  //  
  <a href="https://youglish.com/search/{{text:Word}}/all?">相关视频</a>  //  
  <a href="http://images.google.com/search?tbm=isch&q={{text:Word}}">Image</a>
</div>

<div style='font-family: Segoe UI; font-size: 20px; text-align: left;'>
<a style="background-color: #0D47A1; color: white">noun: </a>
<a style="color: black">{{Definition}}</a>
</div>
</br>
<div style='font-family: Segoe UI; font-size: 25px; text-align: left;'>
<a style="background-color: #0D47A1; color: white">example1: </a>
<a style="color: black">{{Example1}}</a>
</div>
<div style='width: 100%;height: 1em;display: inline-block;background: whitle;'></div>
<div style='font-family: Segoe UI; font-size: 25px; text-align: left;'>
<a style="background-color: #0D47A1; color: white">example2: </a>
<a style="color: black">{{Example2}}</a>
</div>
<div style='width: 100%;height: 1em;display: inline-block;background: whitle;'></div>
<div style='font-family: Segoe UI; font-size: 25px;'>
<a style="background-color: #0D47A1; color: white">synonyms: </a>
<a style="color: blue">{{Synonyms}}</a>
</div>
{{Picture}}
    '''
    template = {
        'name': 'learnWord',
        'qfmt': question_fmt,
        'afmt': answer_fmt,
        }
    return template

def initLanguageModel(model_name):
    my_model = genanki.Model(
    int(hashlib.md5(model_name.encode()).hexdigest()[:10], 16),
    model_name,
    fields=[
        {'name': 'Audio'},
        {'name': 'Phonetic symbol'},
        {'name': 'Word'},
        {'name': 'Picture'},
        {'name': 'PartOfSpeech'},
        {'name': 'Definition'},
        {'name': 'Example1'},
        {'name': 'Example2'},
        {'name': 'Synonyms'},
    ],
    templates=[
        learnWordTemplate(),
    ],
    css=languageCss())
    return my_model

def addNote(my_model, my_deck):
    note_word = {
    "lid":203328869,
    "word":"advertisements", #没有list
    "mp3":"203328869.mp3", #可能空测试下
    "img":"",#格式jpeg,jpg文件不一定
    "phonetic_en":"ədˈvəːtɪzm(ə)nt",
    "partOfSpeech":"noun",
    "definition":"a notice or announcement in a public medium promoting a product, service, or event or publicizing a job vacancy.",
    "example1":"advertisements for alcoholic drinks",
    "example2":"Miss Parrish recently placed an advertisement in the local newspaper.",
    "example3":"The Treviso team was an effective advertisement for the improving state of Italian club rugby.",
    "synonyms": "notice, announcement, bulletin, commercial, promotion, blurb, write-up, display, poster"
}
    note1 = genanki.Note(
        model=my_model,
        fields=[
            '[sound:{}]'.format(note_word['mp3']), 
            "uk [{}]".format(note_word['phonetic_en']),
            note_word['word'],
            '<img src="{}">'.format(note_word['img']) if note_word['img'] else "",
            note_word["partOfSpeech"],
            note_word["definition"],
            note_word["example1"],
            note_word["example2"],
            note_word["synonyms"],
        ]
        )    
    my_deck.add_note(note1)

def addNote2(my_model, my_deck, partname):
    # open file


    with open('kmf_listen_anki_wordlist/kmf_listen_vocab_{}.csv'.format(partname), newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for note_word in reader:
            note = genanki.Note(
                model=my_model,
                fields=[
                    '[sound:{}]'.format(note_word['mp3']), 
                    "uk [{}]".format(note_word['phonetic_en']),
                    note_word['word'],
                    '<img src="{}">'.format(note_word['img']) if note_word['img'] else "",
                    note_word["partOfSpeech"],
                    note_word["definition"],
                    note_word["example1"],
                    note_word["example2"],
                    note_word["synonyms"],
                ]
                )    
            my_deck.add_note(note)

# 每个part是一组
def main():
    print("Hello World!")
    my_model = initLanguageModel('Simple Model')

    parts = [("名词", 1135), #wmf=with morefeatures means 有定义和example和synonyms和图片
        ("吞音_连读", 1333),
        ("形容词_副词",346),  
        ("缩写",127), 
        ("发音",54),
        ("复数",979), 
        ("语法错觉",11), 
        ("动词",109), 
        ("数字和字母",123), 
        ("钱数",15), 
        ("地址",70), 
        ("日期",43), 
        ("专业",44), 
        ("section1",43), 
        ("section2",40), 
        ("section3",45), 
        ("section4",120),
        ]
    
    decks = []

    deck_name = "ielts yasiwang listening vocab" #empty
    my_deck = genanki.Deck(
        int(hashlib.md5(deck_name.encode()).hexdigest()[:10], 16),
        "雅思王听力词汇")
    addNote(my_model, my_deck)
    decks.append(my_deck)


    for part,word_length in parts:
        deck_name = "part_{}_{}".format(part, word_length)
        my_deck2 = genanki.Deck(
            int(hashlib.md5(deck_name.encode()).hexdigest()[:10], 16),
            deck_name)
        addNote2(my_model, my_deck2, part)
        decks.append(my_deck2)


    # To add sounds or images in package
    
    my_package = genanki.Package(decks)
    for filename in listdir("kmf_listen_wordsmp3"):
        my_package.media_files.append("kmf_listen_wordsmp3/{}".format(filename))
    for filename in listdir("kmf_listen_wordsimg"):
        my_package.media_files.append("kmf_listen_wordsimg/{}".format(filename))


  
    my_package.write_to_file('{}.apkg'.format("ielts yasiwang listening vocab"))



if __name__ == "__main__":
    main()
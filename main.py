import genanki
import hashlib

def createCss():
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

.word {
 font-family: Times New Roman;
 font-size: 60px;
 padding-top: 20px;
 padding-bottom: 10px;
 color: green;
}

.ipa {
 font-family: Times New Roman;
 font-size: 20px;
}

.definition {
 text-align: center;
 font-family: Arial;
 font-size: 20px;
 padding-top: 10px;
 padding-bottom: 10px;
}

.sentence {
 font-family: Arial;
 font-size: 20px;
 padding-left: 10px;
 text-align: left;
 border-left: 2.5px solid lightblue;
}

.link {
 font-family: Arial;
 font-size: 15px;
 text-align: right;
}

.block {
 display: inline-block;
 padding-top: 10px;
 padding-bottom: 10px;
 padding-left: 10px;
 padding-right: 10px;
}

.example {
 font-size: 90%;
}

.audio {
 font-size: 150%;
}
    '''

def learnWordTemplate():
    question_fmt = '''<div class="word">{{Word}}</div>
<div class="ipa">{{IPA}}</div>
<div class="audio">{{Audio}}</div>

<div class="search">
  <a href="https://dict.laban.vn/find?type=1&query={{text:Word}}">La bàn</a> //  
  <a href="https://www.thefreedictionary.com/{{text:Word}}">The Free Dictionary</a>  //   
  <a href="http://images.google.com/search?tbm=isch&q={{text:Word}}">Image</a>
</div>'''
    answer_fmt = '''{{FrontSide}}
<div class="definition">{{edit:Definition}}</div>
{{Picture}}
<div class="example">{{edit:Description}}</div>

<div class="block">
  <div class="sentence">{{edit:Sentence}}</div>
</div>
    '''
    learnWord = {
        'name': 'learnWord',
        'qfmt': question_fmt,
        'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
        }

def initSimpleModel(model_name):
    my_model = genanki.Model(
    int(hashlib.md5(model_name.encode()).hexdigest()[:10], 16),
    model_name,
    fields=[
        {'name': 'Question'},
        {'name': 'Answer'},
    ],
    templates=[
        {
        'name': 'learnWord',
        'qfmt': '{{Question}}',
        'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
        },
    ],
    css="")
    return my_model

def createSimpleNotes(my_model):
    my_note1 = genanki.Note(
    model=my_model,
    fields=['note1_Question', 'note1_Answer'])
    my_note2 = genanki.Note(
    model=my_model,
    fields=['note2_Question', 'note2_Answer'])
    return my_note1, my_note2




def main():
    print("Hello World!")
    my_model = initSimpleModel('Simple Model')
    note1, note2 = createSimpleNotes(my_model)
    deck_name = 'DeckExample'
    my_deck = genanki.Deck(
        int(hashlib.md5(deck_name.encode()).hexdigest()[:10], 16),
        deck_name)

    my_deck.add_note(note1)
    my_deck.add_note(note2)

    genanki.Package(my_deck).write_to_file('/Users/wu/Downloads/genanki_tests/{}.apkg'.format(deck_name))



if __name__ == "__main__":
    main()
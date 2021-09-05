import genanki
import hashlib

from genanki import package

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

<div style='font-family: Segoe UI; font-size: 25px; color: green;'>definition: {{Definition}}</div>
</br>
<div style='font-family: Segoe UI; font-size: 25px; color: black;'>example: {{Extra information}}</div>
<hr>
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
        {'name': 'Definition'},
        {'name': 'Extra information'},
    ],
    templates=[
        learnWordTemplate(),
    ],
    css=languageCss())
    return my_model

def addNote(my_model, my_deck):
    note1 = genanki.Note(
        model=my_model,
        fields=[
            '[sound:golf_club_sound.mp3]', 
            "[ɡɒlf klʌb]",
            'golf club',
            '<img src="golf_club_img.jpeg">',
            'A golf club is a social organization which provides a golf course and a building to meet in for its members.',
            "There s a waiting list to join the golf club Entrance to the golf club is by sponsorship only.", 
            ]
        )
    
    my_deck.add_note(note1)




def main():
    print("Hello World!")
    my_model = initLanguageModel('Simple Model')
    deck_name = 'DeckExample'
    my_deck = genanki.Deck(
        int(hashlib.md5(deck_name.encode()).hexdigest()[:10], 16),
        deck_name)
    
    addNote(my_model, my_deck)

    # To add sounds or images in package
    my_package = genanki.Package(my_deck)
    my_package.media_files = ['golf_club_sound.mp3', 
        'golf_club_img.jpeg']


    my_package.write_to_file('{}.apkg'.format(deck_name))



if __name__ == "__main__":
    main()
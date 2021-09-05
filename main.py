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
#typeans { font-size:60px !important }
    '''

def learnWordTemplate():
    question_fmt = '''TYPE WHAT YOU HEAR ------------->  {{Audio}}
</br>
<div style='font-family: Segoe UI; font-size: 25px; color: blue'>{{Phonetic symbol}}</div>
</br>
{{type:Word}}
</br>
<div style='font-family: Segoe UI; font-size: 25px; color: green;'>{{Definition}}</div>
</br>
{{Picture}}'''
    answer_fmt = '''{{type:Word}}
</br>
<div style='font-family: Segoe UI; font-size: 35px; color: blue'>{{Word}}</div>
<div style='font-family: Segoe UI; font-size: 25px;'>{{Phonetic symbol}}</div>
</br>
LISTEN AGAIN ------------->  {{Audio}}
</br></br>
<div style='font-family: Segoe UI; font-size: 25px; color: green;'>{{Definition}}</div>
</br>
<div style='font-family: Segoe UI; font-size: 20px; color: black;'>{{Extra information}}</div>
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
import pymorphy2

morph = pymorphy2.MorphAnalyzer()

def normal_form(word: str):
    p = morph.parse(word)[0]
    return p.normal_form

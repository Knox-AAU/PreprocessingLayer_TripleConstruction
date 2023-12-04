def writeFile(path, content):
    with open(path, "w") as f:
        f.write(content)


from googletrans import Translator
def translateWordToEn(word, language):
    translator = Translator()
    translation = translator.translate(word, src = language)
    #print(language+ ": " + word + ". en: " + translation.text)
    return translation.text

from difflib import SequenceMatcher
#returnerer en konstant mellem 0 og 1. 0 er et elendigt match, 1 er et eksakt match.
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

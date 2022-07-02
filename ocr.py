try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
from nltk import FreqDist
from gtts import gTTS
import pathlib
import os

def ocr_core(file):
    pytesseract.pytesseract.tesseract_cmd = r'D:\Program Files (x86)\Tesseract-OCR\tesseract'
    text = pytesseract.image_to_string(Image.open(file))
    return text

def text_with_space(text):
    lines = text.splitlines()
    return [line for line in lines if line != '' and not line.isspace()]

def lines(text):
    lines = text.splitlines()
    linesWithWords = 0
    for line in lines:
        if line != '' and not line.isspace():
            print(f'line: {line}')
            linesWithWords += 1
    return linesWithWords

def mostCommon(text):
    words = text.split()
    fdist1 = FreqDist(words)
    print(fdist1.most_common())
    highest = 0
    for tuple in fdist1.most_common():
        if tuple[1] > highest:
            highest = tuple[1]
    print(highest)
    return [tuple for tuple in fdist1.most_common() if tuple[1] >= highest/2 and tuple[1] > 1]

def textToSpeech(text, path, filename):
    myObj = gTTS(text=text, lang='en', slow=False)
    filename = filename + '.mp3'
    audio_path = pathlib.Path(path, filename)
    myObj.save(audio_path)
    return audio_path


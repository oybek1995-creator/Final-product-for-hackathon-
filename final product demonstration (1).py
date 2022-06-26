#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# dastur uchun zarur bo'lgan funksiyalar va kutubxonalarni import qilish
import nltk
import string
from heapq import nlargest
import tkinter as tk
from tkinter import filedialog, Text
from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import *
import pyttsx3
import threading
import pytesseract
import cv2
import os

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import heapq
import spacy

from PIL import Image, ImageTk

nlp = spacy.blank("en")

from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation

from heapq import nlargest

from fileinput import filename
import imp
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfile
from tkinter import filedialog
import tkinter as tk
import os
from tkinter import *
import platform
import cv2
import pytesseract
import requests

from tkinter import *
import googletrans
import textblob
from tkinter import ttk, messagebox

# GUI grafik interfeys yaratish


window = Tk()
window.title("Image-Language-Speech Analysis App")
window.geometry("700x400")
window.config(background='black')
style = ttk.Style(window)
style.configure('midtab.TNotebook', tabposition='wn')
window["bg"] = "green"

tab_control = ttk.Notebook(window, style='lefttab.TNotebook')
tab1 = ttk.Frame(tab_control)
tab1_display_text = ScrolledText(tab1, height=5, width=60)
tab1_display_text.grid(row=10, column=0, columnspan=3, padx=12, pady=9)
# displayed_file.grid(row=2, column=0, columnspan=2, padx=12, pady=9)
tab1_display_text.config(state=NORMAL)
tab_control.add(tab1, text=f'{"Multimedia AI tab":^20s}')
label1 = Label(tab1, text='hujjatlar analizi dasturi', padx=9, pady=9)
label1.grid(column=0, row=0)

tab_control.pack(expand=1, fill='both')
nlp.add_pipe('sentencizer')

l1 = Label(tab1, text="Faylni analiz uchun ochish")
l1.grid(row=1, column=1)

displayed_file = ScrolledText(tab1, height=10)
displayed_file.grid(row=2, column=0, columnspan=6, padx=12, pady=9)


# matnni umumiylashtirish funksiyasini tuzish

def text_summarizer(raw_docx):
    raw_text = raw_docx
    docx = nlp(raw_text)
    stopwords = list(STOP_WORDS)

    word_frequencies = {}
    for word in docx:
        if word.text not in stopwords:
            if word.text not in word_frequencies.keys():
                word_frequencies[word.text] = 1
            else:
                word_frequencies[word.text] += 1

    maximum_frequncy = max(word_frequencies.values())

    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word] / maximum_frequncy)

    sentence_list = [sentence for sentence in docx.sents]

    sentence_scores = {}
    for sent in sentence_list:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if len(sent.text.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word.text.lower()]
                    else:
                        sentence_scores[sent] += word_frequencies[word.text.lower()]

    summarized_sentences = nlargest(7, sentence_scores, key=sentence_scores.get)
    final_sentences = [w.text for w in summarized_sentences]
    summary = ' '.join(final_sentences)

    return summary


# natijani o'chirish, faylni yuklash, matnning umumiy variantini olish uchun tegishli funksiyalarni loyihalash
def clear_text_file():
    displayed_file.delete('1.0', END)


def openfiles():
    file1 = tk.filedialog.askopenfilename(filetypes=(("Text Files", ".txt"), ("All files", "*")))
    read_text = open(file1).read()
    displayed_file.insert(tk.END, read_text)

def get_file_summary():
    raw_text = displayed_file.get('1.0', tk.END)
    final_text = text_summarizer(raw_text)
    result ='\nSummary:{}'.format(final_text)
    tab1_display_text.insert(tk.END, result)
    original_text.insert(tk.END, result)
#     text.insert(tk.END, result)
    
def clear_text_result():
    tab1_display_text.delete('1.0', END)


cap = cv2.VideoCapture(0)


def start_capture_thread():
    #t2 = threading.Thread(target=show_frames, args=(label,))
    t2 = threading.Thread(target=show_frames)
    t2.start()
    t2.join()


def show_frames():
    vid = cv2.VideoCapture(0)

    while (True):

        # Capture the video frame
        # by frame
        ret, frame = vid.read()

        # Display the resulting frame
        cv2.imshow('frame', frame)

        # the 'q' button is set as the
        # quitting button you may use any
        # desired button of your choice
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # After the loop release the cap object
    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()
#matnni nutqga utqizish funksiyasini yaratish
speech = pyttsx3.init()

txt = tk.StringVar()

def myspeak():
    speech.say(txt.get())
    speech.runAndWait()
    speech.stop()
    #original_text.insert(tk.END, result)
    
Label(window, text="Gapirish uchun yozish!",fg="Green").pack(pady=10)

frame1 = Frame(window)
Label(frame1, text="type something: ").pack(side=LEFT)
text = Entry(frame1, textvariable=txt)
text.pack()
frame1.pack(pady=10)
# Function Declarations

def universalClear():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


def convertTuple(tup):
    st = ''.join(map(str, tup))
    return st


def uploadFile():

    f_types = [('PNG Files', '*.png')]

    filename = tk.filedialog.askopenfilename(multiple=True, filetypes=f_types)
    filenameStr = convertTuple(filename)
    universalClear()
    image = cv2.imread(filenameStr)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Performing OTSU threshold
    ret, thresh1 = cv2.threshold(
        gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))

    # Applying dilation on the threshold image
    dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)

    # Finding contours
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_NONE)

    # Creating a copy of image
    im2 = image.copy()
    firstFetchText = pytesseract.image_to_string(im2)
    # First Fetch
    print(firstFetchText)
    # Second Fetch

    f = open("Output.txt", 'w+')
    f.write("FIRST FETCH: "+firstFetchText)
    f.close
    # universalClear()
    displayed_file.insert(tk.END, firstFetchText)

# Main
universalClear()

b1 = tk.Button(tab1, text='Rasmdan Matnga Utish',
               width=20, command=lambda: uploadFile())
b1.grid(row=4, column=3, columnspan=8)

universalClear()

# from tkinter import *
# import googletrans
# import textblob
# from tkinter import ttk, messagebox

translated_text = ScrolledText(tab1, height=10, width= 55)
translated_text.grid(row=10, column=9, columnspan=6, padx=12, pady=9)

original_text = ScrolledText(tab1, height=10, width = 55)
original_text.grid(row=2, column=9, pady=9, padx=10)


tab1_display_text = ScrolledText(tab1, height=10, width=100)
def translate_it():
    # Delete Any Previous Translations
    translated_text.delete(1.0, END)

    try:
    # Get Languages From Dictionary Keys
        # Get the From Langauage Key
        for key, value in languages.items():
            if (value == original_combo.get()):
                 from_language_key = key

           # Get the To Language Key
        for key, value in languages.items():
            if (value == translated_combo.get()):
                to_language_key = key

         # Turn Original Text into a TextBlob
        words = textblob.TextBlob(original_text.get(1.0, END))

        # Translate Text
        words = words.translate(from_lang=from_language_key , to=to_language_key)

        # Output translated text to screen
        translated_text.insert(1.0, words)
        text.insert(tk.END, words)
        
    except Exception as e:
           messagebox.showerror("Translator", e)


def clear():
    # Clear the text boxes
    original_text.delete(1.0, END)
    translated_text.delete(1.0, END)

language_list = (1,2,3,4,5,6,7,8,9,0,11,12,13,14,15,16,16,1,1,1,1,1,1,1,1,1,1,1,1,1)
# Grab Language List From GoogleTrans
languages = googletrans.LANGUAGES
# Convert to list
language_list = list(languages.values())
# Text Boxes
#original_text = Text(tab1, height=10, width=40)
#original_text.grid(row=0, column=0, pady=20, padx=10)

translate_button = Button(tab1,text="Translate!", width=20, command=translate_it)
translate_button.grid(row=3, column=2,  columnspan=8, padx=30, pady=30)



# Combo boxes
original_combo = ttk.Combobox(tab1, width=50, value=language_list)
original_combo.current(21)
original_combo.grid(row=1, column=1)

translated_combo = ttk.Combobox(tab1, width=50, value=language_list)
translated_combo.current(36)
translated_combo.grid(row=1, column=2)

# Clear button
clear_button = tk.Button(tab1, text="Clear", width=20, command=clear)
clear_button.grid(row=3, column=8,  columnspan=8, padx=30, pady=30)


# dastur uchun tugmalar yaratish
b0 = Button(tab1, text="Faylni ochish", width=20, command=openfiles, bg='#c5cae9')
b0.grid(row=3, column=0, padx=20, pady=20)

b1 = Button(tab1, text="Qayta ishga tushirish", width=20, command=clear_text_file, bg="#b9f6ca")
b1.grid(row=3, column=1, padx=30, pady=30)

b2 = Button(tab1, text="Matnni umumiylashtirish", width=20, command=get_file_summary, bg='red', fg='#fff')
b2.grid(row=3, column=2, padx=30, pady=30)

b3 = Button(tab1, text="Natijani o'chirish", width=20, command=clear_text_result)
b3.grid(row=4, column=2, padx=30, pady=30)

b4 = Button(tab1, text="kamera olish", width=20, command=start_capture_thread)
b4.grid(row=4, column=0, padx=30, pady=30)

b5 = Button(tab1, text="Matndan nutqga o'tish", width=20,command=myspeak)
b5.grid(row=4, column=1, padx=30, pady=30)


tab1_display_text.grid(row=10, column=0, columnspan=3,padx=12, pady=5)
# displayed_file.grid(row=2, column=0, columnspan=2, padx=12, pady=9)
tab1_display_text.config(state=NORMAL)

window.mainloop()


# In[ ]:





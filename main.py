import speech_recognition as sr
import matplotlib.pyplot as plt
from easygui import *
from PIL import Image, ImageTk
import tkinter as tk
from itertools import count
import os
import string
from matplotlib.animation import FuncAnimation


class ImageLabel(tk.Label):
    """this label displays images and plays them in a slideshow like gifs"""

    def load(self, im, letter):
        if isinstance(im, str):
            im = Image.open(im)

        self.loc = 0
        self.frames = []

        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass

        try:
            self.delay = im.info["duration"]
        except:
            self.delay = 100

        if len(self.frames) == 1:
            self.config(image=self.frames[0], text=letter)
        else:
            self.next_frame()

    def unload(self):
        self.config(image=None)
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.loc += 1
            self.loc %= len(self.frames)
            self.config(image=self.frames[self.loc])
            self.after(self.delay, self.next_frame)


def convertToIsl():
    r = sr.Recognizer()
    isl_gif = [
        "enjoy",
        "father",
        "mother",
        "hi",
        "happy",
        "sad",
        "good morning",
        "good night",
        "man",
        "woman",
        "you're welcome",
    ]
    arr = list(string.ascii_lowercase)

    with sr.Microphone() as source:
        image = "customsignlanguage.jpg"
        msg = "HEARING/SPEAKING IMPAIRMENT ASSISTANT"
        choices = ["Indian Sign Language", "Exit"]
        reply = buttonbox(msg, image=image, choices=choices)
        r.adjust_for_ambient_noise(source)

        while True:
            print("Please speak")
            audio = r.listen(source)

            try:
                a = r.recognize_google(audio)
                a = a.lower()
                print("Repeating your word(s): " + a.lower())

                for c in string.punctuation:
                    a = a.replace(c, "")

                if a.lower() == "exit":
                    print("Exit")
                    break

                elif a.lower() in isl_gif:
                    root = tk.Tk()
                    lbl = ImageLabel(root)
                    lbl.pack()
                    lbl.load(r"ISL_Gifs/{0}.gif".format(a.lower()), a)
                    root.mainloop()

                else:
                    for i in range(len(a)):
                        if a[i] in arr:
                            ImageAddress = "isl_letters/" + a[i] + ".jpeg"
                            ImageItself = Image.open(ImageAddress)
                            ImageNumpyFormat = plt.imread(ImageAddress)
                            plt.imshow(ImageNumpyFormat)
                            plt.title(a[i])
                            plt.draw()
                            plt.pause(0.8)
                        else:
                            continue

            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print(
                    f"Could not request results from Google Speech Recognition service; {e}"
                )

            plt.close()


def convertToAsl():
    r = sr.Recognizer()
    arr = list(string.ascii_lowercase)

    with sr.Microphone() as source:
        image = "customsignlanguage.jpg"
        msg = "HEARING/SPEAKING IMPAIRMENT ASSISTANT"
        choices = ["American Sign Language", "Exit"]
        reply = buttonbox(msg, image=image, choices=choices)
        r.adjust_for_ambient_noise(source)

        while True:
            print("Please speak")
            audio = r.listen(source)

            try:
                a = r.recognize_google(audio)
                a = a.lower()
                print("Repeating your word(s): " + a.lower())

                for c in string.punctuation:
                    a = a.replace(c, "")

                if a.lower() == "exit":
                    print("Exit")
                    break

                for i in range(len(a)):
                    if a[i] in arr:
                        ImageAddress = "asl_letters/" + a[i] + ".jpg"
                        ImageItself = Image.open(ImageAddress)
                        ImageNumpyFormat = plt.imread(ImageAddress)
                        plt.imshow(ImageNumpyFormat)
                        plt.title(a[i])
                        plt.draw()
                        plt.pause(0.8)
                    else:
                        continue

            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print(
                    f"Could not request results from Google Speech Recognition service; {e}"
                )

            plt.close()


while 1:
    image = "customsignlanguage.jpg"
    msg = "SPEECH TO SIGN LANGUAGE CONVERSION"
    choices = ["Indian Sign Language", "American SIgn Language"]
    reply = buttonbox(msg, image=image, choices=choices)
    if reply == choices[0]:
        convertToIsl()
    if reply == choices[1]:
        convertToAsl()

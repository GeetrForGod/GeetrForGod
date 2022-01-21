import playsound  # to play saved mp3 file
from gtts import gTTS  # google text to speech
import os
import wolframalpha  # to calculate strings into formula
import webbrowser
import urllib.request
import re
from pynput.keyboard import Controller, Key
from selenium import webdriver
import os.path
import time
import speech_recognition as sr
import pyjokes

WAKE = "hey Anna"

music_playing = False

assistant_sleep = True

num = 1


def assistant_speaks(output):
    global num

    # num to rename every audio file
    # with different name to remove ambiguity
    num += 1
    print("Anna : ", output)

    toSpeak = gTTS(text=output, lang='en', slow=False)
    # saving the audio file given by google text to speech
    file = str(num) + ".mp3"
    toSpeak.save(file)

    # play sound package is used to play the same file.
    playsound.playsound(file, True)
    os.remove(file)


def get_audio2():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration= 1)
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")

        except Exception as e:
            global music_playing
            if music_playing is False:
                assistant_speaks("Say that again please...")
            return "None"
    return query


def process_text(input):
    global music_playing
    try:
        if 'search' in input:
            # a basic web crawler using selenium
            search_web(input)
            return

        elif "who are you" in input or "define yourself" in input:
            speak = '''Hello, I am Anna. Your personal Assistant.
			I am here to make your life easier. You can command me to perform
			tasks like opening youtube or searching google'''
            assistant_speaks(speak)
            return

        elif "music" in input:
            music_control(input)
            return

        elif "volume" in input:
            volume_control(input)

        elif "mute" in input:
            mute(input)

        elif "joke" in input or "laugh" in input:
            assistant_speaks(pyjokes.get_joke())

        elif "sleep" in input:
            global assistant_sleep
            assistant_speaks("Bye for now")
            assistant_sleep = True
            return

        elif "who made you" in input or "created you" in input:
            speak = "I have been created by Braden Fehr."
            assistant_speaks(speak)
            return

        elif "calculate" in input.lower():

            # write your wolframalpha app_id here
            app_id = "WOLFRAMALPHA_APP_ID"
            client = wolframalpha.Client(app_id)

            index = input.lower().split().index('calculate')
            query = input.split()[index + 1:]
            res = client.query(' '.join(query))
            answer = next(res.results).text
            assistant_speaks("The answer is " + answer)
            return

        else:
            if music_playing is False:
                assistant_speaks("I can search the web for you, Do you want to continue?")
                ans = get_audio2()
            else:
                ans = 'no'
                return
            if 'yes' in str(ans) or 'yeah' in str(ans):
                webbrowser.open("https://www.google.com/search?q=")

            else:
                return
    except:
        if music_playing is False:
            assistant_speaks("I don't understand, I can search the web for you, Do you want to continue?")
            ans = get_audio2()
            if 'yes' in str(ans) or 'yeah' in str(ans):
                query = input.split()[index + 1:]
                webbrowser.open("https://www.google.com/")

            elif 'no' in str(ans):
                return


def search_web(input):
    global music_playing
    driver = webdriver.Firefox()
    driver.implicitly_wait(1)
    driver.maximize_window()

    if 'youtube' in input.lower() and music_playing is False:
        assistant_speaks("Opening in youtube")
        index = input.lower().split().index('youtube')
        query = input.split()[index + 1:]
        html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + '+'.join(query))
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        webbrowser.open("https://www.youtube.com/watch?v=" + video_ids[0])
        # keyboard = Controller()
        key = "k"
        time.sleep(5)
        # keyboard.press(key)
        # keyboard.release(key)
        # k needs to be pressed when using firefox
        music_playing = True
        return

    elif 'youtube' in input.lower() and music_playing is True:
        os.system("pkill brave")
        os.system("pkill firefox")
        assistant_speaks("Opening in youtube")
        index = input.lower().split().index('youtube')
        query = input.split()[index + 1:]
        html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + '+'.join(query))
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        webbrowser.open("https://www.youtube.com/watch?v=" + video_ids[0])

        #keyboard = Controller()
        #print("hello world")
        #keyboard.press(Key.Alt)
        #print("hello world")
        #keyboard.press(Key.Tab)
        #print("hello world")
        #keyboard.release(Key.Alt)
        #print("hello world")
        #keyboard.release(Key.Tab)
        #print("hello world")
        # time.sleep(5)
        # keyboard.press(key)
        # keyboard.release(key)
        # k needs to be pressed when using firefox
        music_playing = True
        return



    elif 'wikipedia' in input.lower():

        assistant_speaks("Opening Wikipedia")
        index = input.lower().split().index('wikipedia')
        query = input.split()[index + 1:]
        driver.get("https://en.wikipedia.org/wiki/" + '_'.join(query))
        return

    else:

        if 'google' in input:

            index = input.lower().split().index('google')
            query = input.split()[index + 1:]
            webbrowser.open("https://www.google.com/search?q=" + '+'.join(query))

        elif 'search' in input:

            index = input.lower().split().index('google')
            query = input.split()[index + 1:]
            webbrowser.open("https://www.google.com/search?q =" + '+'.join(query))

        else:

            webbrowser.open("https://www.google.com/search?q=" + '+'.join(input.split()))

        return


def mute(input):
    keyboard = Controller()
    keyboard.press(Key.f10)
    keyboard.release(Key.f10)


def volume_control(input):
    if "down" in input.lower():
        keyboard = Controller()
        keyboard.press(Key.f11)
        keyboard.release(Key.f11)
        keyboard.press(Key.f11)
        keyboard.release(Key.f11)
        keyboard.press(Key.f11)
        keyboard.release(Key.f11)

    elif "up" in input.lower():
        keyboard = Controller()
        keyboard.press(Key.f12)
        keyboard.release(Key.f12)
        keyboard.press(Key.f12)
        keyboard.release(Key.f12)
        keyboard.press(Key.f12)
        keyboard.release(Key.f12)
        print("up")

    elif "max" in input.lower():
        keyboard = Controller()
        keyboard.press(Key.f12)
        keyboard.release(Key.f12)
        keyboard.press(Key.f12)
        keyboard.release(Key.f12)
        keyboard.press(Key.f12)
        keyboard.release(Key.f12)
        keyboard.press(Key.f12)
        keyboard.release(Key.f12)
        keyboard.press(Key.f12)
        keyboard.release(Key.f12)
        keyboard.press(Key.f12)
        keyboard.release(Key.f12)
        keyboard.press(Key.f12)
        keyboard.release(Key.f12)
        keyboard.press(Key.f12)
        keyboard.release(Key.f12)
        keyboard.press(Key.f12)
        keyboard.release(Key.f12)
        keyboard = Controller()
        keyboard.press(Key.f12)
        keyboard.release(Key.f12)
        keyboard.press(Key.f12)
        keyboard.release(Key.f12)
        keyboard.press(Key.f12)
        keyboard.release(Key.f12)
        keyboard.press(Key.f12)
        keyboard.release(Key.f12)
        keyboard.press(Key.f12)
        keyboard.release(Key.f12)
        keyboard.press(Key.f12)
        keyboard.release(Key.f12)
        keyboard.press(Key.f12)
        keyboard.release(Key.f12)
        keyboard.press(Key.f12)
        keyboard.release(Key.f12)
        keyboard.press(Key.f12)
        keyboard.release(Key.f12)

    else:
        assistant_speaks("please say volume up or volume down to control audio")


def music_control(input):
    global music_playing
    if "play" in input.lower():
        keyboard = Controller()
        key = "k"
        keyboard.press(key)
        keyboard.release(key)
        music_playing = True

    elif "pause" in input.lower():
        keyboard = Controller()
        key = "k"
        keyboard.press(key)
        keyboard.release(key)
        music_playing = False

    elif "stop" in input or "close" in input.lower():
        keyboard = Controller()
        keyboard.press(Key.ctrl)
        keyboard.press("w")
        keyboard.release(Key.ctrl)
        keyboard.release("w")
        os.system("pkill brave")
        os.system("pkill firefox")

    elif "skip" in input or "next" in input.lower():
        keyboard = Controller()
        keyboard.press(Key.shift)
        keyboard.press("n")
        keyboard.release(Key.shift)
        keyboard.release("n")

    else:
        assistant_speaks("please say play music or pause music to control music")


# Driver Code
if __name__ == "__main__":

    while 1:
        text = get_audio2()
        if text.count(WAKE) > 0:
            assistant_speaks("Hello what can i do for you?")
            time.sleep(1)
            assistant_sleep = False
            text = get_audio2()

        elif assistant_sleep is False:
            text

        else:
            continue

        if text == 0:
            continue

        if "exit" in str(text) or "bye" in str(text) in str(text):
            assistant_speaks("Ok bye, " + "Braden" + '.')
            break

        # calling process text to process the query
        process_text(text)

import speech_recognition as sr
import pyttsx3 as ptx
import wikipedia as wk
import pywhatkit as pwk
import datetime
import openai as op

r = sr.Recognizer()
phone_numbers={"abhi":"8884718828","alex":"1234567890","bob":"6382391863816"}
def speak(command):
    engine = ptx.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice',voices[1].id)
    engine.setProperty('rate',180)
    engine.say(command)
    engine.runAndWait()
def commands():
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            print('You may ask your question')
            audioin = r.listen(source)
            my_text = r.recognize_google(audioin)
            my_text = my_text.lower()
            print(my_text)
            #ask to play song
            if 'play' in my_text:
                my_text = my_text.replace('play','')
                speak('playing'+my_text)
                pwk.playonyt(my_text)
            #speak(my_text)
            elif 'time' in my_text:
                timenow = datetime.datetime.now().strftime('%H:%M')
                speak(timenow)
            #ask anything about person
            elif 'information ' in my_text:
                person = my_text.replace('information','')
                info = wk.summary(person,5)
                print(info)
                speak(info)
            #phone number
            elif 'contact details' in my_text:
                names = list(phone_numbers)
                for name in names:
                    if name in my_text:
                        speak(name + "Mobile number is " + phone_numbers[name])
            else:
                speak("sorry,your command not recognized")
                print("sorry,your command not recognized")
    except:
        print("ERROR CAPTURING VOICE...")

commands()

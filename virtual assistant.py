import speech_recognition as sr
import pyttsx3
import datetime as dt
import pywhatkit as pk
import wikipedia as wiki
listener = sr.Recognizer()
speaker = pyttsx3.init()
rate = speaker.getProperty('rate')
speaker.setProperty('rate',145)
def speak(text):
    speaker.say( text)
    speaker.runAndWait()
va_name = 'charlie'
speak('i am your' + va_name +' tell me sudheer')
def take_command():
    command = ''
    try:
        with sr.Microphone() as source:
            print('listening....')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if va_name in command:
                command = command.replace(va_name+'','')
                #print(command)
                #speak(command)


    except:
        print('check your mic')
    return command
while True:
    va_command = take_command()
    if 'see you later' in va_command:
        print('see you again sudheer. i will be there whenever you call me love you bye')
        speak('see you again sudheer. i will be there whenever you call me love you bye')
        break
    elif 'time' in va_command:
        cur_time = dt.datetime.now().strftime('%I:%M %p')
        print(cur_time)
        speak(cur_time)
    elif'play' in va_command:
        va_command = va_command.replace('play', '')
        print('playing...' + va_command)
        speak('playing...' + va_command + 'enjoy sudheer')
        pk.playonyt(va_command)
    elif'search for' in va_command or'google' in va_command:
        va_command = va_command.replace('search for', '')
        va_command = va_command.replace('google', '')
        speak('searching for' +va_command)
        pk.search(va_command)
    elif 'who is ' in va_command:
        va_command = va_command.replace('who is','')
        info = wiki.summary(va_command,2)
        print(info)
        speak(info)
    elif'love you' in va_command:
        speak('love you too sudheer that no one can love you more than me')
    elif'who are you' in va_command:
        speak('i am sudheer assistant')
    elif'hate you' in va_command:
        speak('but i always love you sudheer')
    elif'question' in va_command:
        speak('yes sudheer')
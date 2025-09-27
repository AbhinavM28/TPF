import speech_recognition as sr
from googletrans import Translator

def speech_to_text():
    r = sr.Recognizer()
    with sr.Microphone(device_index=2) as source:
        print("Please wait 1 second...")
        r.adjust_for_ambient_noise(source, duration=1.5)
        r.dynamic_energy_threshold = True
        print("Speak Now!")
        audio = r.listen(source)

    translator = Translator()
    try:
        text_te = r.recognize_google(audio, language="te-IN")
        text_en = translator.translate(text_te, src='te')
        translated_text = text_en.text
        print(translated_text)  # Print the translated text to stdout
        return translated_text  # Return the translated text
    except sr.UnknownValueError:
        print("Could not understand input")
        return None
    except sr.RequestError as e:
        print("Could not request results from Google; {0}".format(e))
        return None

if __name__ == "__main__":
    translated_text = speech_to_text()
    if translated_text is not None:
        with open("output_text.txt", "w") as file:
            file.write(translated_text)

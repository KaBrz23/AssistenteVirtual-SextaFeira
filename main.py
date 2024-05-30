import speech_recognition as sr
from gtts import gTTS
import os
from datetime import datetime
import random
import requests
from playsound import playsound # ou usar o mixer

recognizer = sr.Recognizer()

# Função de fala
def falar(text):
    tts = gTTS(text=text, lang='pt-br')
    filename = "voice.mp3"
    tts.save(filename)
    playsound(filename)
    os.remove(filename)

# Função para ouvir comando de voz
def escutar():
    with sr.Microphone() as source:
        print("Escutando...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio, language='pt')
            print(f"Você disse: {command}")
            return command.lower()
        except sr.UnknownValueError:
            print("Desculpe, não entendi o que você disse.")
            return ""
        except sr.RequestError:
            print("Erro ao conectar com o serviço de reconhecimento de voz.")
            return ""

# Função para cadastrar evento na agenda
def cadastrar_evento():
    falar("Ok, qual evento devo cadastrar?")
    event = escutar()
    with open("agenda.txt", "a") as file:
        file.write(event + "\n")
    falar("Evento cadastrado com sucesso.")

# Função para ler a agenda
def ler_agenda():
    if os.path.exists("agenda.txt"):
        with open("agenda.txt", "r") as file:
            events = file.readlines()
            for event in events:
                falar(event.strip())
    else:
        falar("A agenda está vazia.")

# Função para abrir o navegador
def abrir_navegador():
    falar("Abrindo o Google Chrome.")
    os.system("google-chrome") # este comando é para linux

# Função para informar as horas
def informar_horas():
    agora = datetime.now()
    hora = agora.hour
    minuto = agora.minute
    falar(f"Agora são {hora} horas e {minuto} minutos")

# Função para obter a cotação do dólar
def dolar():
    try:
        requisicao = requests.get('https://economia.awesomeapi.com.br/all/USD-BRL')
        cot = requisicao.json()
        dolar_bid = cot['USD']['bid']
        dolar_replace = dolar_bid.replace('.', ',')
        return f"O dólar está {dolar_replace} Reais"
    except:
        return "Não consegui obter a cotação do dólar."

# Função para contar piada
def contar_piada():
    piadas = [
        'Você conhece a piada do fotógrafo? Ainda não foi revelada!',
        'Por que o livro de matemática está sempre triste? Porque ele tem muitos problemas.',
        'O que o pato disse para a pata? Vem quá!',
        'Por que o peixe vive no mar? Porque na terra o peixe morre.'
    ]
    piada = random.choice(piadas)
    return piada

# Função para obter informações climáticas atuais
def clima_atual():

    API_KEY = "fe44a83a029a7d2130cfa9ead7f206b4"
    cidade = "São Paulo"
    link = f"https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={API_KEY}&lang=pt_br"

    try:
        requisicao = requests.get(link)
        requisicao_dic = requisicao.json()
        descricao = requisicao_dic['weather'][0]['description']
        temperatura = requisicao_dic['main']['temp'] - 273.15
        temperatura_arredondada = round(temperatura)
        return f"{descricao} com temperatura de {temperatura_arredondada} graus."
    except:
        return "Não consegui obter as informações climáticas."

# Função para desligar o computador
def desligar_computador():
    falar("Desligando o computador.")
    os.system("shutdown now") # este comando é para linux

# Função principal
def main():
    while True:
        command = escutar()
        if "ok sexta-feira" in command:
            falar("Sim, mestre. O que posso fazer?")
            command = escutar()

            if "cadastrar evento na agenda" in command:
                cadastrar_evento()
            elif "ler agenda" in command:
                ler_agenda()
            elif "abrir navegador" in command:
                abrir_navegador()
            elif "que horas são" in command:
                informar_horas()
            elif "quanto está o dólar hoje" in command:
                dollar_rate = dolar()
                falar(dollar_rate)
            elif "contar uma piada" in command:
                piada = contar_piada()
                falar(piada)
            elif "clima atual" in command:
                weather_info = clima_atual()
                falar(weather_info)
            elif "desligar o computador" in command:
                desligar_computador()

if __name__ == "__main__":
    main()

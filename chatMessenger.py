#./ngrok http 8080

import os, sys
from flask import Flask, request
from pymessenger import Bot

app = Flask(__name__)

PAGE_ACCESS_TOKEN = "EAAd1aXC5EpsBAC9GcLZBlAZClLeZCUUd9U6RsNE3z8iy67fq9TWQls6HB1TCvm34cfngjPVXK4koIGlVFEmpM4uCO9SdgdeIjovOli9zOZC9qYK5iAHNOcck4chdMBdqxE0v18xKTSZBDzxwFTvOGGaure7WqZBpSdAtiJQqMi1YX7uZCN24gkD"

bot = Bot(PAGE_ACCESS_TOKEN)

@app.route('/', methods=['GET'])
def verify():
	#Verificacion WebHook
	# cuando el endpoint este registrado como webhook, debe mandar de vuelta
    # el valor de 'hub.challenge' que recibe en los argumentos de la llamada
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "hello":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    #log(data) 

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # alguien envia un mensaje

                    sender_id = messaging_event["sender"]["id"]        # el facebook ID de la persona enviando el mensaje
                    recipient_id = messaging_event["recipient"]["id"]  # el facebook ID de la pagina que recibe (tu pagina)

                    if messaging_event.get('message'):
                    	if 'text' in messaging_event['message']:
                    		message_text = messaging_event["message"]["text"]  # el texto del mensaje
                    	else:
                    		message_text = "Sin Texto"

                    #Respuesta
                    response = message_text
                    bot.send_text_message(sender_id, response)

                    



    return "ok", 200


def log(message): 
    print(message)
    sys.stdout.flush()

if __name__ == '__main__':
    app.run(debug=True, port = 8080)
    #app.run(debug=True)
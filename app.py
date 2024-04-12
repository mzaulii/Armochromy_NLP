from flask import Flask, request, jsonify

app = Flask(__name__)

# Inizializzo i contatori per le risposte A e B
count_sottotono_A = 0
count_sottotono_B = 0
count_contrasto_A = 0
count_contrasto_B = 0
sottotono = ""
contrasto = ""

@app.route('/', methods=['GET', 'POST'])
def home():
    global count_sottotono_A, count_sottotono_B, count_contrasto_A, count_contrasto_B
    count_sottotono_A = 0
    count_sottotono_B = 0
    count_contrasto_A = 0
    count_contrasto_B = 0
    return 'OK', 200


# Funzione per determinare il sottotono della pelle in base alle risposte A e B
def determina_sottotono(data):
    global count_sottotono_A, count_sottotono_B
    if 'sessionInfo' in data and 'parameters' in data['sessionInfo']:
        parameters = data['sessionInfo']['parameters']
        for i in range(1, 6):  # Itero su tutte le domande del flusso sottotono
            param_name = f"sottotono_risposta_{i}"
            if param_name in parameters:
                value = parameters[param_name].strip().lower()
                if value == 'a' or value == 'risposta a':
                    count_sottotono_A += 1
                elif value == 'b' or value == 'risposta b':
                    count_sottotono_B += 1

    if count_sottotono_A > count_sottotono_B:
        return "caldo"
    elif count_sottotono_B > count_sottotono_A:
        return "freddo"
    else:
        return "non è possibile determinare"

# Funzione per determinare il contrasto in base alle risposte A e B
def determina_contrasto(data):
    global count_contrasto_A, count_contrasto_B
    if 'sessionInfo' in data and 'parameters' in data['sessionInfo']:
        parameters = data['sessionInfo']['parameters']
        for i in range(6, 9):  # Itero su tutte le domande del flusso contrasto
            param_name = f"contrasto_risposta_{i}"
            if param_name in parameters:
                value = parameters[param_name].strip().lower()
                if value == 'a' or value == 'risposta a':
                    count_contrasto_A += 1
                elif value == 'b' or value == 'risposta b':
                    count_contrasto_B += 1

    if count_contrasto_A > count_contrasto_B:
        return "basso"
    elif count_contrasto_B > count_contrasto_A:
        return "medio/intenso"
    else:
        return "non è possibile determinare"

# Funzione per determinare la stagione cromatica in base al sottotono e al contrasto
def determina_stagione(sottotono, contrasto):
    if sottotono == "caldo":
        if contrasto == "basso":
            return "Primavera"
        else:
            return "Autunno"
    else:
        if contrasto == "basso":
            return "Estate"
        else:
            return "Inverno"

# endpoint per gestire le richieste di dialogflow
@app.route('/dialogflow', methods=['POST'])
def dialogflow():
    global count_sottotono_A, count_sottotono_B, sottotono
    global count_contrasto_A, count_contrasto_B, contrasto

    data = request.get_json()  # get data from dialogflow
    
    # Stampare i valori dei parametri sul terminale
    for i in range(1, 6):
        param_name = f"sottotono_risposta_{i}"
        print(f"{param_name}: {data['sessionInfo']['parameters'].get(param_name, 'Non disponibile')}")
    for i in range(6, 9):
        param_name = f"contrasto_risposta_{i}"
        print(f"{param_name}: {data['sessionInfo']['parameters'].get(param_name, 'Non disponibile')}")

    # Determino il sottotono della pelle solo se non è già stato determinato
    if not sottotono:
        sottotono = determina_sottotono(data)

    # Se il sottotono è stato determinato e il contrasto non è ancora stato determinato, chiedo la domanda sul contrasto
    if sottotono and not contrasto and all(data['sessionInfo']['parameters'].get(f'contrasto_risposta_{i}', '') == '' for i in range(6, 9)):
        return jsonify({
        "fulfillmentResponse": {
            "messages": [
                {
                    "text": {
                        "text": [f"Il sottotono della tua pelle è {sottotono}. \n"
                                 + "Ora scopriamo se il tuo contrasto è alto o basso! \n\n"
                                 + "6. Di che colore sono i tuoi occhi? \n\n"
                                 + "A) Nocciola o marrone \n"
                                 + "B) Blu, verdi o grigi \n"]
                    }
                }
            ]
        }
    })

    # Se il contrasto non è ancora stato determinato, lo determino
    if sottotono and not contrasto:
        contrasto = determina_contrasto(data)

    # Se sia il sottotono che il contrasto sono stati determinati, determino la stagione cromatica
    if sottotono and contrasto:
        stagione = determina_stagione(sottotono, contrasto)
        return jsonify({
            "fulfillmentResponse": {
                "messages": [
                    {
                        "text": {
                            "text": [f"Prima abbiamo visto che il sottotono della tua pelle è {sottotono}. \n\n"
                                     + f"Ora abbiamo stabilito che il tuo contrasto è {contrasto}. \n"
                                     + f"Quindi, la tua stagione cromatica è {stagione}."]
                        }
                    }
                ]
            }
        })

    # Se non siamo ancora all'ultima domanda, restituiamo una risposta vuota
    return jsonify({})


# avvio del server
if __name__ == '__main__':
    app.run(debug=True, port=8080)



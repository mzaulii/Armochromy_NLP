from flask import Flask, request, jsonify

app = Flask(__name__)

# Inizializzo i contatori per le risposte A e B
count_sottotono_A = 0
count_sottotono_B = 0
count_intensità_A = 0
count_intensità_B = 0
sottotono = ""
intensità = ""
stagione = ""

@app.route('/', methods=['GET', 'POST'])
def home():
    global count_sottotono_A, count_sottotono_B, count_intensità_A, count_intensità_B, sottotono, intensità, stagione
    count_sottotono_A = 0
    count_sottotono_B = 0
    count_intensità_A = 0
    count_intensità_B = 0
    sottotono = ""
    intensità = ""
    stagione = ""
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
        return "CALDO🔥"
    elif count_sottotono_B > count_sottotono_A:
        return "FREDDO🥶"
    else:
        return "non è possibile determinare"

# Funzione per determinare il intensità in base alle risposte A e B
def determina_intensità(data):
    global count_intensità_A, count_intensità_B
    if 'sessionInfo' in data and 'parameters' in data['sessionInfo']:
        parameters = data['sessionInfo']['parameters']
        # Controlla che tutte e tre le risposte sul intensità siano state fornite dall'utente
        if all(param_value.strip().lower() in ['a', 'b'] for param_value in [parameters.get(f"intensita_risposta_{i}", "") for i in range(6, 9)]):
            for i in range(6, 9):  # Itero su tutte le domande del flusso intensità
                param_name = f"intensita_risposta_{i}"
                value = parameters[param_name].strip().lower()
                if value == 'a' or value == 'risposta a':
                    count_intensità_A += 1
                elif value == 'b' or value == 'risposta b':
                    count_intensità_B += 1

            if count_intensità_A > count_intensità_B:
                return "BASSA⬇️"
            elif count_intensità_B > count_intensità_A:
                return "ALTA⬆️"
            else:
                return "non è possibile determinare"

    # Se una o più risposte sul intensità non sono state fornite, restituisci un valore vuoto e azzerale
    count_intensità_A = 0
    count_intensità_B = 0
    return ""

# Funzione per determinare la stagione cromatica in base al sottotono e all'intensità
def determina_stagione(sottotono, intensità):
    if sottotono == "CALDO🔥":
        if intensità == "BASSA⬇️":
            return "AUTUNNO🍁"
        else:
            return "PRIMAVERA🌸"
    else:
        if intensità == "BASSA⬇️":
            return "ESTATE☀️"
        else:
            return "INVERNO❄️"

# Funzione per generare la risposta sulla palette dei colori in base alla stagione cromatica
def genera_risposta_palette(stagione):
    if stagione == "PRIMAVERA🌸":
        palette = "La tua stagione è PRIMAVERA🌸 e questi sono i colori che ti valorizzano e quelli nemici:\n\n" \
                  "🌈 Colori chiari, neutro-caldi e vivaci:\n" \
                  "• Rosa pesca o corallo\n" \
                  "• Giallo chiaro\n" \
                  "• Verde acqua, menta, mela o prato\n" \
                  "• Turchese\n" \
                  "• Beige dorato\n" \
                  "🌈 Colori jolly: Bianco panna e cammello\n"\
                  "🌈 Colori nemici: Freddi e polverosi\n\n"
    elif stagione == "ESTATE☀️":
        palette = "La tua stagione è ESTATE☀️ e questi sono i colori che ti valorizzano e quelli nemici:\n\n" \
                  "🌈 Colori nuance delicate e fredde, non troppo intensi:\n"\
                  "• Sfumature pastello come il malva, salvia, lilla\n"\
                  "• Grigi\n"\
                  "• Tortora\n"\
                  "• Blu ma non brillante\n"\
                  "🌈 Colori nemici sono quelli più vibranti, come i fluo, ma anche quelli a base aranciata. \n\n"

    elif stagione == "AUTUNNO🍁":
        palette = "La tua stagione è AUTUNNO🍁 e questi sono i colori che ti valorizzano e quelli nemici:\n\n" \
                  "🌈 Colori con tonalità calde e profonde:\n"\
                  "• Rossi caldi\n"\
                  "• Sfumature del marrone (cuoio, nocciola, terra bruciata)\n"\
                  "• Giallo senape \n"\
                  "• Arancione\n"\
                  "• Sfumature del verde (perfetto quello oliva) \n"\
                  "🌈 Colori nemici: Freddi e cupi, il nero è prevalente\n\n"
    elif stagione == "INVERNO❄️":
        palette = "La tua stagione è INVERNO❄️ e questi sono i colori che ti valorizzano e quelli nemici:\n\n" \
                  "🌈 Colori Freddi e Intensi: \n"\
                  "• Blu Navy\n"\
                  "• Nero\n"\
                  "• Bianco ottico\n"\
                  "• Rosso Rubino \n"\
                  "• Viola Profondo\n"\
                  "• Verde Abete\n"\
                  "• Grigio Antracite\n"\
                  "🌈 Colori nemici: Colori caldi e attenuati come beige e arancio \n\n"\
                  
    else:
        palette = "Stagione non riconosciuta."
    return palette

# Funzione per generare la risposta sull'abbigliamento in base alla stagione cromatica
def genera_risposta_abbigliamento(stagione):
    if stagione == "PRIMAVERA🌸":
        abbigliamento = "La tua stagione è PRIMAVERA🌸, stagione più rara in Italia. I capi che ti consiglio sono:\n\n"\
                        "👕 Le stampe funzionano un po’ tutte, in particolare quelle floreali, basta che abbiano buon contrasto\n"\
                        "⚠️ATTENZIONE⚠️\n Puoi indossare capi fuori dalla tua palette di colori, ma è essenziale che gli oggetti vicino al viso (come le maglie) siano adatti alla tua palette. Se la maglia non è adatta, aggiungi accessori che si armonizzino con i tuoi colori. \n\n\n" 
    elif stagione == "ESTATE☀️":
        abbigliamento = "La tua stagione è ESTATE☀️ e i capi che ti consiglio sono: \n\n" \
                        "👕 Fantasie consigliate sono quelle con disegni piccoli, come i quadretti e le millerighe\n"\
                        "⚠️ATTENZIONE⚠️\n Puoi indossare capi fuori dalla tua palette di colori, ma è essenziale che gli oggetti vicino al viso (come le maglie) siano adatti alla tua palette. Se la maglia non è adatta, aggiungi accessori che si armonizzino con i tuoi colori. \n\n\n" 
    elif stagione == "AUTUNNO🍁":
        abbigliamento = "La tua stagione è AUTUNNO🍁 e i capi che ti consiglio sono: \n\n" \
                        "👕 Tessuti come cashmere e il lino\n" \
                        "👕 Fantasie foliage\n"\
                        "⚠️ATTENZIONE⚠️\n Puoi indossare capi fuori dalla tua palette di colori, ma è essenziale che gli oggetti vicino al viso (come le maglie) siano adatti alla tua palette. Se la maglia non è adatta, aggiungi accessori che si armonizzino con i tuoi colori. \n\n\n" 
    elif stagione == "INVERNO❄️":
        abbigliamento = "La tua stagione è INVERNO❄️ e i capi che ti consiglio sono: \n\n" \
                        "👕 Fantasie a forte contrasto come i pois bianco e nero e le righe marinare\n"\
                        "⚠️ATTENZIONE⚠️\n Puoi indossare capi fuori dalla tua palette di colori, ma è essenziale che gli oggetti vicino al viso (come le maglie) siano adatti alla tua palette. Se la maglia non è adatta, aggiungi accessori che si armonizzino con i tuoi colori. \n\n\n" 
    else:
        abbigliamento = "Stagione non riconosciuta."
    return abbigliamento

# Funzione per generare la risposta sui capelli in base alla stagione cromatica
def genera_risposta_capelli(stagione):
    if stagione == "PRIMAVERA🌸":
        capelli = "La tua stagione è PRIMAVERA🌸 e i colori per capelli che ti consiglio sono: \n\n" \
                    "💇🏻‍♀️ Biondo miele e rosso, biondo dorato, il biondo scuro e il castano chiaro\n\n"
    elif stagione == "ESTATE☀️":
        capelli = "La tua stagione è ESTATE☀️ e i colori per capelli che ti consiglio sono: \n\n" \
                    "💇🏻‍♀️ Biondo chiaro e castano medio\n\n"
    elif stagione == "AUTUNNO🍁":
        capelli = "La tua stagione è AUTUNNO🍁 e i colori per capelli che ti consiglio sono: \n\n" \
                    "💇🏻‍♀️ Biondo, castano (sia chiaro che scuro) oppure rosso\n\n"
    elif stagione == "INVERNO❄️":
        capelli = "La tua stagione è INVERNO❄️ e i colori per capelli che ti consiglio sono: \n\n" \
                    "💇🏻‍♀️ Dai toni del castano scuro fino al nero corvino, a volte possono comprendere anche tonalità più chiare come il biondo cenere\n\n"
    else:
        capelli = "Stagione non riconosciuta."
    return capelli

# Funzione per generare la risposta sul make-up in base alla stagione cromatica
def genera_risposta_makeup(stagione):
    if stagione == "PRIMAVERA🌸":
        makeup = "La tua stagione è PRIMAVERA🌸 e questi sono i make-up che ti valorizzano: \n\n" \
                 "💄 Fondotinta: Neutri radiosi, beige-nude molto luminosi. \n"\
                 "💄 Blush: Albicocca e rosa caldi, anche corallo in estate.  \n"\
                 "💄 Occhi: Tonalità brillanti e sottotoni caldi come bronzo, melanzana, terracotta, ruggine, rosa anticato.  \n"\
                 "💄 Labbra: Nude caldi come rosa albicoccato, salmone, beige ambrato e rosso fragola, con una punta di giallo o aranciato. \n\n"
    elif stagione == "ESTATE☀️":
        makeup = "La tua stagione è ESTATE☀️ e questi sono i make-up che ti valorizzano: \n\n" \
                 "💄 Fondotinta: Rosato freddo o avorio per un colore di porcellana.  \n"\
                 "💄 Blush: Rosa freddi come confetto e rosa seta.  \n"\
                 "💄 Occhi: Ombretti come azzurro freddo, grigi, perla, mauve, talpa, rosa.  \n"\
                 "💄 Labbra: Rosso freddo come il ciliegia e neutri rosati come rosa petalo. \n\n"
    elif stagione == "AUTUNNO🍁":
        makeup = "La tua stagione è AUTUNNO🍁 e questi sono i make-up che ti valorizzano: \n\n" \
                  "💄 Fondotinta: Giallo o rosa caldo per mantenere il calore naturale.  \n"\
                  "💄 Blush: Pesca e successivamente terra e corallo con l’abbronzatura.  \n"\
                  "💄 Occhi: Ombretti nei toni del bronzo, cioccolato, melanzana.  \n"\
                  "💄 Labbra: Nude calde e caramellate o rossi mat come rossi mela all’aragosta. \n\n"
    elif stagione == "INVERNO❄️":
        makeup = "La tua stagione è INVERNO❄️ e questi sono i make-up che ti valorizzano: \n\n" \
                  "💄 Fondotinta: Avorio o leggermente rosato, evitando il giallo o il pesca.  \n"\
                  "💄 Blush: Rosato freddo.  \n"\
                  "💄 Occhi: Tonalità del marrone freddo, nero, blu, grigi profondi e, come colore azzardo, il bordeaux.  \n"\
                  "💄 Labbra: Rossi freddi sontuosi con una punta di blu, come rossi rubino fino ai bordeaux o ai vinaccia, oltre a rosa freddo, malva, e frutto di bosco. \n\n"
    else:
        makeup = "Stagione non riconosciuta."
    return makeup

# Funzione per generare la risposta sui gioielli in base alla stagione cromatica
def genera_risposta_gioielli(stagione):
    if stagione == "PRIMAVERA🌸":
        gioielli = "La tua stagione è PRIMAVERA🌸 e i gioielli che ti consiglio sono: \n\n" \
                   "💎 Metalli tipici caldi: oro e argento, giallo o rosa\n" \
                   "💎 Pietre e/o gemme: aulite celeste, smalti corallo e agata verde\n\n" 
    elif stagione == "ESTATE☀️":
        gioielli = "La tua stagione è ESTATE☀️ e i gioielli che ti consiglio sono: \n\n" \
                   "💎 Metalli tipici: oro bianco e argento naturale\n" \
                   "💎 Pietre e/o gemme: quarzo rosa, prehnite, smalti turchesi, perle barocche e grigie\n\n" 
    elif stagione == "AUTUNNO🍁":
        gioielli = "La tua stagione è AUTUNNO🍁 e i gioielli che ti consiglio sono: \n\n" \
                   "💎 Metalli tipici: giallo oro, argento rosé e bronzo\n" \
                   "💎 Pietre e/o gemme: labradorite, il marrone e il verde scuro dell’agata muschiata, il giallo dell’ambra\n\n" 
    elif stagione == "INVERNO❄️":
        gioielli = "La tua stagione è INVERNO❄️ e i gioielli che ti consiglio sono: \n\n" \
                    "💎 Metalli tipici: platino, l’oro bianco e l’argento\n" \
                    "💎 Pietre e/o gemme: ametista viola, agata nera e rubino, apatite blu\n\n" 
    else:
        gioielli = "Stagione non riconosciuta."
    return gioielli




# Funzione per gestire la scelta dell'utente
def gestisci_scelta_utente(data):
    if 'sessionInfo' in data and 'parameters' in data['sessionInfo']:
        parameters = data['sessionInfo']['parameters']
        if 'curiosita' in parameters:
            curiosita = parameters['curiosita'].strip().lower()
            return curiosita
    return ""

# endpoint per gestire le richieste di dialogflow
@app.route('/dialogflow', methods=['POST'])
def dialogflow():
    global count_sottotono_A, count_sottotono_B, sottotono
    global count_intensità_A, count_intensità_B, intensità, stagione
    count_sottotono_A = 0
    count_sottotono_B = 0
    count_intensità_A = 0
    count_intensità_B = 0
    intensità = ""
    sottotono = ""
    data = request.get_json()  # get data from dialogflow
    
    # Determino il sottotono della pelle solo se non è già stato determinato
    if not sottotono:
        sottotono = determina_sottotono(data)

    # Se il sottotono è stato determinato e il intensità non è ancora stato determinato, chiedo la domanda sul intensità
    if sottotono and not intensità and all(data['sessionInfo']['parameters'].get(f'intensita_risposta_{i}', '') == '' for i in range(6, 9)):
        return jsonify({
            "fulfillmentResponse": {
                "messages": [
                    {
                        "text": {
                            "text": [f"Il sottotono della tua pelle è {sottotono}. \n"
                                     + "Ora scopriamo se la tua intensità è alta o bassa! \n\n"
                                     + "6. Di che colore sono i tuoi occhi? \n\n"
                                     + "🅰️ Azzurri, verdi, grigi o nocciola/verdi \n"
                                     + "🅱️ Blu brillante, verdi, castani o neri \n"]
                        }
                    }
                ]
            }
        })

    # Se l'intensità non è ancora stato determinato, lo determino
    if sottotono and not intensità:
        intensità = determina_intensità(data)
    
    

    # Se sia il sottotono che il intensità sono stati determinati e non c'è già una curiosita dell'utente, determino la stagione cromatica
    if sottotono and intensità and not gestisci_scelta_utente(data):
        stagione = determina_stagione(sottotono, intensità)
        message = f"Prima abbiamo visto che il sottotono della tua pelle è {sottotono}. \n"
        message += f"Ora abbiamo stabilito che la tua intensità è {intensità}. \n\n"
        message += f"Quindi, la tua stagione cromatica è {stagione}!\n\n"
        

        # Altre opzioni per l'utente solo se non è stato scelto ancora una curiosita
        message += "\nSe sei curioso di scoprirne di più sulla tua stagione, indicami quali tra queste curiosità vuoi che ti mostri:\n"
        message += "▪️ Elenco dei colori che rientrano nella tua palette 🌈\n"
        message += "▪️ Consigli sull'abbigliamento 👕\n"
        message += "▪️ Consigli sui capelli 💇🏻‍♀️\n"
        message += "▪️ Consigli sul make-up 💄\n"
        message += "▪️ Consigli sui gioielli 💍\n"

        count_sottotono_A = 0
        count_sottotono_B = 0
        count_intensità_A = 0
        count_intensità_B = 0
    else:
        message = ""

    # Suggerimento in base alla curiosità dell'utente (palette, abbigliamento, capelli, makeup, gioielli)
    if gestisci_scelta_utente(data) == "palette" and stagione:
        palette_colors = genera_risposta_palette(stagione)
        message += f"{palette_colors}"
        curiosita = ""
    
    if gestisci_scelta_utente(data) == "abbigliamento" and stagione:
        abbigliamento_suggerito = genera_risposta_abbigliamento(stagione)
        message += f"{abbigliamento_suggerito}"
        curiosita = ""

    if gestisci_scelta_utente(data) == "capelli" and stagione:
        capelli_suggeriti = genera_risposta_capelli(stagione)
        message += f"{capelli_suggeriti}"
        curiosita = ""

    if gestisci_scelta_utente(data) == "makeup" and stagione:
        makeup_suggerito = genera_risposta_makeup(stagione)
        message += f"{makeup_suggerito}"
        curiosita = ""

    if gestisci_scelta_utente(data) == "gioielli" and stagione:
        gioiello_suggerito = genera_risposta_gioielli(stagione)
        message += f"{gioiello_suggerito}"
        curiosita = ""


    # Estrai e stampa il parametro "curiosita" se presente
    curiosita = gestisci_scelta_utente(data)
    if curiosita and not (gestisci_scelta_utente(data) == "palette" and stagione):
        message += f""
        print(f"Curiosità dell'utente: {curiosita}")


    # Se c'è un messaggio da restituire, crea la risposta JSON
    if message:
        return jsonify({
            "fulfillmentResponse": {
                "messages": [
                    {
                        "text": {
                            "text": [message]
                        }
                    }
                ]
            }
        })
    else:
        return jsonify({})


# avvio del server
if __name__ == '__main__':
    app.run(debug=True, port=8080)


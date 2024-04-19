from flask import Flask, request, jsonify
from colorama import init, Fore, Style
import math



app = Flask(__name__)

# Inizializzo i contatori per le risposte A e B
count_sottotono_A = 0
count_sottotono_B = 0
count_contrasto_A = 0
count_contrasto_B = 0
sottotono = ""
contrasto = ""
stagione = ""

@app.route('/', methods=['GET', 'POST'])
def home():
    global count_sottotono_A, count_sottotono_B, count_contrasto_A, count_contrasto_B, sottotono, contrasto, stagione
    count_sottotono_A = 0
    count_sottotono_B = 0
    count_contrasto_A = 0
    count_contrasto_B = 0
    sottotono = ""
    contrasto = ""
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
        return "CALDO"
    elif count_sottotono_B > count_sottotono_A:
        return "FREDDO"
    else:
        return "non è possibile determinare"

# Funzione per determinare il contrasto in base alle risposte A e B
def determina_contrasto(data):
    global count_contrasto_A, count_contrasto_B
    if 'sessionInfo' in data and 'parameters' in data['sessionInfo']:
        parameters = data['sessionInfo']['parameters']
        # Controlla che tutte e tre le risposte sul contrasto siano state fornite dall'utente
        if all(param_value.strip().lower() in ['a', 'b'] for param_value in [parameters.get(f"contrasto_risposta_{i}", "") for i in range(6, 9)]):
            for i in range(6, 9):  # Itero su tutte le domande del flusso contrasto
                param_name = f"contrasto_risposta_{i}"
                value = parameters[param_name].strip().lower()
                if value == 'a' or value == 'risposta a':
                    count_contrasto_A += 1
                elif value == 'b' or value == 'risposta b':
                    count_contrasto_B += 1

            if count_contrasto_A > count_contrasto_B:
                return "BASSO"
            elif count_contrasto_B > count_contrasto_A:
                return "ALTO"
            else:
                return "non è possibile determinare"

    # Se una o più risposte sul contrasto non sono state fornite, restituisci un valore vuoto e azzerale
    count_contrasto_A = 0
    count_contrasto_B = 0
    return ""

# Funzione per determinare la stagione cromatica in base al sottotono e al contrasto
def determina_stagione(sottotono, contrasto):
    if sottotono == "CALDO":
        if contrasto == "BASSO":
            return "PRIMAVERA"
        else:
            return "AUTUNNO"
    else:
        if contrasto == "BASSO":
            return "ESTATE"
        else:
            return "INVERNO"

# Funzione per generare la risposta sulla palette dei colori in base alla stagione cromatica
def genera_risposta_palette(stagione):
    if stagione == "PRIMAVERA":
        palette = "La tua stagione è PRIMAVERA e i colori che ti valorizzano sono i colori caldi e allegri!\n\n Nello specifico, ti risaltano i seguenti colori: \n" \
                  "- Verde Smeraldo\n" \
                  "- Giallo limone\n" \
                  "- Pesca\n" \
                  "- Corallo\n" \
                  "- Crema\n" \
                  "- Beige caldo\n" \
                  "- Rosso Aranciato\n"\
                    "*******************************************\n"
    elif stagione == "ESTATE":
        palette = "La tua stagione è ESTATE e i colori che ti valorizzano sono i colori freschi e soft!\n\n Nello specifico, ti risaltano i seguenti colori: \n" \
                  "- Azzurro\n" \
                  "- Rosa antico\n" \
                  "- Lavanda\n" \
                  "- Grigio Perla\n" \
                  "- Menta\n" \
                  "- Blu polvere\n" \
                  "- Pesca pallido\n"\
                    "*******************************************\n"
    elif stagione == "AUTUNNO":
        palette = "La tua stagione è AUTUNNO e i colori che ti valorizzano sono i colori caldi e terrosi!\n\n Nello specifico, ti risaltano i seguenti colori: \n" \
                  "- Marrone Cannella\n" \
                  "- Ocra\n" \
                  "- Verde Oliva\n" \
                  "- Senape\n" \
                  "- Arancione Terra\n" \
                  "- Bordeaux\n" \
                  "- Terracotta\n"\
                    "*******************************************\n"
    elif stagione == "INVERNO":
        palette = "La tua stagione è INVERNO e i colori che ti valorizzano sono i colori freddi e intensi!\n\n Nello specifico, ti risaltano i seguenti colori: \n" \
                  "- Blu Navy\n" \
                  "- Nero\n" \
                  "- Bianco Puro\n" \
                  "- Rosso Rubino\n" \
                  "- Viola Profondo\n" \
                  "- Verde Abete\n" \
                  "- Grigio Antracite\n"\
                    "*******************************************\n"
    else:
        palette = "Stagione non riconosciuta."
    return palette

# Funzione per generare la risposta sull'abbigliamento in base alla stagione cromatica
def genera_risposta_abbigliamento(stagione):
    if stagione == "PRIMAVERA":
        abbigliamento = "La tua stagione è PRIMAVERA e i capi che ti consiglio sono: \n\n" \
                        "Sciarpe e Scialli Leggeri:\n" \
                        "- Sciarpe di seta o chiffon in colori vivaci come il giallo limone o il corallo\n" \
                        "- Scialli floreali o con motivi primaverili\n" \
                        "Cappelli e Berretti:\n" \
                        "- Cappelli a tesa larga in paglia o cotone\n" \
                        "- Berretti in tessuti leggeri come il lino o la canapa\n"\
                    "*******************************************\n"
    elif stagione == "ESTATE":
        abbigliamento = "La tua stagione è ESTATE e i capi che ti consiglio sono: \n\n" \
                        "Cappelli da Sole e Cappellini:\n" \
                        "- Cappelli da sole in paglia o cotone con ampie tese\n" \
                        "- Cappellini da baseball in tessuti traspiranti e colori vivaci\n" \
                        "Occhiali da Sole:\n" \
                        "- Occhiali da sole con montature leggere e lenti colorate o a specchio\n"\
                    "*******************************************\n"
    elif stagione == "AUTUNNO":
        abbigliamento = "La tua stagione è AUTUNNO e i capi che ti consiglio sono: \n\n" \
                        "Sciarpe e Scaldacollo:\n" \
                        "- Sciarpe in lana o cachemire in tonalità autunnali come il verde oliva o il bordeaux\n" \
                        "- Scaldacollo in maglia grossa o invernale\n" \
                        "Cappelli e Berretti:\n" \
                        "- Berretti in lana o feltro con colori autunnali come il marrone o il grigio\n"\
                    "*******************************************\n"
    elif stagione == "INVERNO":
        abbigliamento = "La tua stagione è INVERNO e i capi che ti consiglio sono: \n\n" \
                        "Sciarpe e Cappelli Caldi:\n" \
                        "- Sciarpe in lana o pile in tonalità scure come il blu navy o il nero\n" \
                        "- Cappelli di lana o tricot con copricollo\n" \
                        "Guanti e Scaldamani:\n" \
                        "- Guanti in pelle o lana con fodera calda\n" \
                        "- Scaldamani in tessuti termici o imbottiti\n"\
                    "*******************************************\n"
    else:
        abbigliamento = "Stagione non riconosciuta."
    return abbigliamento

# Funzione per generare la risposta sugli accessori in base alla stagione cromatica
def genera_risposta_accessori(stagione):
    if stagione == "PRIMAVERA":
        accessori = "La tua stagione è PRIMAVERA e gli accessori che ti consiglio sono: \n\n" \
                    "Sciarpe e Scialli Leggeri:\n" \
                    "- Sciarpe di seta o chiffon in colori vivaci come il giallo limone o il corallo\n" \
                    "- Scialli floreali o con motivi primaverili\n" \
                    "Cappelli e Berretti:\n" \
                    "- Cappelli a tesa larga in paglia o cotone\n" \
                    "- Berretti in tessuti leggeri come il lino o la canapa\n"\
                    "*******************************************\n"
    elif stagione == "ESTATE":
        accessori = "La tua stagione è ESTATE e gli accessori che ti consiglio sono: \n\n" \
                    "Cappelli da Sole e Cappellini:\n" \
                    "- Cappelli da sole in paglia o cotone con ampie tese\n" \
                    "- Cappellini da baseball in tessuti traspiranti e colori vivaci\n" \
                    "Occhiali da Sole:\n" \
                    "- Occhiali da sole con montature leggere e lenti colorate o a specchio\n"\
                    "*******************************************\n"
    elif stagione == "AUTUNNO":
        accessori = "La tua stagione è AUTUNNO e gli accessori che ti consiglio sono: \n\n" \
                    "Sciarpe e Scaldacollo:\n" \
                    "- Sciarpe in lana o cachemire in tonalità autunnali come il verde oliva o il bordeaux\n" \
                    "- Scaldacollo in maglia grossa o invernale\n" \
                    "Cappelli e Berretti:\n" \
                    "- Berretti in lana o feltro con colori autunnali come il marrone o il grigio\n"\
                    "*******************************************\n"
    elif stagione == "INVERNO":
        accessori = "La tua stagione è INVERNO e gli accessori che ti consiglio sono: \n\n" \
                    "Sciarpe e Cappelli Caldi:\n" \
                    "- Sciarpe in lana o pile in tonalità scure come il blu navy o il nero\n" \
                    "- Cappelli di lana o tricot con copricollo\n" \
                    "Guanti e Scaldamani:\n" \
                    "- Guanti in pelle o lana con fodera calda\n" \
                    "- Scaldamani in tessuti termici o imbottiti\n"\
                    "*******************************************\n"
    else:
        accessori = "Stagione non riconosciuta."
    return accessori

# Funzione per generare la risposta sul make-up in base alla stagione cromatica
def genera_risposta_makeup(stagione):
    if stagione == "PRIMAVERA":
        makeup = "La tua stagione è PRIMAVERA e il make-up che ti consiglio è: \n\n" \
                 "Trucco Fresco e Naturale:\n" \
                 "- Fondotinta leggero o BB cream per una copertura leggera e fresca\n" \
                 "- Ombretti neutri e luminosi come il beige o il pesca\n" \
                 "- Blush in tonalità rosate o pesca per un tocco di freschezza\n" \
                 "- Rossetti in colori soft come il rosa chiaro o il nude\n" \
                 "- Mascara leggero per definire le ciglia senza appesantire lo sguardo\n"\
                    "*******************************************\n"
    elif stagione == "ESTATE":
        makeup = "La tua stagione è ESTATE e il make-up che ti consiglio è: \n\n" \
                 "Trucco Leggero e Resistente all'Acqua:\n" \
                 "- Fondotinta o BB cream con SPF per proteggere la pelle dai raggi solari\n" \
                 "- Ombretti waterproof in colori luminosi e vibranti come il turchese o il bronzo\n" \
                 "- Blush in tonalità corallo o rosa intenso per un tocco di freschezza\n" \
                 "- Rossetti in colori vivaci come il rosso ciliegia o il fucsia\n" \
                 "- Mascara waterproof per evitare sbavature durante le giornate calde\n"\
                    "*******************************************\n"
    elif stagione == "AUTUNNO":
        makeup = "La tua stagione è AUTUNNO e il make-up che ti consiglio è: \n\n" \
                 "Trucco Caldo e Avvolgente:\n" \
                 "- Fondotinta idratante per contrastare l'effetto della pelle secca dovuta al cambio di stagione\n" \
                 "- Ombretti in tonalità calde e terrose come il marrone cioccolato o il bronzo\n" \
                 "- Blush in colori terracotta o arancioni per un aspetto caldo e avvolgente\n" \
                 "- Rossetti in tonalità ricche come il bordeaux o il rosso mattone\n" \
                 "- Mascara volumizzante per uno sguardo intenso e avvolgente\n"\
                    "*******************************************\n"
    elif stagione == "INVERNO":
        makeup = "La tua stagione è INVERNO e il make-up che ti consiglio è: \n\n" \
                 "Trucco Elegante e Intenso:\n" \
                 "- Fondotinta idratante e ad alta copertura per contrastare la secchezza cutanea\n" \
                 "- Ombretti in tonalità scure e intense come il grigio antracite o il viola profondo\n" \
                 "- Blush in tonalità neutre o rosa scuro per un tocco di colore sulle guance\n" \
                 "- Rossetti in colori audaci come il rosso scuro o il borgogna\n" \
                 "- Mascara allungante e volumizzante per uno sguardo intenso e seducente\n"\
                    "*******************************************\n"
    else:
        makeup = "Stagione non riconosciuta."
    return makeup

# Funzione per generare la risposta sui gioielli in base alla stagione cromatica
def genera_risposta_gioielli(stagione):
    if stagione == "PRIMAVERA":
        gioielli = "La tua stagione è PRIMAVERA e i gioielli che ti consiglio sono: \n\n" \
                   "Gioielli Leggeri e Floreali:\n" \
                   "- Collane con pendenti a forma di fiore o di foglia\n" \
                   "- Braccialetti con charm primaverili come farfalle o fiori\n" \
                   "- Orecchini a goccia o a cerchio con motivi floreali\n" \
                   "- Anelli con pietre colorate e brillanti come zaffiri o ametiste\n" \
                   "- Gioielli in argento o oro rosa per un tocco delicato e luminoso\n"\
                    "*******************************************\n"
    elif stagione == "ESTATE":
        gioielli = "La tua stagione è ESTATE e i gioielli che ti consiglio sono: \n\n" \
                   "Gioielli Brillanti e Colorati:\n" \
                   "- Collane lunghe con perle o pietre semipreziose come il corallo o il turchese\n" \
                   "- Bracciali multicolori con perle o pietre brillanti\n" \
                   "- Orecchini a lobo con pietre luminose e colorate come l'acquamarina o il topazio\n" \
                   "- Anelli con pietre colorate e vivaci come il rubino o lo zaffiro\n" \
                   "- Gioielli placcati in oro per riflettere la luce solare estiva\n"\
                    "*******************************************\n"
    elif stagione == "AUTUNNO":
        gioielli = "La tua stagione è AUTUNNO e i gioielli che ti consiglio sono: \n\n" \
                   "Gioielli Caldi e Terrosi:\n" \
                   "- Collane con pendenti in pietre naturali come l'agata o l'ambra\n" \
                   "- Bracciali in bronzo o ottone con motivi geometrici o naturali\n" \
                   "- Orecchini a cerchio o a goccia con pietre autunnali come l'occhio di tigre o il quarzo fumé\n" \
                   "- Anelli con pietre calde e ricche come l'ambra o il citrino\n" \
                   "- Gioielli in oro giallo o rame per un aspetto caldo e avvolgente\n"\
                    "*******************************************\n"
    elif stagione == "INVERNO":
        gioielli = "La tua stagione è INVERNO e i gioielli che ti consiglio sono: \n\n" \
                    "Gioielli Eleganti e Scintillanti:\n" \
                    "- Collane a girocollo con pendenti in cristallo o zirconi\n" \
                    "- Bracciali rigidi o a maglie con dettagli scintillanti\n" \
                    "- Orecchini a cerchio o pendenti con cristalli o perle di fiume\n" \
                    "- Anelli con diamanti o pietre preziose come lo zaffiro o l'opale\n" \
                    "- Gioielli in platino o oro bianco per uno stile elegante e raffinato\n"\
                    "*******************************************\n"
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
    global count_contrasto_A, count_contrasto_B, contrasto, stagione
    count_sottotono_A = 0
    count_sottotono_B = 0
    count_contrasto_A = 0
    count_contrasto_B = 0
    contrasto = ""
    sottotono = ""
    data = request.get_json()  # get data from dialogflow
    
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
    
    

    # Se sia il sottotono che il contrasto sono stati determinati e non c'è già una curiosita dell'utente, determino la stagione cromatica
    if sottotono and contrasto and not gestisci_scelta_utente(data):
        stagione = determina_stagione(sottotono, contrasto)
        message = f"Prima abbiamo visto che il sottotono della tua pelle è {sottotono}. \n"
        message += f"Ora abbiamo stabilito che il tuo contrasto è {contrasto}. \n\n"
        message += f"Quindi, la tua stagione cromatica è {stagione}!\n\n"
        message += f"*******************************************\n"
        

        # Altre opzioni per l'utente solo se non è stato scelto ancora una curiosita
        message += "\nSe sei curioso di scoprirne di più sulla tua stagione, indicami quali tra queste cose vuoi che ti mostri:\n"
        message += "- Elenco dei colori che rientrano nella mia palette\n"
        message += "- Consigli sull'abbigliamento\n"
        message += "- Consigli sugli accessori\n"
        message += "- Consigli sul make-up\n"
        message += "- Consigli sui gioielli\n"

        count_sottotono_A = 0
        count_sottotono_B = 0
        count_contrasto_A = 0
        count_contrasto_B = 0
    else:
        message = ""

    # Suggerimento in base alla curiosità dell'utente (palette, abbigliamento, accessori, makeup, gioielli)
    if gestisci_scelta_utente(data) == "palette" and stagione:
        palette_colors = genera_risposta_palette(stagione)
        message += f"{palette_colors}"
        curiosita = ""
    
    if gestisci_scelta_utente(data) == "abbigliamento" and stagione:
        abbigliamento_suggerito = genera_risposta_abbigliamento(stagione)
        message += f"{abbigliamento_suggerito}"
        curiosita = ""

    if gestisci_scelta_utente(data) == "accessori" and stagione:
        accessori_suggerito = genera_risposta_accessori(stagione)
        message += f"{accessori_suggerito}"
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


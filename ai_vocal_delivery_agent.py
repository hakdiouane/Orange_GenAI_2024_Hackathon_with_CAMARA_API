import time
import speech_recognition as sr
import pyttsx3
import openai
from openai import OpenAI
import requests

CLIENT_ID = "YOUR_CLIENT_ID"
CLIENT_SECRET = "YOUR_CLIENT_SECRET"
AUTH_HEADER = "YOUR_AUTH_HEADER"
PHONE_NUMBER = "PHONE_NUMBER_AVAILABLE_FROM_API"

def get_access_token(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, scope=""):
    token_url = 'https://api.orange.com/oauth/v3/token'
    payload = {
        'grant_type': 'client_credentials',
        'Authorization': AUTH_HEADER,
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': scope
    }
    response = requests.post(token_url, data=payload)
    response_data = response.json()
    access_token = response_data.get('access_token')
    return response_data['access_token']




# === FONCTIONS API CAMARA ===

def get_device_location(access_token, phone_number=PHONE_NUMBER):
    """Récupère la position actuelle de l'utilisateur via l'API CAMARA."""
    api_url = 'https://api.orange.com/camara/location-retrieval/orange-lab/v0/retrieve'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'x-correlator': 'your_correlator'
    }
    data = {
        "device": {
            "phoneNumber": phone_number
        },
        "maxAge": 60
    }
    response = requests.post(api_url, headers=headers, json=data)

    if response.status_code == 200:
        location_data = response.json()
        return {
            "latitude": location_data["area"]["center"]["latitude"],
            "longitude": location_data["area"]["center"]["longitude"],
        }
    else:
        print(f"Erreur lors de la récupération de la position : {response.status_code} - {response.text}")
        return None

def verify_location_in_zone(access_token, phone_number="+33699901031", latitude="48.80", longitude="2.26999", radius="2000", max_age=3600):
    """
    Vérifie si un appareil est dans une zone circulaire spécifiée via l'API Location Verification.

    :param access_token: Jeton d'accès pour l'API.
    :param phone_number: Numéro de téléphone de l'appareil au format E.164 (par exemple, "+33699901031").
    :param latitude: Latitude du centre de la zone.
    :param longitude: Longitude du centre de la zone.
    :param radius: Rayon de la zone en mètres.
    :param max_age: Âge maximal acceptable des données de localisation en secondes (par défaut : 3600).
    :return: Résultat de la vérification ou None en cas d'erreur.
    """
    url = "https://api.orange.com/camara/location-verification/orange-lab/v0/verify"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Cache-Control": "no-cache",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    data = {
        "device": {
            "phoneNumber": phone_number
        },
        "area": {
            "areaType": "CIRCLE",
            "center": {
                "latitude": latitude,
                "longitude": longitude
            },
            "radius": radius
        },
        "maxAge": max_age
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        print("Vérification de la localisation réussie.")
        print(response.json())
        return response.json()
    else:
        print(f"Erreur lors de la vérification de la localisation : {response.status_code}")
        print(response.text)
        return None





def setup_geofencing(access_token):
    """
    Crée une souscription de géorepérage pour un appareil via l'API Geofencing avec des paramètres prédéfinis.
    """
    # URL de l'API
    url = "https://api.orange.com/camara/geofencing/orange-lab/v0/subscriptions"


    # Paramètres de la requête
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Cache-Control": "no-cache",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    # Données de la souscription
    data = {
        "protocol": "HTTP",
        "sink": "https://notificationSendServer12.supertelco.com",
        "types": [
            "org.camaraproject.geofencing-subscriptions.v0.area-entered"
        ],
        "config": {
            "subscriptionDetail": {
                "device": {
                    "phoneNumber": "+33699901032"
                },
                "area": {
                    "areaType": "CIRCLE",
                    "center": {
                        "latitude": "48.80",
                        "longitude": "2.259"
                    },
                    "radius": 2000
                }
            },
            "initialEvent": True,
            "subscriptionMaxEvents": 10,
            "subscriptionExpireTime": "2024-03-22T05:40:58.469Z"
        }
    }

    # Effectuer la requête POST
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        print("Souscription de géorepérage créée avec succès.")
        print(response.json())
        return response.json()
    else:
        print(f"Erreur lors de la création de la souscription : {response.status_code}")
        print(response.text)
        return None



def check_device_connectivity(access_token):
    """
    Vérifie la joignabilité d'un appareil via l'API Device Reachability Status.
    """
    # URL de l'API
    url = "https://api.orange.com/camara/orange-lab/device-reachability-status/v0/retrieve"


    # En-têtes de la requête
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Cache-Control": "no-cache",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    # Corps de la requête
    data = {
        "device": {
            "phoneNumber": "+33699901064"
        }
    }

    # Effectuer la requête POST
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        print("Joignabilité de l'appareil vérifiée avec succès.")
        print(response.json())
        return response.json()
    else:
        print(f"Erreur lors de la vérification de la joignabilité : {response.status_code}")
        print(response.text)
        return None


def request_network_quality_boost(access_token):
    url = "https://api.orange.com/camara/quality-on-demand/orange-lab/v0/sessions"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Cache-Control": "no-cache",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    data = {
        "duration": 600,
        "device": {
            "ipv4Address": {
                "publicAddress": "172.20.120.105",
                "privateAddress": "172.20.120.105"
            }
        },
        "applicationServer": {
            "ipv4Address": "172.20.120.84"
        },
        "devicePorts": {
            "ports": [50984]
        },
        "applicationServerPorts": {
            "ports": [10000]
        },
        "qosProfile": "b55e2cc8-b386-4d90-9f95-b98ba20be050",
        "webhook": {
            "notificationUrl": "https://webhook.site/.....-b450-cfffc51b4c13"
        },
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        print("Session QoS créée avec succès.")
        print(response.json())
    else:
        print(f"Erreur lors de la création de la session QoS : {response.status_code}")
        print(response.text)




def kyc_verification(access_token):
    url = "https://api.orange.com/camara/orange-lab/kyc-match/v0/match"
    headers = {
        "Authorization": f"Bearer {access_token}",
        'x-correlator': 'your_correlator'
    }
    data = {
        "phoneNumber": "+33699901031",
        "givenName": "Maeva",
        "familyName": "Hurt",
        "address": "12 impasse Samson",
        "locality": "Pottrnec",
        "email": "maeva.huart@voila.fr"
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        print("Vérification KYC réussie.")
        print(response.json())
    else:
        print(f"Erreur lors de la vérification KYC : {response.status_code}")
        print(response.text)
    
########### AGENT ###########


client = OpenAI(
    api_key = "YOUR_OPENAI_API_KEY"
)

# Initialisation de la synthèse vocale
tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 350)

def speak(text):
    """Prononce le texte donné."""
    tts_engine.say(text)
    tts_engine.runAndWait()




# === FONCTIONS GPT ===

def analyze_with_llm(user_input):
    """Analyse le texte avec le LLM pour fournir des instructions."""
    try:
        completion = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": '''
                    Tu es un assistant pour livreurs. Voici les fonctions disponibles que tu peux appeler en fonction des demandes :
                    - kyc_verification : Vérifie l'identité de l'utilisateur.
                    - get_device_location : Récupère la position actuelle du livreur.
                    - verify_location_in_zone : Vérifie si l'utilisateur est dans une zone spécifique (par exemple, zone de livraison).
                    - request_network_quality_boost : Améliore la qualité du réseau si nécessaire.
                    - check_device_connectivity : Vérifie si l'appareil est joignable.

                    Lorsqu'une demande de l'utilisateur nécessite l'exécution d'une fonction API, ajoute à ta réponse : "Exécuter : nom_de_la_fonction".
                    Sinon, réponds simplement à la question ou fais une suggestion.
                '''},
                {"role": "user", "content": user_input},
            ]
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"Erreur avec le modèle GPT : {str(e)}"

# === LOGIQUE PRINCIPALE ===

def continuous_assistant(access_token):
    """Assistant automatisé pour livreurs."""
    recognizer = sr.Recognizer()
    conversation_history = []  # Historique des conversations
    last_activity_time = time.time()  # Temps de la dernière activité utilisateur
    check_interval = 5  # Intervalle d'écoute (en secondes)
    max_inactivity = 10  # Durée maximale sans activité (en secondes)

    # Initialisation
    speak("Bonjour, je suis votre assistant. Dites 'assistant' pour démarrer.")
    
    # Définir une zone de livraison fictive pour les tests
    delivery_zone = {"latitude": 48.8566, "longitude": 2.3522, "radius": 1000}  # Exemple pour Paris

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=2)
        
        while True:
            try:
                # Vérifie l'inactivité
                inactivity_duration = time.time() - last_activity_time
                if inactivity_duration > max_inactivity:
                    #handle_inactivity(access_token)
                    last_activity_time = time.time()
                    continue

                print("Écoute en cours...")
                try:
                    # Écoute et reconnaissance vocale
                    audio = recognizer.listen(source, timeout=check_interval, phrase_time_limit=5)
                    user_text = process_user_input(audio, recognizer)
                    if not user_text:
                        continue

                    # Mise à jour de l'heure de la dernière activité
                    last_activity_time = time.time()

                    # Analyse avec LLM
                    llm_response = analyze_with_llm(user_text)
                    print(f"LLM : {llm_response}")
                    speak(llm_response)
                    conversation_history.append({"role": "assistant", "content": llm_response})

                    # Vérification et exécution des actions demandées par le LLM
                    handle_llm_actions(llm_response.strip(), access_token, delivery_zone)

                except sr.UnknownValueError:
                    print("Je n'ai pas compris. Silence ou bruit de fond détecté.")
                except sr.WaitTimeoutError:
                    print("Aucune activité détectée pendant l'écoute.")

            except sr.RequestError as e:
                print(f"Erreur de reconnaissance vocale : {e}")
                speak("Erreur de reconnaissance vocale. Veuillez patienter.")
            except Exception as e:
                print(f"Erreur inattendue : {e}")
                speak("Une erreur inattendue est survenue. Veuillez réessayer.")


# === Fonctions auxiliaires ===

def handle_inactivity(access_token):
    """Gère les périodes d'inactivité."""
    print("Aucune activité détectée. Vérification de la connectivité...")
    if not check_device_connectivity(access_token):
        print("Appareil injoignable. Contacter l'administrateur.")
        speak("Appareil injoignable. Veuillez contacter un administrateur.")
        raise SystemExit  # Arrête l'assistant si l'appareil est injoignable
    else:
        print("Appareil joignable. Aucune activité détectée. Veuillez parler.")
        speak("Appareil joignable. Veuillez parler.")


def process_user_input(audio, recognizer):
    """Traite l'entrée utilisateur pour convertir l'audio en texte."""
    try:
        user_text = recognizer.recognize_google(audio, language="fr-FR").lower()
        print(f"Utilisateur : {user_text}")
        return user_text.strip()
    except sr.UnknownValueError:
        print("Je n'ai pas compris. Silence ou bruit de fond détecté.")
        return None


def handle_llm_actions(llm_response, access_token):
    """Vérifie les actions demandées par le LLM et exécute les fonctions appropriées."""
    if "Exécuter :" not in llm_response:
        return

    action = llm_response.split(": ")[1].strip().lower()
    print("ACTION = ",action)

    if "kyc_verification" in action:
        if not kyc_verification(access_token):
            speak("Vérification de votre identité échouée. Veuillez réessayer.")
        else:
            speak("Vérification d'identité réussie.")
    elif "get_device_location" in action:
        location = get_device_location(access_token)
        if location:
            speak(f"Votre localisation actuelle est {location['latitude']}, {location['longitude']}.")
        else:
            speak("Impossible de récupérer votre position.")
    elif "verify_location_in_zone" in action:
        location = get_device_location(access_token)
        if location and not verify_location_in_zone(access_token=access_token, latitude=location["latitude"],longitude=location["longitude"]):
            speak("Vous êtes en dehors de la zone de livraison.")
        else:
            speak("Vous êtes dans la zone de livraison.")
    elif "request_network_quality_boost" in action:
        if request_network_quality_boost(access_token) == "success":
            speak("La qualité du réseau a été améliorée.")
        else:
            speak("Je n'ai pas pu améliorer la qualité du réseau.")
    elif "check_device_connectivity" in action:
        if check_device_connectivity(access_token):
            speak("L'appareil est joignable.")
        else:
            speak("L'appareil n'est pas joignable. Veuillez contacter un administrateur.")
    else:
        speak("Je n'ai pas compris quelle action exécuter.")




def main():
    """Lance l'assistant vocal et le polling des notifications."""
    access_token = get_access_token(CLIENT_ID, CLIENT_SECRET)
    if not access_token:
        print("Impossible d'obtenir le jeton d'accès. Arrêt.")
        return
    
    print(f"Access Token : {access_token}")


    # Démarre le polling et l'assistant vocal dans des threads séparés
    continuous_assistant(access_token)


if __name__ == "__main__":
    main()

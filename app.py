import streamlit as st
import requests
from io import BytesIO
import base64
import json

import time

decoded_image_data = "decoded_image.png"

# set connection
headers = {
    'Content-Type': 'application/json',
    'Authorization': f"Bearer {st.secrets['api']['authorization']}"
}


### Frontend
st.title(":blue[Dör]:red[We]:green[Dall]:sparkles: Vision")

col1, col2 = st.columns(2)

with col1:
    st.image("output_image.png", caption="letztes generiertes Bild")

with col2:
    st.write("""
        Für gute Ergebnisse den Prompt in Englisch befüllen | *For best results speak english !*
    
        [ChatGPT beim Prompt erstellen helfen lassen](https://chatgpt.com/g/g-NLx886UZW-flux-prompt-pro)
    
        Ein Bild zu generieren kann locker mal 2 - 3 Minuten dauern!
    
        Im Prompt den Namen klein schreiben in der Form: :green[markusdoering, a cool man] oder :green[natalieweber, a beautiful woman]
    
        Jedes Bild kostet den Jan Geld 💰
    
        """)

    option = st.selectbox(
        "Person wählen",
        ("Markus", "Natalie", "Jan"),
    )

    st.write("You selected:", option)

    if option == "Markus":
        with open('markus.json') as comfyui_file:
            file_contents = comfyui_file.read()
            data_template_loaded = json.loads(file_contents)
            data_template = data_template_loaded

    elif option == "Natalie":
        with open('natalie.json') as comfyui_file:
            file_contents = comfyui_file.read()
            data_template_loaded = json.loads(file_contents)
            data_template = data_template_loaded
    else:
        with open('jan.json') as comfyui_file:
            file_contents = comfyui_file.read()
            data_template_loaded = json.loads(file_contents)
            data_template = data_template_loaded

print(option)
print(data_template)


### PROMPT
st.text_area("Prompt", key="new_prompt")
# You can access the value at any point with:
print(st.session_state.new_prompt)
prompt = st.session_state.new_prompt.replace('\n', ' ').replace('\r', '')
print(prompt)

# Replace the CLIP Text Encode (Prompt) Placeholder
data = json.loads(json.dumps(data_template).replace("YOUR_PROMPT",prompt))
print(data)

def generate_image():
    # POST to runpod
    response = requests.post('https://api.runpod.ai/v2/to8axubqtqzy78/runsync', headers=headers, json=data)

    # GET image as base64
    message = response.json().get("output", {}).get("message", "Kein Message-Schlüssel gefunden")

    # debug:
    # print(message)
    print(option)

    # base64 codierter String
    base64_string = message
    # Base64-String dekodieren
    image_data = base64.b64decode(base64_string)
    # In ein BytesIO-Objekt umwandeln
    image_stream = BytesIO(image_data)
    # Bild in Streamlit anzeigen
    st.image(image_stream, caption="Generiertes Bild", use_container_width=True)



    # Bild speichern auf dem Server
    output_path = "output_image.png"
    with open(output_path, "wb") as file:
        file.write(image_stream.getvalue())  # Holt die Bytes aus dem Stream



    print(f"Bild erfolgreich gespeichert als {output_path}")

upper = st.container()
lower = st.container()


if 'run_button' in st.session_state and st.session_state.run_button == True:
    with st.spinner("Wait for it...", show_time=True):
        generate_image()

upper.button('Bild generieren', key='run_button', use_container_width=True)


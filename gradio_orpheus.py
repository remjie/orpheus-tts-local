import os
import time
import gradio as gr
from gguf_orpheus import generate_speech_from_api, AVAILABLE_VOICES, DEFAULT_VOICE

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def synthesize_and_play(text, voice):
    if not text.strip():
        return None, "Veuillez saisir un texte."
    
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(OUTPUT_DIR, f"{voice}_{timestamp}.wav")
    
    try:
        generate_speech_from_api(
            prompt=text,
            voice=voice,
            output_file=output_file
        )
        return output_file, f"Audio généré et sauvegardé dans {output_file}"
    except Exception as e:
        return None, f"Erreur: {e}"

with gr.Blocks(title="Orpheus TTS Local") as demo:
    gr.Markdown("## 🎙️ Orpheus TTS Local\nSaisissez un texte et écoutez la voix générée.")
    
    with gr.Row():
        text_input = gr.Textbox(label="Texte à convertir", lines=3, placeholder="Entrez votre texte ici...")
    
    voice_dropdown = gr.Dropdown(choices=AVAILABLE_VOICES, value=DEFAULT_VOICE, label="Voix")
    
    generate_button = gr.Button("Générer")
    
    audio_output = gr.Audio(label="Lecture audio", type="filepath")
    status_output = gr.Textbox(label="Statut", interactive=False)
    
    generate_button.click(
        fn=synthesize_and_play,
        inputs=[text_input, voice_dropdown],
        outputs=[audio_output, status_output]
    )

if __name__ == "__main__":
    demo.launch()

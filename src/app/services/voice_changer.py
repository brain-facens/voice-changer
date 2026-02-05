import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import save


load_dotenv()

OUTPUT_DIR = os.getenv("OUTPUT_FILES_PATH")

def voice_changer(
        voice_id: str = os.getenv("MAN_ID"), 
        audio_url: str = 'https://storage.googleapis.com/eleven-public-cdn/audio/marketing/nicole.mp3'
    ) -> str:

    try:
        eleven_labs = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
    
        with open(audio_url, "rb") as audio_file:
            audio_stream = eleven_labs.speech_to_speech.convert(
                voice_id=voice_id,
                audio=audio_file,
                model_id="eleven_multilingual_sts_v2",
                output_format="mp3_44100_128",
            )

            out_file_path = os.path.join(OUTPUT_DIR, "out.wav")
            save(audio_stream, out_file_path)

            return out_file_path
    except FileNotFoundError:
        print(f"Error: The file '{audio_url}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def menu():
    girl = os.getenv("GIRL_ID")
    boy = os.getenv("BOY_ID")
    man = os.getenv("MAN_ID")
    woman = os.getenv("WOWAN_ID")
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("1 - Menina\n2 - Menino\n3 - Homem\n4 - Mulher\n")
        option = int(input("Opção: "))

        if option == 1:
            voice_id = girl
        elif option == 2:
            voice_id = boy
        elif option == 3:
            voice_id = man
        elif option == 4:
            voice_id = woman
        else:
            print("Opção não encontrada! Tente novamente.")
            break

        audio_url = os.getenv("AUDIO_TEST")
        voice_changer(voice_id, audio_url)


if __name__ == '__main__':
    menu()

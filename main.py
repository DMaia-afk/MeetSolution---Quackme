import os
from dotenv import load_dotenv
from record import record_audio_dual
from diarization import transcription_with_diarization, format_transcription, DEFAULT_CONFIGS
from summarizer import generate_summary
from colorama import init, Fore, Back, Style
import torch

# Initialize colorama
init(autoreset=True)

# Load environment variables
load_dotenv()

# Default configurations
configs = DEFAULT_CONFIGS.copy()

def print_title():
    title = """\n\n\n\n
    ███╗   ███╗███████╗███████╗████████╗███████╗ ██████╗ ██╗     ██╗   ██╗████████╗██╗ ██████╗ ███╗   ██╗
    ████╗ ████║██╔════╝██╔════╝╚══██╔══╝██╔════╝██╔═══██╗██║     ██║   ██║╚══██╔══╝██║██╔═══██╗████╗  ██║
    ██╔████╔██║█████╗  █████╗     ██║   ███████╗██║   ██║██║     ██║   ██║   ██║   ██║██║   ██║██╔██╗ ██║
    ██║╚██╔╝██║██╔══╝  ██╔══╝     ██║   ╚════██║██║   ██║██║     ██║   ██║   ██║   ██║██║   ██║██║╚██╗██║
    ██║ ╚═╝ ██║███████╗███████╗   ██║   ███████║╚██████╔╝███████╗╚██████╔╝   ██║   ██║╚██████╔╝██║ ╚████║
    ╚═╝     ╚═╝╚══════╝╚══════╝   ╚═╝   ╚══════╝ ╚═════╝ ╚══════╝ ╚═════╝    ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
    """
    print(Fore.CYAN + Style.BRIGHT + title)
    print(Fore.YELLOW + "Welcome to MeetSolution - Solution for Meeting Transcription and Summarization!\n")

def settings_menu():
    while True:
        os.system('cls')
        print_title()
        print(Fore.CYAN + "\nSettings:")
        print("1. HUGGINGFACE_TOKEN")
        print("2. DEVICE")
        print("3. MODEL_NAME")
        print("4. SPEAKER_COUNT")
        print("5. MAX_SPEAKERS")
        print("6. BATCH_SIZE")
        print("7. LANGUAGE")
        print("8. COMPUTE_TYPE")
        print("9. Back")
        choice = input(Fore.WHITE + "Choose a setting to change (1-9): ").strip()

        if choice == "1":
            new_value = input(Fore.WHITE + f"Current: {configs['HUGGINGFACE_TOKEN']}. New value: ").strip()
            configs['HUGGINGFACE_TOKEN'] = new_value
            print(Fore.GREEN + "Updated.")
        elif choice == "2":
            print(Fore.WHITE + f"Current: {configs['DEVICE']}")
            print("Options: auto, cuda, cpu")
            new_value = input(Fore.WHITE + "New value: ").strip().lower()
            if new_value == "auto":
                configs['DEVICE'] = "cuda" if torch.cuda.is_available() else "cpu"
            elif new_value in ["cuda", "cpu"]:
                configs['DEVICE'] = new_value
            else:
                print(Fore.RED + "Invalid option.")
            print(Fore.GREEN + f"DEVICE set to: {configs['DEVICE']}")
        elif choice == "3":
            new_value = input(Fore.WHITE + f"Current: {configs['MODEL_NAME']}. New value: ").strip()
            configs['MODEL_NAME'] = new_value
            print(Fore.GREEN + "Updated.")
        elif choice == "4":
            new_value = input(Fore.WHITE + f"Current: {configs['SPEAKER_COUNT']} (None for automatic). New value: ").strip()
            if new_value.lower() == "none":
                configs['SPEAKER_COUNT'] = None
            else:
                try:
                    configs['SPEAKER_COUNT'] = int(new_value)
                except ValueError:
                    print(Fore.RED + "Invalid value. Must be a number or 'none'.")
                    continue
            print(Fore.GREEN + "Updated.")
        elif choice == "5":
            new_value = input(Fore.WHITE + f"Current: {configs['MAX_SPEAKERS']}. New value: ").strip()
            try:
                configs['MAX_SPEAKERS'] = int(new_value)
            except ValueError:
                print(Fore.RED + "Invalid value. Must be a number.")
                continue
            print(Fore.GREEN + "Updated.")
        elif choice == "6":
            new_value = input(Fore.WHITE + f"Current: {configs['BATCH_SIZE']}. New value: ").strip()
            try:
                configs['BATCH_SIZE'] = int(new_value)
            except ValueError:
                print(Fore.RED + "Invalid value. Must be a number.")
                continue
            print(Fore.GREEN + "Updated.")
        elif choice == "7":
            new_value = input(Fore.WHITE + f"Current: {configs['LANGUAGE']} (None for automatic). New value: ").strip()
            if new_value.lower() == "none":
                configs['LANGUAGE'] = None
            else:
                configs['LANGUAGE'] = new_value
            print(Fore.GREEN + "Updated.")
        elif choice == "8":
            print(Fore.WHITE + f"Current: {configs['COMPUTE_TYPE']}")
            print("Options: int8, float16, float32")
            new_value = input(Fore.WHITE + "New value: ").strip()
            if new_value in ["int8", "float16", "float32"]:
                configs['COMPUTE_TYPE'] = new_value
            else:
                print(Fore.RED + "Invalid option.")
                continue
            print(Fore.GREEN + "Updated.")
        elif choice == "9":
            break
        else:
            print(Fore.RED + "Invalid option.")

def action_menu():
    audio_file = None
    transcricao = None
    last_audio_file = None

    while True:
        os.system('cls')
        print_title()
        print(Fore.WHITE + "Action Menu:")
        print("1. Record audio")
        print("2. Transcribe")
        print("3. Summarize transcription")
        print("4. Do everything")
        print("9. Settings")
        print("10. Back to Main Menu")
        choice = input(Fore.WHITE + "Choose an option (1-4,9-10): ").strip()

        if choice == "1":
            os.system('cls')
            print(Fore.BLUE + "Starting recording...")
            audio_file = record_audio_dual()
            if not audio_file:
                print(Fore.RED + "Recording failed.")
            else:
                print(Fore.GREEN + f"Audio recorded: {audio_file}")

        elif choice == "2":
            os.system('cls')
            if audio_file:
                use_recorded = input(Fore.WHITE + "Use recorded audio (y) or choose file (n)? ").strip().lower()
                if use_recorded == "y":
                    selected_audio = audio_file
                else:
                    selected_audio = input(Fore.WHITE + "Enter the audio file path: ").strip()
            else:
                selected_audio = input(Fore.WHITE + "Enter the audio file path: ").strip()
            
            if not os.path.exists(selected_audio):
                print(Fore.RED + "File not found.")
                continue
            
            print(Fore.GREEN + "Starting transcription with diarization...")
            final_result = transcription_with_diarization(selected_audio, configs)
            formatted_output = format_transcription(final_result)
            transcricao = "\n".join(f"Speaker {seg['speaker']}: {seg['text']}" for seg in formatted_output)
            
            # Save transcription to file
            base_name = os.path.splitext(os.path.basename(selected_audio))[0]
            transcription_file = f"{base_name}.txt"
            with open(transcription_file, "w", encoding="utf-8") as f:
                f.write(transcricao)
            last_audio_file = selected_audio
            print(Fore.GREEN + f"Transcription completed and saved to {transcription_file}.")

        elif choice == "3":
            os.system('cls')
            if not transcricao:
                print(Fore.RED + "No transcription available. Run option 2 first.")
                continue
            if not last_audio_file:
                print(Fore.RED + "No audio file associated with the transcription.")
                continue
            print(Fore.GREEN + "Generating summary...")
            resumo = generate_summary(transcricao)
            base_name = os.path.splitext(os.path.basename(last_audio_file))[0]
            summary_file = f"summary_{base_name}.txt"
            with open(summary_file, "w", encoding="utf-8") as f:
                f.write(resumo)
            print(Fore.GREEN + f"Summary saved to {summary_file}")

        elif choice == "4":
            os.system('cls')
            print(Fore.BLUE + "Starting recording...")
            audio_file = record_audio_dual()
            if not audio_file:
                print(Fore.RED + "Recording failed.")
                continue
            print(Fore.GREEN + f"Audio recorded: {audio_file}")
            
            print(Fore.GREEN + "Starting transcription with diarization...")
            final_result = transcription_with_diarization(audio_file, configs)
            formatted_output = format_transcription(final_result)
            transcricao = "\n".join(f"Speaker {seg['speaker']}: {seg['text']}" for seg in formatted_output)
            
            # Save transcription to file
            base_name = os.path.splitext(os.path.basename(audio_file))[0]
            transcription_file = f"{base_name}.txt"
            with open(transcription_file, "w", encoding="utf-8") as f:
                f.write(transcricao)
            last_audio_file = audio_file
            print(Fore.GREEN + f"Transcription completed and saved to {transcription_file}.")
            
            print(Fore.GREEN + "Generating summary...")
            resumo = generate_summary(transcricao)
            base_name = os.path.splitext(os.path.basename(audio_file))[0]
            summary_file = f"summary_{base_name}.txt"
            with open(summary_file, "w", encoding="utf-8") as f:
                f.write(resumo)
            print(Fore.GREEN + f"Summary saved to {summary_file}")

        elif choice == "9":
            os.system('cls')
            settings_menu()

        elif choice == "10":
            os.system('cls')
            break

        else:
            print(Fore.RED + "Invalid option. Try again.")

def documentation():
    os.system('cls')
    print_title()
    print(Fore.CYAN + "\nDocumentation:")
    print("MeetSolution is a tool for transcribing and summarizing meeting audio.")
    print("Features:")
    print("- Record audio from microphone and loopback.")
    print("- Transcribe with speaker diarization.")
    print("- Generate structured summaries.")
    print("- Configurable settings for advanced users.")
    print("\nFor more details, check the README.md file or visit the repository:")
    print(Fore.BLUE + "https://github.com/DMaia-afk/MeetSolution---Quackme")
    input(Fore.WHITE + "Press Enter to return to Main Menu.")

def main():
    while True:
        os.system('cls')
        print_title()
        print(Fore.WHITE + "Main Menu:")
        print("1. Start")
        print("2. Documentation")
        print("3. Exit")
        choice = input(Fore.WHITE + "Choose an option (1-3): ").strip()

        if choice == "1":
            action_menu()
        elif choice == "2":
            documentation()
        elif choice == "3":
            print(Fore.YELLOW + "Exiting... Goodbye!")
            break
        else:
            print(Fore.RED + "Invalid option. Try again.")

if __name__ == "__main__":
    main()
from colorama import Fore

def start_vectorize():
    print(Fore.YELLOW + "Vectorizing..." + Fore.RESET)

def vectorize_file(file_name: str):
    print(Fore.BLACK + f"Vectorizing {file_name}..." + Fore.RESET)

def vectorize_finish(ms):
    print(Fore.GREEN + f"Vectorizing finished in {ms}ms" + Fore.RESET)
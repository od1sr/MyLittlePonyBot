from colorama import Fore

def DEBUG_start_pdf_loading():
    print(f"{Fore.YELLOW}[DEBUG]{Fore.RESET} Загрузка PDF ...")

def DEBUG_founded_pdfs(pdf_files):
    print(f"{Fore.GREEN}[DEBUG]{Fore.RESET} Найдено {pdf_files} PDF-файлов.")

def DEBUG_pdf_mathing():
    print(f"{Fore.YELLOW}[DEBUG]{Fore.RESET} Обработка PDF ...")


def DEBUG_prepare_chunks():
    print(f"{Fore.YELLOW}[DEBUG]{Fore.RESET} Подготовка чанков для векторной базы ...")

def DEBUG_prepare_indexing(all_cunks):
    print(f"{Fore.YELLOW}[DEBUG]{Fore.RESET} Подготовка к индексации для векторной базы ...")
    print(f"{Fore.BLACK} | Количество чанков {all_cunks} {Fore.RESET}")

def DEBUG_connect_to_data_base(path):
    print(f"{Fore.YELLOW}[DEBUG]{Fore.RESET} Подключение к векторной базе ...")
    print(f"{Fore.BLACK} | Путь к базе {path} {Fore.RESET}")
import requests
import argparse
from urllib.parse import urljoin

def gobuster(url, wordlist, status_codes, timeout=5):
    found = []

    print(f"[+] Iniciando força bruta em: {url}")
    try:
        with open(wordlist, "r") as f:
            paths = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[-] Wordlist não encontrada: {wordlist}")
        return

    for path in paths:
        full_url = urljoin(url, path)
        try:
            response = requests.get(full_url, timeout=timeout)
            if response.status_code in status_codes:
                print(f"[{response.status_code}] {full_url}")
                found.append((response.status_code, full_url))
        except requests.RequestException as e:
            print(f"[-] Erro ao acessar {full_url}: {e}")

    print("\n[+] Diretórios encontrados:")
    for status, path in found:
        print(f"{status} -> {path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script tipo gobuster em Python")
    parser.add_argument("-u", "--url", required=True, help="URL alvo (ex: http://exemplo.com/)")
    parser.add_argument("-w", "--wordlist", required=True, help="Caminho para a wordlist")
    parser.add_argument("-s", "--status", default="200,204,301,302,307,403", help="Códigos de status a considerar como válidos")
    parser.add_argument("-t", "--timeout", type=int, default=5, help="Timeout para requisições (default: 5s)")

    args = parser.parse_args()
    status_codes = set(int(code.strip()) for code in args.status.split(","))

    gobuster(args.url, args.wordlist, status_codes, args.timeout)

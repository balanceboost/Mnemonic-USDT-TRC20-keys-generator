import random
import time
import concurrent.futures as cf
import requests
from requests.exceptions import RequestException
from blessed import Terminal
import psutil
from rich.panel import Panel
from rich.console import Console
from rich.style import Style
from cryptofuzz import Convertor, Tron
from mnemonic import Mnemonic
import os
import sys

conv = Convertor()
tron = Tron()
console = Console()


def OnClear():
    if "win" in sys.platform.lower():
        os.system("cls")
    else:
        os.system("clear")


def balance(addr):
    url_n = f"https://api.trongrid.io/v1/accounts/{addr}/tokens"
    try:
        req = requests.get(url_n)
        req.raise_for_status()
        tokens = req.json().get('data', [])
        for token in tokens:
            if token['symbol'] == 'USDT':
                return token['balance']
        return "0"
    except RequestException as e:
        # Проверяем код ошибки для определения превышения лимита
        if e.response and e.response.status_code == 429:
            print("Достигнут лимит API, ожидаем 1 час...")
            time.sleep(3600)  # Ожидание 1 час
        return "0"


def transaction(addr):
    url_n = f"https://api.trongrid.io/v1/accounts/{addr}/transactions"
    try:
        req = requests.get(url_n)
        req.raise_for_status()
        return len(req.json().get('data', []))
    except RequestException as e:
        if e.response and e.response.status_code == 429:
            print("Достигнут лимит API, ожидаем 1 час...")
            time.sleep(3600)  # Ожидание 1 час
        return 0


def draw_system_status(term):
    cpu_percent = psutil.cpu_percent()
    ram_percent = psutil.virtual_memory().percent
    disk_percent = psutil.disk_usage('/').percent
    termWidth = term.width
    system_status = (
        f'\n{draw_graph("CPU", cpu_percent, termWidth)}\n'
        f'\n{draw_graph("RAM", ram_percent, termWidth)}\n'
        f'\n{draw_graph("HDD", disk_percent, termWidth)}\n'
    )
    return system_status


def draw_usdt_info(z, w, addr, priv, mixWord, txs):
    usdt_info_panel = (
        f'\n[gold1]Total Checked: [orange_red1]{z}[/][gold1]  Win: [white]{w}[/]'
        f'[gold1]  Transaction: [/][aquamarine1]{txs}\n\n[/][gold1]ADDR: [white] {addr}[/white]\n\n'
        f'PRIVATE: [grey54]{priv}[/grey54]\n\nMNEMONIC: [white]{mixWord}[/white]\n'
    )
    return usdt_info_panel


def draw_graph(title, percent, width):
    bar_length = int(width - 17)
    num_blocks = int(percent * bar_length / 100)
    dash = "[grey54]–[/]"
    barFill = "[green]▬[/]"
    bar = barFill * num_blocks + dash * (bar_length - num_blocks)
    return f"[white]{title}[/]: |{bar}| {percent}%"


def main():
    term = Terminal()
    with term.fullscreen():
        with term.cbreak(), term.hidden_cursor():
            OnClear()
            z = 0
            w = 0
            while True:
                system_status = draw_system_status(term)
                draw_system_status_panel = Panel(system_status, border_style="grey66")
                mne = Mnemonic("english")
                NumberList = [128, 256]
                randomSize = random.choice(NumberList)
                words = mne.generate(strength=randomSize)
                priv = conv.mne_to_hex(words)
                addr = tron.hex_addr(priv)
                mixWord = words[:64]
                txs = transaction(addr)

                if txs > 0:
                    w += 1
                    with open("Found_USDT_TRC20.txt", "a") as fr:
                        fr.write(f"{addr} TXS: {txs} BAL: {balance(addr)}\n")
                        fr.write(f"{priv}\n")
                        fr.write(f"{words}\n")
                        fr.write(f"{'-' * 50}\n")
                else:
                    with open("BAD_USDT_TRC20.txt", "a") as fr:
                        fr.write(f"ADDR: {addr}\n")
                        fr.write(f"PRIVATE: {priv}\n")
                        fr.write(f"MNEMONIC: {words}\n")
                        fr.write(f"{'-' * 50}\n")

                usdt_info_panel = draw_usdt_info(z, w, addr, priv, mixWord, txs)
                with term.location(0, 1):
                    console.print(draw_system_status_panel, justify="full", soft_wrap=True)
                    console.print(Panel(usdt_info_panel, title="[white]USDT TRC20 Mnemonic Checker V1[/]", style="green"),
                                  justify="full", soft_wrap=True)
                z += 1


if __name__ == "__main__":
    with cf.ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        for _ in range(os.cpu_count()):
            executor.submit(main).result()

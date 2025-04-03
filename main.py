from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from colorama import Fore, Style, init

init(autoreset=True)

def efetuar_login(driver):
    driver.get("https://web.whatsapp.com/")
    print(Fore.YELLOW + "[!] Aguardando o login. Por favor, escaneie o QR Code com seu celular.")
    try:
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, "//div[@id='pane-side']"))
        )
        print(Fore.GREEN + "[✔] Login efetuado com sucesso!")
        return True
    except Exception as e:
        print(Fore.RED + "[X] Erro no login ou tempo de espera excedido:", e)
        return False

def clicar_botao(driver):
    try:
        botao = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div[3]/div/div[3]/header/header/div/span/div/div[1]/button/span"))
        )
        botao.click()
        print(Fore.CYAN + "[✔] Botão clicado com sucesso!")
    except Exception as e:
        print(Fore.RED + "[X] Erro ao tentar clicar no botão:", e)

def limpar_campo(elemento):
    elemento.click()
    time.sleep(0.5)
    elemento.send_keys(Keys.CONTROL, "a")
    elemento.send_keys(Keys.BACKSPACE)

def testar_telefones(driver, lista_arquivo, live_arquivo, die_arquivo, valido_nome_arquivo):
    with open(live_arquivo, "a", encoding="utf-8") as live_file, \
         open(die_arquivo, "a", encoding="utf-8") as die_file, \
         open(valido_nome_arquivo, "a", encoding="utf-8") as valido_nome_file:
        
        with open(lista_arquivo, "r", encoding="utf-8") as f:
            telefones = f.readlines()
        
        for telefone in telefones:
            telefone = telefone.strip()
            if not telefone:
                continue

            print(Fore.YELLOW + f"[!] Testando o telefone: {telefone}")

            try:
                campo_busca = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[3]/div/div[2]/div[1]/span/div/span/div/div[1]/div[2]/div/div/div[1]/p"))
                )
                limpar_campo(campo_busca)
                campo_busca.send_keys(telefone)
                time.sleep(2)

                try:
                    driver.find_element(By.XPATH, "//*[contains(text(), 'Não está na sua lista de contatos')]")
                    try:
                        nome_elemento = driver.find_element(By.XPATH, "//*[starts-with(@title, '~')]")
                        nome = nome_elemento.get_attribute("title").replace("~", "").strip()
                        print(Fore.BLUE + f"[+] LIVE {telefone} - {nome}")
                        valido_nome_file.write(f"{telefone}|{nome}\n")
                    except:
                        print(Fore.GREEN + f"[+] LIVE {telefone} - Sem Nome Encontrado")
                        live_file.write(telefone + "\n")
                except:
                    try:
                        driver.find_element(By.XPATH, "//*[contains(text(), 'Nenhum resultado encontrado para')]")
                        print(Fore.RED + f"[-] DIE {telefone} - Número Inexistente")
                        die_file.write(telefone + "\n")
                    except:
                        print(Fore.YELLOW + f"[!] Telefone {telefone}: Resultado não identificado.")
                
                time.sleep(2)
            except Exception as e:
                print(Fore.RED + f"[X] Erro ao testar o telefone {telefone}: {e}")

def main():
    driver = webdriver.Chrome()
    driver.maximize_window()

    if efetuar_login(driver):
        clicar_botao(driver)
        testar_telefones(driver, "lista_telefone.txt", "live.txt", "die.txt", "valido_nome.txt")
    else:
        print(Fore.RED + "[X] Login não efetuado, encerrando execução.")

    time.sleep(5)
    driver.quit()

if __name__ == "__main__":
    main()

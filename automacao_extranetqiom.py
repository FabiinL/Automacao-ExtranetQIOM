
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService

# bases
DOWNLOAD_DIR = r"C:\Users\usuario\Downloads\relatorios\periodo" 
BASE_URL = "http://urlbase.com.br/exemplo/relatorio.aspx"
TABELAS_BASE = [
    {"codAutos": "XXXX", "codDigito": "X", "codLinha": "XXXX", "dtRef": "1/6/2025", "qtdeVeic": "X", "sufixo_nome": "-A-1"},
    {"codAutos": "YYYY", "codDigito": "Y", "codLinha": "YYYY", "dtRef": "1/6/2025", "qtdeVeic": "Y", "sufixo_nome": "-A-1"},
    {"codAutos": "ZZZZ", "codDigito": "Z", "codLinha": "ZZZZ", "dtRef": "1/6/2025", "qtdeVeic": "Z", "sufixo_nome": "-B-2"},
]

# inicia o navegador
options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": DOWNLOAD_DIR,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
}
options.add_experimental_option("prefs", prefs)
service = ChromeService(executable_path='./chromedriver.exe') # certifique-se que o chromedriver está na mesma pasta que o código

print("Iniciando o navegador...")
try:
    driver = webdriver.Chrome(service=service, options=options)
    print("Navegador iniciado com sucesso.")
except Exception as e:
    print(f"Erro ao iniciar o navegador. Verifique se o chromedriver.exe está na pasta correta e sua versão. Erro: {e}")
    exit()

# construção da URL
def baixar_relatorio_base(cod_Autos, cod_Digito, cod_Linha, dt_Ref, cod_Emp, nm_Emp, qtde_Veic, sufixo_Nome):
    url_completa = (
        f"{BASE_URL}?"
        f"codAutos={cod_Autos}&"
        f"codDigito={cod_Digito}&"
        f"codLinha={cod_Linha}&"
        f"dtRef={dt_Ref}&"
        f"codEmp={cod_Emp}&"
        f"nmEmp={nm_Emp}&"
        f"qtdeVeic={qtde_Veic}"
    )

    print(f"\nTentando baixar relatório do Autos: {cod_Autos}...")
    print(f"Acessando URL: {url_completa}")

# processo de download + rename
    try:
        driver.get(url_completa)
        time.sleep(5) 
        original_filename = "RelatorioBase.pdf"
        downloaded_files = os.listdir(DOWNLOAD_DIR)
        pdf_files = [f for f in downloaded_files if f.endswith('.pdf')]
        latest_pdf = None
        latest_time = 0
        for f in pdf_files:
            file_path = os.path.join(DOWNLOAD_DIR, f)
            if os.path.isfile(file_path):
                mod_time = os.path.getmtime(file_path)
                if mod_time > latest_time:
                    latest_time = mod_time
                    latest_pdf = f
        if latest_pdf:
            old_file_path = os.path.join(DOWNLOAD_DIR, latest_pdf)
            new_filename = f"RelatorioBase{cod_Autos}{sufixo_Nome}.pdf"
            new_file_path = os.path.join(DOWNLOAD_DIR, new_filename)
            os.rename(old_file_path, new_file_path)
            print(f"Arquivo '{latest_pdf}' renomeado para '{new_filename}' com sucesso.")
        else:
            print(f"Aviso: Não foi possível encontrar um novo arquivo PDF para renomear em {DOWNLOAD_DIR}.")
    except Exception as e:
        print(f"Erro ao baixar ou renomear relatório para Autos {cod_Autos}: {e}")

if not os.path.exists(DOWNLOAD_DIR):
    print(f"Criando pasta para download: {DOWNLOAD_DIR}")
    os.makedirs(DOWNLOAD_DIR)

print("\nIniciando o processo de download dos relatórios...")
for relatorio in TABELAS_BASE:
    baixar_relatorio_base(
        cod_autos=relatorio["codAutos"],
        cod_digito=relatorio["codDigito"],
        cod_linha=relatorio["codLinha"],
        dt_ref=relatorio["dtRef"],
        cod_emp="X",
        nm_emp="null",
        qtde_veic=relatorio["qtdeVeic"],
        sufixo_nome=relatorio["sufixo_nome"]
    )

print("\nTodos os downloads tentados. Fechando o navegador...")
driver.quit()
print("Processo concluído.")
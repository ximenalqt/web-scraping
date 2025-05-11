from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time

# URL de la página
url = "https://www.sbs.gob.pe/app/pp/EstadisticasSAEEPortal/Paginas/TIPasivaMercado.aspx?tip=B"

# Inicializa el navegador
options = webdriver.ChromeOptions()

service = Service()
driver = webdriver.Chrome(service=service, options=options)

# Cargar la página
driver.get(url)

# Esperar a que cargue el elemento específico (hasta 15 segundos)
try:
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, "ctl00_cphContent_lblVAL_TIPMN_TASA"))
    )

    # Obtener HTML cargado
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    # Extraer los valores
    tipmn = soup.find("span", id="ctl00_cphContent_lblVAL_TIPMN_TASA").text.strip()
    tipmex = soup.find("span", id="ctl00_cphContent_lblVAL_TIPMEX_TASA").text.strip()

    # Crear DataFrame
    df = pd.DataFrame({
        "Moneda": ["Nacional (TIPMN)", "Extranjera (TIPMEX)"],
        "Tasa (%)": [tipmn, tipmex],
        "Periodo": ["Anual", "Anual"]
    })

    # Guardar en CSV
    df.to_csv("tasas_sbs.csv", index=False, encoding="utf-8-sig")
    print(df)

except Exception as e:
    print("Ocurrió un error:", e)

finally:
    driver.quit()

import json
import csv
import urllib.request
import io
import time
from curl_cffi import requests
from google import genai

print("🤖 Iniciando Radar Eleitoral: Modo Local con Fotos Estáticas...")

CLAVE_SECRETA = "TU_API_KEY_AQUI"
cliente = genai.Client(api_key=CLAVE_SECRETA)

ELEICAO_MAGICA = "20322002026"

url_github_csv = "https://github.com/Drste1n/Radar-electoral/raw/refs/heads/main/consulta_cand_2026_BR.csv"
candidatos_extraidos = []

print("📥 1. Descargando esqueleto de candidatos desde tu GitHub...")

try:
    req = urllib.request.Request(url_github_csv, headers={'User-Agent': 'Mozilla/5.0'})
    respuesta_web = urllib.request.urlopen(req)
    datos_crudos = respuesta_web.read().decode("latin-1")
    
    archivo_virtual = io.StringIO(datos_crudos)
    lector_csv = csv.DictReader(archivo_virtual, delimiter=';')
    
    for fila in lector_csv:
        if fila.get("DS_CARGO", "") == "PRESIDENTE":
            candidatos_extraidos.append({
                "nomeUrna": fila.get("NM_URNA_CANDIDATO", "Desconhecido").title(),
                "partido": fila.get("SG_PARTIDO", "N/A"),
                "numeroUrna": fila.get("NR_CANDIDATO", "00"),
                "sq_candidato": fila.get("SQ_CANDIDATO", "")
            })
    print(f"✅ Se encontraron {len(candidatos_extraidos)} presidentes.")
except Exception as e:
    print(f"⚠️ ERROR procesando tu repositorio: {e}")
    exit()

print("\n🕵️‍♂️ 2. Infiltrando la API del TSE...")
candidatos_finales = []
cabeceras_json = {"Accept": "application/json, text/plain, */*"}

for item in candidatos_extraidos:
    print(f"\n   ⏳ Extrayendo datos reales de: {item['nomeUrna']}...")
    
    patrimonio = "Não declarado"
    vicepresidente = "Aguardando registro"
    profesion = "Não informada"
    coligacao = "Sem coligação"
    composicao_coligacao = "Sem detalhes"
    situacion = "Aguardando"
    genero = "Não informado"
    raza = "Não informada"
    estado_civil = "Não informado"
    instruccion = "Não informada"
    limite_gastos = "Não declarado"
    redes_sociales = "Nenhuma"
    
    if item['sq_candidato']:
        try:
            url_api = f"https://divulgacandcontas.tse.jus.br/divulga/rest/v1/candidatura/buscar/2026/BR/{ELEICAO_MAGICA}/candidato/{item['sq_candidato']}"
            resp_api = requests.get(url_api, headers=cabeceras_json, impersonate="chrome110", timeout=15)
            
            if resp_api.status_code == 200 and "{" in resp_api.text:
                print("      ✅ ¡Datos encontrados en el TSE!")
                datos = resp_api.json()
                
                if 'totalDeBens' in datos and datos['totalDeBens']:
                    patrimonio = f"R$ {float(datos['totalDeBens']):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                
                if 'ocupacao' in datos and isinstance(datos['ocupacao'], str):
                    profesion = datos['ocupacao'].title()
                elif isinstance(datos.get('ocupacao'), dict):
                    profesion = datos['ocupacao'].get('descricao', 'Não informada').title()
                    
                if 'nomeColigacao' in datos and datos['nomeColigacao']:
                    coligacao = str(datos['nomeColigacao']).title()
                    
                if 'composicaoColigacao' in datos and datos['composicaoColigacao']:
                    composicao_coligacao = str(datos['composicaoColigacao'])
                    
                if 'descricaoSituacao' in datos and datos['descricaoSituacao']:
                    situacion = str(datos['descricaoSituacao']).title()
                    
                if 'descricaoSexo' in datos and datos['descricaoSexo']:
                    genero = str(datos['descricaoSexo']).title()
                    
                if 'descricaoCorRaca' in datos and datos['descricaoCorRaca']:
                    raza = str(datos['descricaoCorRaca']).title()
                    
                if 'descricaoEstadoCivil' in datos and datos['descricaoEstadoCivil']:
                    estado_civil = str(datos['descricaoEstadoCivil']).title()
                    
                if 'grauInstrucao' in datos and datos['grauInstrucao']:
                    instruccion = str(datos['grauInstrucao']).title()
                    
                if 'gastoCampanha1T' in datos and datos['gastoCampanha1T']:
                    limite_gastos = f"R$ {float(datos['gastoCampanha1T']):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                
                if 'sites' in datos and datos['sites']:
                    redes = ", ".join([red.get('url', '') for red in datos['sites'] if isinstance(red, dict)])
                    redes_sociales = redes if redes else "Nenhuma"
                
                if 'vices' in datos and isinstance(datos['vices'], list):
                    for vice in datos['vices']:
                        if isinstance(vice, dict):
                            vicepresidente = vice.get('nm_CANDIDATO', vicepresidente).title()
            else:
                print("      ❌ Sin datos públicos aún.")
                
        except Exception as e:
            print(f"      ⚠️ Falla de conexión interna: {e}")

    # 4. INTELIGENCIA ARTIFICIAL (Propuestas)
    prompt = f"""
    Enumera 3 propuestas principales de la plataforma política e histórico del candidato presidencial de Brasil {item['nomeUrna']} del partido {item['partido']}.
    Escribe SOLO 3 viñetas cortas en português.
    """

    resumen_ia = "• Propostas detalhadas no TSE."
    intentos = 0
    
    while intentos < 3:
        try:
            respuesta = cliente.models.generate_content(model='gemini-3.1-flash-lite', contents=prompt)
            resumen_ia = respuesta.text.strip()
            break 
        except Exception:
            time.sleep(4)
            intentos += 1
                
    texto_detalles_extra = (
        f"Coligação: {coligacao} ({composicao_coligacao})\n"
        f"Perfil: {genero}, {raza}, {estado_civil}\n"
        f"Escolaridade: {instruccion}\n"
        f"Limite de Gastos: {limite_gastos}\n"
        f"Sites: {redes_sociales}"
    )

    # ASIGNACIÓN DE FOTO LOCAL (Ej: /images/candidatos/lula.jpg)
    # Reemplaza espacios por guiones bajos para que coincida con el nombre de tu archivo
    nombre_archivo_foto = item["nomeUrna"].lower().replace(" ", "_")

    candidatos_finales.append({
        "nomeUrna": item["nomeUrna"],
        "partido": {"sigla": item["partido"]},
        "numeroUrna": item["numeroUrna"],
        "profesion": profesion,
        "patrimonio": patrimonio,
        "situacionLegal": situacion,
        "vicepresidente": vicepresidente,
        "fotoUrl": f"/images/candidatos/{nombre_archivo_foto}.jpg",
        "pdfPlanGobiernoUrl": f"https://divulgacandcontas.tse.jus.br/divulga/#/candidato/2026/{ELEICAO_MAGICA}/BR/{item['sq_candidato']}",
        "resumenPropuestas": resumen_ia,
        "propuestas": texto_detalles_extra
    })
    
    time.sleep(2)

with open("src/main/resources/dados-tse.json", "w", encoding="utf-8") as f:
    json.dump({"candidatos": candidatos_finales}, f, indent=4, ensure_ascii=False)

print("\n🎉 ¡LISTO! JSON generado apuntando a tus fotos locales en /images/candidatos/.")
import requests
import zipfile
import io

URL = "https://cdn.tse.jus.br/estatistica/sead/odsele/consulta_cand/consulta_cand_2026.zip"

print("🔎 Descargando dataset oficial de candidatos 2026...")
print("🔗", URL)

try:
    # Descargar el ZIP
    resp = requests.get(URL, timeout=60)
    resp.raise_for_status()

    # Abrir el ZIP en memoria
    with zipfile.ZipFile(io.BytesIO(resp.content)) as z:
        # Listar archivos dentro del ZIP
        print("\n📦 Archivos encontrados en el ZIP:")
        for name in z.namelist():
            print("-", name)

        # Extraer el CSV principal
        csv_name = [n for n in z.namelist() if n.endswith(".csv")][0]
        print("\n✅ Extrayendo:", csv_name)

        with z.open(csv_name) as f:
            data = f.read().decode("latin1")  # CSV está en codificación latin1
            # Guardar en disco
            with open("candidatos_2026.csv", "w", encoding="utf-8") as out:
                out.write(data)

        print("\n🎉 Archivo guardado como candidatos_2026.csv")

except Exception as erro:
    print("\n❌ Error:", type(erro).__name__, erro)


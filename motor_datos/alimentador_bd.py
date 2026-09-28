import os
os.environ["PGCLIENTENCODING"] = "utf-8"

import zipfile
import csv
import io
import psycopg2
import shutil
import json
from collections import defaultdict

DIRECTORIO_SCRIPT = os.path.dirname(os.path.abspath(__file__))

def buscar_zip(prefijo):
    for f in os.listdir(DIRECTORIO_SCRIPT):
        if f.lower().startswith(prefijo.lower()) and f.lower().endswith('.zip'):
            return os.path.join(DIRECTORIO_SCRIPT, f)
    return None

Z_CAND = buscar_zip("consulta_cand")
Z_BENS = buscar_zip("bem_candidato")
Z_REDE = buscar_zip("rede_social")
Z_CONTAS = buscar_zip("prestacao_de_contas")
Z_PROPOSTAS = buscar_zip("proposta_governo")

DIR_PDFS_JAVA = os.path.abspath(os.path.join(DIRECTORIO_SCRIPT, "..", "src", "main", "resources", "static", "pdfs"))

DB_HOST = "localhost"
DB_NAME = "radar_electoral"
DB_USER = "postgres"
DB_PASS = "admin123"

print("🚀 Iniciando Super Alimentador Definitivo (Con Datos Jurídicos Reales)...")
if not Z_CAND or not Z_CONTAS:
    print("❌ ERROR: Faltan archivos ZIP indispensables en la carpeta motor_datos.")
    exit()

candidatos_maestro = {}
vices_temp = {}

# ==========================================
# FASE 1: CANDIDATOS, VICE Y SITUACIÓN LEGAL
# ==========================================
print(f"📦 [1/6] Leyendo candidatos y extrayendo metadatos jurídicos...")
with zipfile.ZipFile(Z_CAND, 'r') as z:
    archivos_csv = [a for a in z.namelist() if a.endswith('.csv')]
    archivo_brasil = next((a for a in archivos_csv if 'BRASIL' in a.upper()), None)
    archivos_a_procesar = [archivo_brasil] if archivo_brasil else archivos_csv

    for arch in archivos_a_procesar:
        with z.open(arch) as f:
            lector = csv.DictReader(io.TextIOWrapper(f, encoding='latin-1'), delimiter=';')
            for fila in lector:
                cargo_csv = fila.get('DS_CARGO', '').strip().upper()
                numero_urna = int(fila.get('NR_CANDIDATO', '0'))

                if cargo_csv in ['PRESIDENTE', 'VICE-PRESIDENTE']:
                    sq = fila.get('SQ_CANDIDATO', '')
                    coligacao = fila.get('NM_COLIGACAO', 'Sem coligação')
                    composicao = fila.get('DS_COMPOSICAO_COLIGACAO', '')
                    
                    # 1. LIMPIEZA DEL ESTADO LEGAL
                    situacao_bruta = (fila.get('DS_SIT_TOT_TURNO', '') or fila.get('DS_DETALHE_SITUACAO_CAND', '') or fila.get('DS_SITUACAO_CANDIDATURA', '')).strip().upper()
                    if situacao_bruta in ['#NULO#', '#NULO', '#NE#', '', 'NAN']:
                        situacao_limpia = 'AGUARDANDO JULGAMENTO'
                    else:
                        situacao_limpia = situacao_bruta

                    # 2. NUEVO: EXTRACCIÓN DEL NÚMERO DE PROCESO Y MOTIVO
                    numero_processo = fila.get('NR_PROCESSO', 'Não informado').strip()
                    motivo_bruto = fila.get('DS_MOTIVO_SITUACAO_CAND', '') or fila.get('DS_MOTIVO_INDEFERIMENTO', '') or fila.get('DS_MOTIVO_CASSACAO', '')
                    if not motivo_bruto or motivo_bruto in ['#NULO#', '#NULO', '-1']:
                        motivo_situacao = "Análise concluída ou sem ocorrências registradas"
                    else:
                        motivo_situacao = motivo_bruto.strip().capitalize()

                    # 3. ENLACE DE CERTIDÕES
                    ano_e = str(fila.get('ANO_ELEICAO', '2024')).strip()
                    cd_e = str(fila.get('CD_ELEICAO', '')).strip()
                    sg_uf = str(fila.get('SG_UF', 'BR')).strip().upper()
                    url_certidoes = f"https://divulgacandcontas.tse.jus.br/divulga/#/candidato/{ano_e}/{cd_e}/{sg_uf}/{sq}" if cd_e else ""
                    
                    gasto_bruto = fila.get('VR_DESPESA_MAX_CAMPANHA', '0')
                    if not gasto_bruto or gasto_bruto in ['-1', '-1.00']: gasto_bruto = '0'
                    gasto_limpio = gasto_bruto.replace('.', '').replace(',', '.')
                    try:
                        gasto_max_float = float(gasto_limpio)
                        if gasto_max_float == 0.0: gasto_max_float = 88944030.80 
                    except:
                        gasto_max_float = 0.0
                    
                    candidatos_maestro[sq] = {
                        'nome': fila.get('NM_CANDIDATO', '').title(),
                        'nome_urna': fila.get('NM_URNA_CANDIDATO', '').title(),
                        'numero': numero_urna,
                        'cargo': cargo_csv,
                        'situacao': situacao_limpia,
                        'numero_processo': numero_processo,
                        'motivo_situacao': motivo_situacao,
                        'partido_sigla': fila.get('SG_PARTIDO', ''),
                        'profesion': fila.get('DS_OCUPACAO', 'Não informada').title(),
                        'patrimonio_total': 0.0,
                        'lista_bienes': [],
                        'redes': [],
                        'detalles_alianza': f"Coligação: {coligacao}\nPartidos: {composicao}",
                        'vicepresidente': 'A definir' if cargo_csv == 'PRESIDENTE' else '',
                        'sq_candidato_vice': None, 
                        'pdf_url': '',
                        'pdf_certidoes_url': url_certidoes,
                        'grau_instrucao': fila.get('DS_GRAU_INSTRUCAO', 'Não informado').title(),
                        'estado_civil': fila.get('DS_ESTADO_CIVIL', 'Não informado').title(),
                        'ocupacao': fila.get('DS_OCUPACAO', 'Não informada').title(),
                        'cor_raca': fila.get('DS_COR_RACA', 'Não informada').title(),
                        'despesa_maxima': gasto_max_float,
                        'receitas_dict': defaultdict(float),
                        'receitas_nomes': {}, 
                        'fornecedores_dict': defaultdict(float),
                        'fornecedores_nomes': {}, 
                        'despesas_dict': defaultdict(float),
                        'total_receitas': 0.0,
                        'total_despesas': 0.0,
                        'top_doadores': '[]',
                        'top_fornecedores': '[]',
                        'top_despesas': '[]'
                    }

                    if cargo_csv == 'VICE-PRESIDENTE':
                        vices_temp[numero_urna] = {'nome_urna': fila.get('NM_URNA_CANDIDATO', '').title(), 'sq': sq}

for sq, datos in candidatos_maestro.items():
    if datos['cargo'] == 'PRESIDENTE':
        num = datos['numero']
        if num in vices_temp:
            datos['vicepresidente'] = vices_temp[num]['nome_urna']
            datos['sq_candidato_vice'] = vices_temp[num]['sq'] 

# ==========================================
# FASES 2 A 5 SE MANTIENEN IGUAL
# ==========================================
print(f"💰 [2/6] Extrayendo desglose de bienes...")
bienes_procesados = set()
if Z_BENS and os.path.exists(Z_BENS):
    with zipfile.ZipFile(Z_BENS, 'r') as z:
        archivos_csv = [a for a in z.namelist() if a.endswith('.csv')]
        archivo_brasil = next((a for a in archivos_csv if 'BRASIL' in a.upper()), None)
        for arch in ([archivo_brasil] if archivo_brasil else archivos_csv):
            with z.open(arch) as f:
                lector = csv.DictReader(io.TextIOWrapper(f, encoding='latin-1'), delimiter=';')
                for fila in lector:
                    sq = fila.get('SQ_CANDIDATO', '')
                    if sq in candidatos_maestro:
                        tipo_bien, valor_str = fila.get('DS_BEM_CANDIDATO', 'Bem declarado').title(), fila.get('VR_BEM_CANDIDATO', '0').replace(',', '.')
                        id_bien = fila.get('NR_ORDEM_BEM', tipo_bien)
                        huella = f"{sq}_{id_bien}_{valor_str}"
                        if huella not in bienes_procesados:
                            bienes_procesados.add(huella)
                            try:
                                valor_float = float(valor_str)
                                if valor_float > 0:
                                    candidatos_maestro[sq]['patrimonio_total'] += valor_float
                                    candidatos_maestro[sq]['lista_bienes'].append(f"- {tipo_bien}: R$ {f'{valor_float:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')}")
                            except: pass

print(f"📱 [3/6] Extrayendo redes sociales...")
if Z_REDE and os.path.exists(Z_REDE):
    with zipfile.ZipFile(Z_REDE, 'r') as z:
        for arch in [a for a in z.namelist() if a.endswith('.csv')]:
            with z.open(arch) as f:
                for fila in csv.DictReader(io.TextIOWrapper(f, encoding='latin-1'), delimiter=';'):
                    if fila.get('SQ_CANDIDATO', '') in candidatos_maestro and fila.get('DS_URL'):
                        candidatos_maestro[fila['SQ_CANDIDATO']]['redes'].append(fila.get('DS_URL'))

print(f"📄 [4/6] Extrayendo Planes de Governo...")
if Z_PROPOSTAS and os.path.exists(Z_PROPOSTAS):
    os.makedirs(DIR_PDFS_JAVA, exist_ok=True) 
    try:
        with zipfile.ZipFile(Z_PROPOSTAS, 'r') as z:
            pdfs = [a for a in z.namelist() if a.lower().endswith('.pdf')]
            for sq in candidatos_maestro:
                if candidatos_maestro[sq]['cargo'] == 'PRESIDENTE': 
                    pdf_cand = sorted([a for a in pdfs if str(sq) in a])
                    if pdf_cand:
                        with z.open(pdf_cand[0]) as origen, open(os.path.join(DIR_PDFS_JAVA, f"plan_{sq}.pdf"), 'wb') as destino:
                            shutil.copyfileobj(origen, destino)
                        candidatos_maestro[sq]['pdf_url'] = f"/pdfs/plan_{sq}.pdf"
    except: pass

print(f"🕵️  [5/6] Analizando recibos y facturas...")
with zipfile.ZipFile(Z_CONTAS, 'r') as z:
    for arch in [a for a in z.namelist() if a.endswith('.csv')]:
        with z.open(arch) as f:
            lector = csv.DictReader(io.TextIOWrapper(f, encoding='latin-1'), delimiter=';')
            for fila in lector:
                sq = fila.get('SQ_CANDIDATO', '')
                if sq in candidatos_maestro:
                    if 'receitas' in arch.lower():
                        try:
                            valor = float(fila.get('VR_RECEITA', '0').strip().replace('.', '').replace(',', '.'))
                            if valor > 0:
                                doc = fila.get('NR_CPF_CNPJ_DOADOR', '').strip() or fila.get('NM_DOADOR', 'Desconhecido').strip()
                                candidatos_maestro[sq]['receitas_dict'][doc] += valor
                                candidatos_maestro[sq]['receitas_nomes'][doc] = fila.get('NM_DOADOR', 'Desconhecido').strip()
                                candidatos_maestro[sq]['total_receitas'] += valor
                        except: pass
                    elif 'despesas' in arch.lower():
                        try:
                            valor = float(fila.get('VR_DESPESA_CONTRATADA', '0').strip().replace('.', '').replace(',', '.'))
                            if valor > 0:
                                forn, doc = fila.get('NM_FORNECEDOR', 'Desconhecido').strip(), fila.get('NR_CPF_CNPJ_FORNECEDOR', '').strip()
                                tipo = fila.get('DS_TIPO_DESPESA', '').strip() or fila.get('DS_DESPESA', 'Outros').strip()
                                candidatos_maestro[sq]['fornecedores_dict'][doc or forn] += valor
                                candidatos_maestro[sq]['fornecedores_nomes'][doc or forn] = forn
                                candidatos_maestro[sq]['despesas_dict'][tipo] += valor
                                candidatos_maestro[sq]['total_despesas'] += valor
                        except: pass

for sq, datos in candidatos_maestro.items():
    if datos['total_receitas'] > 0:
        candidatos_maestro[sq]['top_doadores'] = json.dumps([{"nome": datos['receitas_nomes'][d], "documento": d, "valor": float(v), "porcentaje": float(round((v / datos['total_receitas']) * 100, 2))} for d, v in sorted(datos['receitas_dict'].items(), key=lambda x: x[1], reverse=True)[:5]])
    if datos['total_despesas'] > 0:
        candidatos_maestro[sq]['top_fornecedores'] = json.dumps([{"nome": datos['fornecedores_nomes'][d], "documento": d, "valor": float(v), "porcentaje": float(round((v / datos['total_despesas']) * 100, 2))} for d, v in sorted(datos['fornecedores_dict'].items(), key=lambda x: x[1], reverse=True)[:5]])
        candidatos_maestro[sq]['top_despesas'] = json.dumps([{"tipo": k, "valor": float(v), "porcentaje": float(round((v / datos['total_despesas']) * 100, 2))} for k, v in sorted(datos['despesas_dict'].items(), key=lambda x: x[1], reverse=True)[:5]])

# ==========================================
# FASE 6: INYECCIÓN SEGURA EN POSTGRESQL
# ==========================================
print(f"🔌 [6/6] Inyectando datos en PostgreSQL...")
try:
    conexion = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
    cursor = conexion.cursor()

    # NUEVAS COLUMNAS JURÍDICAS
    cursor.execute("ALTER TABLE candidatos ADD COLUMN IF NOT EXISTS numero_processo VARCHAR(100);")
    cursor.execute("ALTER TABLE candidatos ADD COLUMN IF NOT EXISTS motivo_situacao TEXT;")
    conexion.commit()

    for sq, datos in candidatos_maestro.items():
        pat_fmt = f"{datos['patrimonio_total']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        bienes_str = "\n".join(datos['lista_bienes']) if datos['lista_bienes'] else "Nenhum bem detalhado."
        foto_url = f"/images/candidatos/{datos['nome_urna'].lower().replace(' ', '_')}.jpg"

        consulta_sql = """
            INSERT INTO candidatos 
            (sq_candidato, nome, nome_urna, numero, cargo, situacao, profesion, patrimonio, vicepresidente, partido_sigla, propuestas_detalles, foto_url, redes_sociales, bienes_detalles, pdf_plan_gobierno_url, pdf_certidoes_url, grau_instrucao, estado_civil, ocupacao, cor_raca, despesa_maxima, top_despesas, top_doadores, top_fornecedores, total_receitas, total_despesas, sq_candidato_vice, numero_processo, motivo_situacao, atualizado_em)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
            ON CONFLICT (sq_candidato) 
            DO UPDATE SET 
                nome = EXCLUDED.nome, nome_urna = EXCLUDED.nome_urna, numero = EXCLUDED.numero, cargo = EXCLUDED.cargo, situacao = EXCLUDED.situacao,
                profesion = EXCLUDED.profesion, patrimonio = EXCLUDED.patrimonio, vicepresidente = EXCLUDED.vicepresidente,
                partido_sigla = EXCLUDED.partido_sigla, propuestas_detalles = EXCLUDED.propuestas_detalles, foto_url = EXCLUDED.foto_url,
                redes_sociales = EXCLUDED.redes_sociales, bienes_detalles = EXCLUDED.bienes_detalles, pdf_plan_gobierno_url = EXCLUDED.pdf_plan_gobierno_url, pdf_certidoes_url = EXCLUDED.pdf_certidoes_url,
                grau_instrucao = EXCLUDED.grau_instrucao, estado_civil = EXCLUDED.estado_civil, ocupacao = EXCLUDED.ocupacao,
                cor_raca = EXCLUDED.cor_raca, despesa_maxima = EXCLUDED.despesa_maxima, top_despesas = EXCLUDED.top_despesas,
                top_doadores = EXCLUDED.top_doadores, top_fornecedores = EXCLUDED.top_fornecedores, 
                total_receitas = EXCLUDED.total_receitas, total_despesas = EXCLUDED.total_despesas,
                sq_candidato_vice = EXCLUDED.sq_candidato_vice, numero_processo = EXCLUDED.numero_processo, motivo_situacao = EXCLUDED.motivo_situacao, atualizado_em = CURRENT_TIMESTAMP;
        """
        cursor.execute(consulta_sql, (
            sq, datos['nome'], datos['nome_urna'], datos['numero'], datos['cargo'], datos['situacao'], datos['profesion'], 
            pat_fmt, datos['vicepresidente'], datos['partido_sigla'], datos['detalles_alianza'], foto_url, ",".join(datos['redes']), 
            bienes_str, datos['pdf_url'], datos['pdf_certidoes_url'], datos['grau_instrucao'], datos['estado_civil'], datos['ocupacao'], datos['cor_raca'], 
            datos['despesa_maxima'], datos['top_despesas'], datos['top_doadores'], datos['top_fornecedores'],
            datos['total_receitas'], datos['total_despesas'], datos['sq_candidato_vice'], datos['numero_processo'], datos['motivo_situacao']
        ))

    conexion.commit()
    print(f"\n🎉 ¡ÉXITO! Base de datos enriquecida con metadatos judiciales reales.")

except Exception as e:
    print(f"\n⚠️ ERROR POSTGRESQL: {e}")
finally:
    if 'conexion' in locals() and conexion:
        cursor.close()
        conexion.close()
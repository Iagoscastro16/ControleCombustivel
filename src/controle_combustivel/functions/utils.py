from datetime import datetime

def normalizar_data(entrada):
    limpo = entrada.replace("/","").strip()
    if not limpo.isdigit() or len(limpo) != 6:
        return None
    
    dia = limpo[0:2]
    mes = limpo[2:4]
    ano = "20" + limpo[4:6]

    try:
        data = datetime.strptime(f"{dia}/{mes}/{ano}", "%d/%m/%Y")
        return data.strftime("%Y-%m-%d")
    except ValueError:
        return None
    
def calcular_av(total_veiculo, total_geral):
    if total_geral == 0:
        return 0
    return (total_veiculo / total_geral) * 100

def calcular_ah(atual,anterior):
    if anterior == 0:
        return 0
    return (atual / anterior - 1) * 100
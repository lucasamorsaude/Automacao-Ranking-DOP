import os
from datetime import datetime

# 1. DADOS MOCK (com a estrutura de 6 colunas)
dados_unidades = [
    {'unidade': 'Araucária', 'conf_9h': '10,00%', 'conf_12h': '--', 'evol_conf': '--', 'ocup_9h': '52,63%', 'ocup_12h': '--', 'evol_ocup': '--'},
    {'unidade': 'Colombo', 'conf_9h': '69,07%', 'conf_12h': '--', 'evol_conf': '--', 'ocup_9h': '55,11%', 'ocup_12h': '--', 'evol_ocup': '--'},
    {'unidade': 'Curitiba Pinheirinho', 'conf_9h': '4,73%', 'conf_12h': '--', 'evol_conf': '--', 'ocup_9h': '73,16%', 'ocup_12h': '--', 'evol_ocup': '--'},
    {'unidade': 'Foz do Iguaçu', 'conf_9h': '6,42%', 'conf_12h': '--', 'evol_conf': '--', 'ocup_9h': '65,85%', 'ocup_12h': '--', 'evol_ocup': '--'},
    {'unidade': 'Francisco Beltrão', 'conf_9h': '18,75%', 'conf_12h': '--', 'evol_conf': '--', 'ocup_9h': '43,24%', 'ocup_12h': '--', 'evol_ocup': '--'},
    {'unidade': 'Montenegro', 'conf_9h': '3,57%', 'conf_12h': '--', 'evol_conf': '--', 'ocup_9h': '43,75%', 'ocup_12h': '--', 'evol_ocup': '--'},
    {'unidade': 'São João Del Rei', 'conf_9h': '20,83%', 'conf_12h': '--', 'evol_conf': '--', 'ocup_9h': '68,57%', 'ocup_12h': '--', 'evol_ocup': '--'}
]
totais = {'conf_9h': '17,45%', 'conf_12h': '--', 'evol_conf': '--', 'ocup_9h': '61,70%', 'ocup_12h': '--', 'evol_ocup': '--'}

# 2. FUNÇÃO DE LÓGICA PARA AS CORES
def get_cor_class(valor_str):
    if not valor_str or valor_str == '--': return 'celula-vazia'
    try:
        valor = float(valor_str.replace('%', '').replace(',', '.'))
        if valor < 60: return 'cor-vermelho'
        if valor < 70: return 'cor-amarelo'
        return 'cor-verde'
    except (ValueError, TypeError):
        return 'celula-vazia'

# 3. PREPARAÇÃO DOS DADOS
hoje = datetime.now().strftime('%d/%m')

# 4. TEMPLATE HTML FINAL
html_final = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Ranking DOP</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500;700;800&display=swap" rel="stylesheet">
    <style>
        body {{
            font-family: 'Montserrat', sans-serif; background-color: #002060; color: white;
            padding: 40px; margin: 0; width: 1080px; box-sizing: border-box;
            display: flex; flex-direction: column;
        }}
        header {{
            display: flex; align-items: center; margin-bottom: 20px;
        }}
        header img {{ width: 120px; }}
        header h1 {{ font-size: 32px; font-weight: 800; text-align: center; flex-grow: 1; margin: 0; }}

        .grid-container {{ display: flex; flex-direction: column; gap: 8px; }}
        .grid-row, .grid-header, .grid-footer {{ display: flex; gap: 8px; align-items: stretch; text-align: center; }}
        .grid-cell {{
            padding: 12px 5px; border-radius: 8px; display: flex;
            align-items: center; justify-content: center; font-weight: 700; font-size: 14px;
        }}
        
        /* ESTRUTURA DAS COLUNAS (A CHAVE DO ALINHAMENTO) */
        .grid-cell.unidade {{
            flex: 0 0 25%; /* Largura fixa para a coluna de unidades */
            background-color: #0c3877;
            justify-content: flex-start;
            padding-left: 15px;
        }}
        .data-cells {{
            flex: 1; /* Ocupa o resto do espaço */
            display: flex;
            gap: 8px;
        }}
        .data-cells .grid-cell {{
            flex: 1; /* Células de dados dividem o espaço igualmente */
        }}
        
        .grid-header .grid-cell {{ background-color: #0c3877; font-weight: 500; font-size: 13px;}}
        
        /* CORREÇÃO DO RODAPÉ */
        .grid-footer .grid-cell {{
            background-color: #737373; /* Cinza escuro para todas as células do rodapé */
            color: #000; /* Cor de texto suave */
        }}

        .grid-footer .grid-cell.unidade {{ background-color: #0c3877; font-weight: 700; font-size: 14px; color: #fff; }}
        
        /* Cores de status das linhas de dados */
        .cor-vermelho {{ background-color: #ea9999; color: #000; }}
        .cor-amarelo {{ background-color: #ffe599; color: #000; }}
        .cor-verde {{ background-color: #b6d7a8; color: #000; }}
        .celula-vazia {{ background-color: #fff; color: #000; }} /* Cor cinza claro para células vazias */
        
        footer {{ margin-top: auto; padding-top: 20px; }}
        .legenda-titulo {{ font-weight: 700; font-size: 18px; }}
    </style>
</head>
<body>
<div class="container">
    <header>
        <img src="https://cdn.jsdelivr.net/gh/lucasamorsaude/Automacao-Ranking-DOP/logo-dop.png" alt="Logo DOP">
        <h1>🩺 % Confirmação Medicina | {hoje}</h1>
    </header>
    
    <main>
        <div class="grid-container">
            <div class="grid-header">
                <div class="grid-cell unidade">Unidades</div>
                <div class="data-cells">
                    <div class="grid-cell">Confirmação (%) até 9h</div>
                    <div class="grid-cell">Confirmação (%) até 12h</div>
                    <div class="grid-cell">(%) Evolução confirmação</div>
                    <div class="grid-cell">Ocupação (%) até 09h</div>
                    <div class="grid-cell">Ocupação (%) até 12h</div>
                    <div class="grid-cell">(%) Evolução ocupação</div>
                </div>
            </div>

            {''.join([f"""
            <div class="grid-row">
                <div class="grid-cell unidade">{item['unidade']}</div>
                <div class="data-cells">
                    <div class="grid-cell {get_cor_class(item['conf_9h'])}">{item['conf_9h']}</div>
                    <div class="grid-cell {get_cor_class(item['conf_12h'])}">{item['conf_12h']}</div>
                    <div class="grid-cell celula-vazia">{item['evol_conf']}</div>
                    <div class="grid-cell {get_cor_class(item['ocup_9h'])}">{item['ocup_9h']}</div>
                    <div class="grid-cell {get_cor_class(item['ocup_12h'])}">{item['ocup_12h']}</div>
                    <div class="grid-cell celula-vazia">{item['evol_ocup']}</div>
                </div>
            </div>
            """ for item in dados_unidades])}

            <div class="grid-footer">
                <div class="grid-cell unidade">TOTAL DOP</div>
                <div class="data-cells">
                    <div class="grid-cell">{totais['conf_9h']}</div>
                    <div class="grid-cell">{totais['conf_12h']}</div>
                    <div class="grid-cell">{totais['evol_conf']}</div>
                    <div class="grid-cell">{totais['ocup_9h']}</div>
                    <div class="grid-cell">{totais['ocup_12h']}</div>
                    <div class="grid-cell">{totais['evol_ocup']}</div>
                </div>
            </div>
        </div>
    </main>

    <footer >
        <div class="legenda-titulo"><br>Meta de confirmação mínima entre 95% e 100%</div>
    </footer>
</div>
</body>
</html>
"""

# 5. SALVA O ARQUIVO HTML
nome_arquivo = "confirmacao_med.html"
with open(nome_arquivo, "w", encoding="utf-8") as f:
    f.write(html_final)

print(f"Arquivo '{nome_arquivo}' gerado com sucesso!")
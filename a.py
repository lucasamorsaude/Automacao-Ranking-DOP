import asyncio
from playwright.async_api import async_playwright
import jinja2
import os

# --- DADOS DE EXEMPLO (Os mesmos de antes) ---
dados_ranking = [
    {'unidade': 'Araucária', 'contratado': 'R$ 0,00', 'cadastros': 7, 'simulacoes': 51, 'unicas': 15, 'cor': 'zona-de-perigo'},
    {'unidade': 'Colombo', 'contratado': 'R$ 3.566,00', 'cadastros': 4, 'simulacoes': 44, 'unicas': 8, 'cor': 'meta-amarela'},
    {'unidade': 'Curitiba Pinheirinho', 'contratado': 'R$ 3.052,25', 'cadastros': 10, 'simulacoes': 185, 'unicas': 18, 'cor': 'meta-verde'},
    {'unidade': 'Foz do Iguaçu', 'contratado': 'R$ 0,00', 'cadastros': 8, 'simulacoes': 5, 'unicas': 4, 'cor': 'zona-de-perigo'},
    {'unidade': 'Francisco Beltrão', 'contratado': 'R$ 0,00', 'cadastros': 4, 'simulacoes': 26, 'unicas': 7, 'cor': 'zona-de-perigo'},
    {'unidade': 'Montenegro', 'contratado': 'R$ 0,00', 'cadastros': 6, 'simulacoes': 0, 'unicas': 0, 'cor': 'zona-de-perigo'},
    {'unidade': 'SJDR', 'contratado': 'R$ 0,00', 'cadastros': 11, 'simulacoes': 61, 'unicas': 11, 'cor': 'zona-de-perigo'},
]
total_dop = {'contratado': 'R$ 6.618,25', 'cadastros': 50, 'simulacoes': 372, 'unicas': 63}
# --------------------------------------------------------------------

async def gerar_imagem():
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    
    # 1. Renderiza o template com Jinja2 (exatamente como antes)
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(diretorio_atual))
    template = env.get_template('template.html')
    html_final = template.render(ranking=dados_ranking, totais=total_dop)

    caminho_html = os.path.join(diretorio_atual, 'ranking_para_imagem.html')
    with open(caminho_html, 'w', encoding='utf-8') as f:
        f.write(html_final)

    # 2. Usa o Playwright para tirar a foto
    print("Iniciando o Playwright para gerar a imagem...")
    caminho_imagem = os.path.join(diretorio_atual, 'ranking_final_playwright.png')
    
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            
            # Define o tamanho da "janela" do navegador para ser idêntico ao da imagem
            await page.set_viewport_size({"width": 1080, "height": 840})
            
            # Abre o arquivo HTML local
            await page.goto(f"file://{caminho_html}")
            
            # IMPORTANTE: Espera a fonte do Google Fonts carregar da internet
            await page.wait_for_load_state('networkidle')
            
            # Tira a screenshot
            await page.screenshot(path=caminho_imagem)
            
            await browser.close()
        print(f"Sucesso! Imagem salva em: {caminho_imagem}")

    except Exception as e:
        print(f"Ocorreu um erro com o Playwright: {e}")
    finally:
        # Limpa o arquivo HTML temporário
        os.remove(caminho_html)
        print("Arquivo HTML temporário removido.")


# Executa a função assíncrona
if __name__ == "__main__":
    asyncio.run(gerar_imagem())
from flask import Flask, render_template, request, redirect, url_for, flash,send_from_directory
import os
from codigo import validar_colunas
import pandas as pd

app = Flask(__name__)
app.secret_key = 'supersecretkey'

#iniciando flag junto com o servidor
with open("server_on.flag", "w") as f:
    f.write("on")

#local onde salva os arquivos enviados
PASTA_UPLOAD = "arquivos/brutos"
app.config['PASTA_UPLOAD'] = PASTA_UPLOAD

EXTENSOES_PERMITIDAS = {'xlsx','csv','json'}

def  arquivo_permitido(nome_do_arquivo):
    if "." in nome_do_arquivo and nome_do_arquivo.rsplit(".", 1)[1].lower() in EXTENSOES_PERMITIDAS:
        return True
    else:
        return False
    
# status para o servidor ser validado
@app.route('/status')
def status():
    return "on"
# Home
@app.route('/')
def home():
    return render_template('index.html')

# Upload
@app.route('/upload', methods=['GET', 'POST'])
def upload_arquivos():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash("Nenhum arquivo selecionado","warning")
            return redirect(request.url)

        arquivos = request.files.getlist('file')  # Pega todos os arquivos

        # Verifica se o envio esta vazio
        if not arquivos or arquivos[0].filename == '':
            flash("Nenhum arquivo selecionado","warning")
            return redirect(request.url)

        for arquivo in arquivos:
            if arquivo and arquivo_permitido(arquivo.filename):
                nome_arquivo = arquivo.filename
                caminho_completo = os.path.join(app.config['PASTA_UPLOAD'], nome_arquivo)
                
                extensao = nome_arquivo.rsplit('.', 1)[1].lower()

                try:
                    if extensao == 'xlsx':
                        df = pd.read_excel(arquivo)
                    elif extensao == 'csv':
                        df = pd.read_csv(arquivo)
                    elif extensao == 'json':
                        df = pd.read_json(arquivo)
                    else:
                        flash(f"Formato {extensao} não suportado.","error")
                        continue

                    if validar_colunas(df):
                        try:
                            df['CPF'] = df['CPF'].str.replace(r'\D', '', regex=True)
                            if not os.path.exists(caminho_completo):
                                arquivo.seek(0)
                                arquivo.save(caminho_completo)
                                flash(f"Arquivo {nome_arquivo} enviado com sucesso!", "success")
                            else:
                                flash(f"Arquivo {nome_arquivo} já existe. Ignorado.", "warning")
                        except AttributeError as erro:
                            flash(f"O ARQUIVO {nome_arquivo} JA FOI ANALISADO","error")
                    else:
                        flash(f"O arquivo {nome_arquivo} tem colunas faltando. Verifique e corrija.", "error")

                except Exception as e:
                    flash(f"Erro ao processar {nome_arquivo}: {e}", "error")

            else:
                flash(f"Arquivo {nome_arquivo} é inválido. Envie .xlsx, .csv ou .json", "error")

    
        return redirect(url_for('upload_arquivos'))

    return render_template('upload.html')

# Download
@app.route('/download')
def download():
    pasta_organizados = "arquivos/organizados"
    lista_nome_arquivos = os.listdir(pasta_organizados)
    lista_nome_arquivos.sort

    return render_template('download.html',lista_nome_arquivos=lista_nome_arquivos)

# download arquivo
@app.route('/baixar/<nome_arquivo>')
def baixar_arquivo(nome_arquivo):
    pasta = os.path.join("arquivos", "organizados")
    return send_from_directory(pasta, nome_arquivo, as_attachment=True)




if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
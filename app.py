from flask import Flask, render_template, jsonify
from data_loader import carregar_dados_e_limpar_colunas
from statistics_calculator import calcular_estatisticas
from visualization_generator import gerar_visualizacoes_base64

app = Flask(__name__)
num_linhas_iniciais = 50

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    try:
        df = carregar_dados_e_limpar_colunas()
        
        # Gerar gráficos
        graficos = gerar_visualizacoes_base64(df)
        
        # Estatísticas descritivas
        estatisticas = calcular_estatisticas(df)
        
        dados = df.head(num_linhas_iniciais).to_dict('records')
        total_registros = len(df)
        
        return render_template('dashboard.html', 
                               dados=dados, 
                               total_registros=total_registros,
                               graficos=graficos,
                               estatisticas=estatisticas)
        
    except FileNotFoundError as e:
        return render_template('dashboard.html', 
                               dados=[], 
                               total_registros=0,
                               erro=str(e))
    except Exception as e:
        return render_template('dashboard.html', 
                               dados=[], 
                               total_registros=0,
                               erro=f"Erro ao ler o arquivo: {str(e)}")

@app.route('/mais_dados')
def mais_dados():
    try:
        df = carregar_dados_e_limpar_colunas()
        
        dados_restantes = df.iloc[num_linhas_iniciais:].to_dict('records')
        
        return jsonify(dados_restantes)
    
    except FileNotFoundError as e:
        return jsonify({'erro': str(e)}), 404
    except Exception as e:
        return jsonify({'erro': f'Erro interno no servidor: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import base64
from io import BytesIO

def fig_para_base64(fig):
    """Converte uma figura do Plotly para base64 usando uma abordagem alternativa."""
    try:
        # Tenta usar o método padrão primeiro
        img_bytes = fig.to_image(format="png")
        encoded = base64.b64encode(img_bytes).decode('utf-8')
        return f"data:image/png;base64,{encoded}"
    except Exception as e:
        print(f"Erro ao converter figura: {e}")
        # Fallback: retorna uma imagem placeholder
        return "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjMwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjZGRkIi8+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtZmFtaWx5PSJBcmlhbCIgZm9udC1zaXplPSIyMCIgZmlsbD0iIzY2NiIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZHk9Ii4zZW0iPkVycm8gYW8gZ2VyYXIgZ3LDoWZpY288L3RleHQ+PC9zdmc+"

def gerar_visualizacoes_base64(df):
    """Gera todos os gráficos solicitados usando Plotly e converte para base64."""
    graficos = {}
    
    # Histogramas
    for taxa in ['Taxa de Aprovação', 'Taxa de Reprovação', 'Taxa de Abandono']:
        try:
            fig = px.histogram(df, x=taxa, marginal="box", 
                              title=f'Distribuição da {taxa}',
                              nbins=20)
            fig.update_layout(bargap=0.1, height=400, paper_bgcolor='white', plot_bgcolor='white')
            fig.update_traces(marker_color='lightblue')
            graficos[f'histograma_{taxa.replace(" ", "_").lower()}'] = fig_para_base64(fig)
        except Exception as e:
            print(f"Erro ao gerar histograma para {taxa}: {e}")
            graficos[f'histograma_{taxa.replace(" ", "_").lower()}'] = ""
    
    # Gráficos de pizza
    try:
        contagem_dependencia = df['Dependência Administrativa'].value_counts().reset_index()
        contagem_dependencia.columns = ['dependencia', 'contagem']
        fig_dependencia = px.pie(contagem_dependencia, values='contagem', names='dependencia', 
                                title='Composição por Dependência Administrativa')
        fig_dependencia.update_layout(height=400, paper_bgcolor='white')
        graficos['pie_dependencia'] = fig_para_base64(fig_dependencia)
    except Exception as e:
        print(f"Erro ao gerar gráfico de pizza para dependência: {e}")
        graficos['pie_dependencia'] = ""
    
    try:
        contagem_localizacao = df['Localização'].value_counts().reset_index()
        contagem_localizacao.columns = ['localizacao', 'contagem']
        fig_localizacao = px.pie(contagem_localizacao, values='contagem', names='localizacao', 
                                title='Composição por Localização')
        fig_localizacao.update_layout(height=400, paper_bgcolor='white')
        graficos['pie_localizacao'] = fig_para_base64(fig_localizacao)
    except Exception as e:
        print(f"Erro ao gerar gráfico de pizza para localização: {e}")
        graficos['pie_localizacao'] = ""
    
    # Gráficos de linha temporal
    try:
        df_por_ano = df.groupby('Ano')[['Taxa de Aprovação', 'Taxa de Reprovação', 'Taxa de Abandono']].mean().reset_index()
        fig_linha = go.Figure()
        fig_linha.add_trace(go.Scatter(x=df_por_ano['Ano'], y=df_por_ano['Taxa de Aprovação'], 
                                      mode='lines+markers', name='Aprovação', line=dict(color='green')))
        fig_linha.add_trace(go.Scatter(x=df_por_ano['Ano'], y=df_por_ano['Taxa de Reprovação'], 
                                      mode='lines+markers', name='Reprovação', line=dict(color='red')))
        fig_linha.add_trace(go.Scatter(x=df_por_ano['Ano'], y=df_por_ano['Taxa de Abandono'], 
                                      mode='lines+markers', name='Abandono', line=dict(color='orange')))
        fig_linha.update_layout(title='Evolução das Taxas de Rendimento por Ano', 
                               xaxis_title='Ano', yaxis_title='Taxa Média (%)',
                               height=400, paper_bgcolor='white', plot_bgcolor='white')
        graficos['linha_temporal'] = fig_para_base64(fig_linha)
    except Exception as e:
        print(f"Erro ao gerar gráfico de linha temporal: {e}")
        graficos['linha_temporal'] = ""
    
    # Gráficos de barras comparativas
    try:
        # Filtrar apenas regiões para evitar muitos dados
        regioes = ['Norte', 'Nordeste', 'Sudeste', 'Sul', 'Centro-Oeste']
        df_regioes = df[df['Unidade Geográfica'].isin(regioes)]
        
        if not df_regioes.empty:
            df_por_unidade = df_regioes.groupby('Unidade Geográfica')[['Taxa de Aprovação', 'Taxa de Reprovação', 'Taxa de Abandono']].mean().reset_index()
            
            fig_barras = make_subplots(rows=1, cols=3, 
                                      subplot_titles=('Aprovação', 'Reprovação', 'Abandono'))
            
            fig_barras.add_trace(go.Bar(x=df_por_unidade['Unidade Geográfica'], 
                                       y=df_por_unidade['Taxa de Aprovação'], 
                                       name='Aprovação', marker_color='green'), row=1, col=1)
            
            fig_barras.add_trace(go.Bar(x=df_por_unidade['Unidade Geográfica'], 
                                       y=df_por_unidade['Taxa de Reprovação'], 
                                       name='Reprovação', marker_color='red'), row=1, col=2)
            
            fig_barras.add_trace(go.Bar(x=df_por_unidade['Unidade Geográfica'], 
                                       y=df_por_unidade['Taxa de Abandono'], 
                                       name='Abandono', marker_color='orange'), row=1, col=3)
            
            fig_barras.update_layout(title_text='Taxas Médias por Região', 
                                   showlegend=False, height=400, paper_bgcolor='white')
            graficos['barras_comparativas'] = fig_para_base64(fig_barras)
        else:
            graficos['barras_comparativas'] = ""
    except Exception as e:
        print(f"Erro ao gerar gráficos de barras: {e}")
        graficos['barras_comparativas'] = ""
    
    # Heatmap de correlação
    try:
        correlations = df[['Taxa de Aprovação', 'Taxa de Reprovação', 'Taxa de Abandono']].corr()
        fig_heatmap = px.imshow(correlations, 
                               text_auto=True, 
                               color_continuous_scale='RdBu_r', 
                               aspect="auto",
                               title='Correlação entre as Taxas de Rendimento')
        fig_heatmap.update_layout(height=400, paper_bgcolor='white')
        graficos['heatmap_correlacao'] = fig_para_base64(fig_heatmap)
    except Exception as e:
        print(f"Erro ao gerar heatmap de correlação: {e}")
        graficos['heatmap_correlacao'] = ""
    
    return graficos
def calcular_estatisticas(df):
    """Calcula estatísticas descritivas para as taxas."""
    estatisticas = {}
    
    for taxa in ['Taxa de Aprovação', 'Taxa de Reprovação', 'Taxa de Abandono']:
        estatisticas[taxa] = {
            'média': round(df[taxa].mean(), 2),
            'mediana': round(df[taxa].median(), 2),
            'desvio_padrão': round(df[taxa].std(), 2),
            'mínimo': round(df[taxa].min(), 2),
            'máximo': round(df[taxa].max(), 2),
            'q1': round(df[taxa].quantile(0.25), 2),
            'q3': round(df[taxa].quantile(0.75), 2)
        }
    
    return estatisticas

def gerar_insights(df):
    """Gera insights automáticos baseados nos dados."""
    insights = []
    
    # Análise por região
    regioes = ['Norte', 'Nordeste', 'Sudeste', 'Sul', 'Centro-Oeste']
    df_regioes = df[df['Unidade Geográfica'].isin(regioes)]
    
    if not df_regioes.empty:
        # Região com maior aprovação
        aprovação_por_regiao = df_regioes.groupby('Unidade Geográfica')['Taxa de Aprovação'].mean()
        regiao_maior_aprovacao = aprovação_por_regiao.idxmax()
        maior_aprovacao = aprovação_por_regiao.max()
        
        # Região com maior abandono
        abandono_por_regiao = df_regioes.groupby('Unidade Geográfica')['Taxa de Abandono'].mean()
        regiao_maior_abandono = abandono_por_regiao.idxmax()
        maior_abandono = abandono_por_regiao.max()
        
        insights.append(f"A região {regiao_maior_aprovacao} possui a maior taxa média de aprovação ({maior_aprovacao:.1f}%)")
        insights.append(f"A região {regiao_maior_abandono} possui a maior taxa média de abandono ({maior_abandono:.1f}%)")
    
    # Análise temporal
    if 'Ano' in df.columns and len(df['Ano'].unique()) > 1:
        evolucao_aprovacao = df.groupby('Ano')['Taxa de Aprovação'].mean().pct_change().iloc[-1] * 100
        if evolucao_aprovacao > 0:
            insights.append(f"Taxa de aprovação aumentou {evolucao_aprovacao:.1f}% no último período analisado")
        else:
            insights.append(f"Taxa de aprovação diminuiu {abs(evolucao_aprovacao):.1f}% no último período analisado")
    
    # Análise por dependência administrativa
    if 'Dependência Administrativa' in df.columns:
        aprovação_por_dependencia = df.groupby('Dependência Administrativa')['Taxa de Aprovação'].mean()
        melhor_dependencia = aprovação_por_dependencia.idxmax()
        pior_dependencia = aprovação_por_dependencia.idxmin()
        
        insights.append(f"Maior taxa de aprovação em instituições {melhor_dependencia.lower()}")
        insights.append(f"Menor taxa de aprovação em instituições {pior_dependencia.lower()}")
    
    # Correlações
    correlacao_aprov_reprov = df['Taxa de Aprovação'].corr(df['Taxa de Reprovação'])
    if correlacao_aprov_reprov < -0.7:
        insights.append("Fort correlação negativa entre aprovação e reprovação (esperado)")
    
    return insights

def gerar_resumo_executivo(df):
    """Gera um resumo executivo dos dados."""
    resumo = {
        'total_registros': len(df),
        'periodo_anos': f"{df['Ano'].min()} - {df['Ano'].max()}" if 'Ano' in df.columns else "N/A",
        'unidades_geograficas': df['Unidade Geográfica'].nunique(),
        'media_aprovacao': round(df['Taxa de Aprovação'].mean(), 1),
        'media_reprovacao': round(df['Taxa de Reprovação'].mean(), 1),
        'media_abandono': round(df['Taxa de Abandono'].mean(), 1)
    }
    
    return resumo
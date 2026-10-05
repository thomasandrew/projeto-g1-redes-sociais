"""Leitura, preparação e indicadores compartilhados pelo projeto."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent

def carregar():
    df = pd.read_csv(ROOT / 'dados/simulacao_redes_sociais_brasil.csv')
    df = df.drop_duplicates().copy()
    df['data'] = pd.to_datetime(df['data'], errors='raise')
    numeros = ['seguidores', 'curtidas', 'comentarios', 'compartilhamentos',
               'visualizacoes', 'alcance', 'taxa_engajamento']
    for coluna in numeros:
        df[coluna] = pd.to_numeric(df[coluna], errors='raise')
    if df[numeros].isna().any().any() or (df[numeros] < 0).any().any():
        raise ValueError('Métricas ausentes ou negativas na base.')
    df['ano'] = df['data'].dt.year
    df['mes'] = df['data'].dt.month
    df['hora'] = pd.to_datetime(df['horario_publicacao'], format='%H:%M').dt.hour
    df['interacoes'] = df['curtidas'] + df['comentarios'] + df['compartilhamentos']
    df['engajamento_por_alcance'] = df['interacoes'].div(df['alcance'].replace(0, float('nan'))) * 100
    df['periodo'] = df['data'].dt.to_period('M').astype(str)
    return df

def indicadores(df):
    return {
        'publicacoes': len(df),
        'seguidores_somados': int(df.seguidores.sum()),
        'engajamento_medio': float(df.taxa_engajamento.mean()),
        'visualizacoes': int(df.visualizacoes.sum()),
        'plataforma': df.groupby('plataforma').taxa_engajamento.mean().idxmax(),
        'conteudo': df.groupby('tipo_conteudo').alcance.mean().idxmax(),
        'horario': df.groupby('horario_publicacao').taxa_engajamento.mean().idxmax(),
    }

def persistir(df):
    """Atualiza a tabela e comprova a leitura SQL via SQLAlchemy."""
    from sqlalchemy import create_engine, text
    pasta = ROOT / 'database'
    pasta.mkdir(exist_ok=True)
    engine = create_engine('sqlite:///' + str(pasta / 'redes_sociais.db'))
    df.to_sql('publicacoes', engine, if_exists='replace', index=False)
    with engine.connect() as conexao:
        total = conexao.execute(text('SELECT COUNT(*) FROM publicacoes')).scalar_one()
    engine.dispose()
    return total

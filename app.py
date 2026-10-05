"""Dashboard G1 — execute com streamlit run app.py."""
import streamlit as st
import plotly.express as px
from analise import carregar, indicadores, persistir

st.set_page_config(page_title='Engajamento Digital | G1', layout='wide')

@st.cache_data
def dados():
    return carregar()

base = dados()
with st.sidebar:
    st.header('Filtros')
    df = base.copy()
    for coluna, rotulo in [('ano','Ano'), ('mes','Mês'), ('plataforma','Plataforma'),
                           ('categoria','Categoria'), ('tipo_conteudo','Tipo de conteúdo'), ('perfil','Perfil')]:
        opcoes = sorted(base[coluna].unique().tolist())
        escolhas = st.multiselect(rotulo, opcoes, default=opcoes, key=coluna)
        df = df[df[coluna].isin(escolhas)]
    st.caption('Filtros aplicados a todas as páginas. Nenhuma opção selecionada produz um recorte vazio.')

def cabecalho():
    st.title('Análise de Redes Sociais e Engajamento Digital')
    st.markdown('**Disciplina:** Linguagem de Programação — Análise e Visualização de Dados com Python  \n**Professor:** Alexandre Neves Louzada  \n**Aluno:** Thomas Andrew de Souza Batista')
    st.write('Projeto G1 • Analisar plataformas, conteúdos, perfis e horários entre 2015 e 2024.')
    st.info('Base simulada: os resultados não representam o desempenho real das plataformas. A taxa fornecida é analisada separadamente da taxa calculada por alcance.')
    if df.empty:
        st.warning('Nenhum registro corresponde aos filtros. Selecione outras opções.')
        st.stop()

def conclusao():
    k = indicadores(df)
    st.subheader('Conclusão executiva do recorte')
    st.write(f"No recorte de {k['publicacoes']:,} registros, {k['plataforma']} apresenta a maior taxa média informada; {k['conteudo']} lidera o alcance médio e {k['horario']} lidera o engajamento médio por horário. Compare também o tamanho dos grupos antes de escolher uma estratégia.")
    st.caption('Diferenças descritivas não demonstram causalidade nem significância estatística. Não há identificador de campanha; não é possível comparar campanhas. Seguidores variam entre registros e não formam um histórico validado de crescimento.')

def visao():
    cabecalho()
    k = indicadores(df)
    cols = st.columns(3)
    cols[0].metric('Seguidores somados nos registros', f"{k['seguidores_somados']:,}")
    cols[1].metric('Engajamento médio informado', f"{k['engajamento_medio']:.2f}%")
    cols[2].metric('Visualizações acumuladas', f"{k['visualizacoes']:,}")
    cols = st.columns(3)
    cols[0].metric('Plataforma mais engajada', k['plataforma'])
    cols[1].metric('Formato com maior alcance médio', k['conteudo'])
    cols[2].metric('Horário com maior engajamento médio', k['horario'])
    st.caption('A soma de seguidores atende ao enunciado, mas repete perfis e não representa pessoas únicas. Visualizações e alcance também podem repetir pessoas.')
    temporal = df.groupby('periodo', as_index=False).taxa_engajamento.mean()
    st.plotly_chart(px.line(temporal, x='periodo', y='taxa_engajamento', title='Engajamento médio mensal (%)'), use_container_width=True)
    for coluna, titulo in [('plataforma','Engajamento por plataforma'), ('tipo_conteudo','Engajamento por formato')]:
        tabela = df.groupby(coluna).agg(engajamento=('taxa_engajamento','mean'), registros=('data','size')).reset_index()
        st.plotly_chart(px.bar(tabela, x=coluna, y='engajamento', hover_data=['registros'], title=titulo), use_container_width=True)
    conclusao()

def exploracao():
    cabecalho()
    mapa = df.pivot_table(index='plataforma', columns='hora', values='alcance', aggfunc='mean')
    st.plotly_chart(px.imshow(mapa, aspect='auto', title='Alcance médio por plataforma e horário'), use_container_width=True)
    st.plotly_chart(px.scatter(df, x='seguidores', y='taxa_engajamento', color='plataforma', hover_data=['perfil','tipo_conteudo'], title='Seguidores × taxa de engajamento informada'), use_container_width=True)
    ranking = df.groupby(['plataforma','perfil']).agg(engajamento=('taxa_engajamento','mean'), alcance=('alcance','mean'), registros=('data','size')).sort_values('engajamento', ascending=False)
    st.subheader('Ranking de perfis')
    st.dataframe(ranking, use_container_width=True)
    seguidores = df.groupby(['ano','plataforma','perfil'], as_index=False).seguidores.median()
    seguidores['conta'] = seguidores['plataforma'] + ' / ' + seguidores['perfil']
    st.plotly_chart(px.line(seguidores, x='ano', y='seguidores', color='conta', title='Seguidores medianos por conta e ano — evolução descritiva'), use_container_width=True)
    st.caption('A mediana resume os registros de cada conta/ano; não é uma medição de novos seguidores.')
    frequencia = df.groupby(['periodo','plataforma','perfil']).agg(postagens=('data','size'), alcance_medio=('alcance','mean')).reset_index()
    st.plotly_chart(px.scatter(frequencia, x='postagens', y='alcance_medio', color='plataforma', title='Frequência mensal × alcance médio'), use_container_width=True)
    st.subheader('Publicações de alcance elevado')
    limite = df.alcance.quantile(.95)
    st.caption('Critério exploratório: alcance no percentil 95 ou superior do recorte. Não comprova viralidade real.')
    st.dataframe(df[df.alcance >= limite].sort_values('alcance', ascending=False), use_container_width=True)
    st.subheader('Tabela dinâmica')
    grupo = st.selectbox('Agrupar por', ['plataforma','perfil','categoria','tipo_conteudo','ano','mes'])
    st.dataframe(df.groupby(grupo).agg(publicacoes=('data','size'), engajamento_medio=('taxa_engajamento','mean'), alcance_medio=('alcance','mean'), visualizacoes=('visualizacoes','sum')), use_container_width=True)
    st.download_button('Baixar recorte CSV', df.to_csv(index=False).encode('utf-8-sig'), 'recorte.csv', 'text/csv')
    conclusao()

def metodologia():
    cabecalho()
    st.subheader('Qualidade e método')
    st.write('Leitura com Pandas; remoção de duplicatas; validação numérica; conversão de datas; atributos de hora, período mensal, interações e engajamento por alcance. As médias são simples por registro.')
    st.write('Taxa calculada = 100 × (curtidas + comentários + compartilhamentos) / alcance. Como a definição da taxa original não foi fornecida, preservamos ambas.')
    colunas = ['seguidores','curtidas','comentarios','compartilhamentos','visualizacoes','alcance','taxa_engajamento']
    st.plotly_chart(px.imshow(df[colunas].corr(), zmin=-1, zmax=1, color_continuous_scale='RdBu_r', title='Correlação de Pearson'), use_container_width=True)
    st.caption('Correlação mede associação linear, não causa e efeito. A taxa original pode ter sido simulada independentemente das outras métricas.')
    if st.button('Persistir base completa no SQLite'):
        st.success(f'{persistir(base):,} registros gravados e conferidos por consulta SQL.')
    st.caption('O SQLite fica no servidor; na nuvem, o armazenamento local pode ser recriado. O CSV é a fonte reproduzível do projeto.')
    st.dataframe(df.describe(), use_container_width=True)
    conclusao()

pagina = st.navigation([st.Page(visao, title='Visão geral'), st.Page(exploracao, title='Conteúdos e perfis'), st.Page(metodologia, title='Método e correlações')])
pagina.run()

# import libs 
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from matplotlib import cm

#
def load_sub_dataframes():
    # importando o dicionario de dataframes
    file_path = "../../datasets/processados/sub_dataframes.pkl"
    with open(file_path, 'rb') as file:
        return pickle.load(file)

# carregar o dicionario de dataframes
sub_dataframes = load_sub_dataframes()

##sub_dataframes

###OBJ UTEIS
bimestres = [1, 2, 3, 4]

disciplinas = ['port', 'cien', 'edfi', 'geog', 'hist', 'mate', 'ingl', 'arte', 'reli']

###FUNÇÕES

#pgeral
# (PG 1)
def plot_medias_todas_disciplinas_plotly(sub_dataframes, tema):
    """
    grafico de linhas com marcadores para comparar as medias das notas de diferentes disciplinas ao longo dos anos,
    utilizando o Plotly e permitindo a visualizaçao individual das disciplinas atraves da legenda.

    arguments:
        sub_dataframes (dict): Dicionario com os DataFrames de cada turma. As chaves sao os nomes das turmas, e os valores
                          sao DataFrames contendo as colunas 'disciplina_#bimestre' e 'nota'.
        tema (str): Tema do grafico (light ou dark) - útil para locais com pouca/muita luminosidade     

    Returns:
        plotly.graph_objects.Figure: Figura do grafico.
    """
    # Validaçao de entrada
    if not isinstance(sub_dataframes, dict):
        raise ValueError("sub_dataframes deve ser um dicionario.")
    if tema not in ['light', 'dark']:
        raise ValueError("O tema deve ser 'light' ou 'dark'.")

    # verificando se as colunas necessarias estao presentes
    required_columns = ['disciplina_#bimestre', 'nota']
    for df in sub_dataframes.values():
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Os DataFrames devem conter as colunas: {required_columns}")
    
    # definindo template e cor das anotações com base no tema
    template = 'plotly_dark' if tema == 'dark' else 'plotly'
    #annotation_color = "white" if tema == 'dark' else "black"

    fig = go.Figure()

    # adiciona as linhas das disciplinas
    for idx, disciplina in enumerate(disciplinas):
        media_da_turma = {}

        # filtrando os dados por disciplina
        for turma, df in sub_dataframes.items():
            # usando uma comparaçao exata para evitar problemas com o filtro
            df_filtrado = df[df['disciplina_#bimestre'].str.contains(disciplina, case=False, na=False)]
            if not df_filtrado.empty:
                media = df_filtrado['nota'].mean()
                media_da_turma[turma] = media

        ## se for a primeira disciplina (idx == 0) fica visivel, senao so na legenda
        visibilidade = True if idx == 0 else 'legendonly'

        # adiciona a linha ao grafico
        fig.add_trace(go.Scatter(
            x=list(media_da_turma.keys()),
            y=list(media_da_turma.values()),
            mode='lines+markers',
            name=disciplina,
            visible=visibilidade 
        ))

    # ajustes do layout
    fig.update_layout(
        title='Media das Notas por Disciplina ao Longo dos Anos',
        xaxis_title='Ano',
        yaxis_title='Media das Notas',
        template=template,
        xaxis=dict(showline=True, showgrid=True, zeroline=False),
        yaxis=dict(showline=True, showgrid=True, zeroline=False),
        showlegend=True,        
        title_x=0.5,
        title_y=0.9
    )
    return fig

# (PG 2)
#definindo uma cor padrao para determinada disciplina, facilitando comparaçao ao trocar de turma:
# paleta de cores qualitative do Plotly
cores_plotly = px.colors.qualitative.Plotly

#dicionario para mapear disciplinas a cores
disciplina_colors = dict(zip(disciplinas, cores_plotly))

def plot_medias_disciplina_por_turma(sub_dataframes, turma, tema):
    """
    grafico de barras horizontais das medias anuais das notas por disciplina para uma turma especifica. 
    (utiliza a media das 'medias das notas finais' dos estudantes daquela turma)

    As barras sao coloridas de acordo com a disciplina, usando uma paleta de cores qualitativas do Plotly.

    """
   
    if not isinstance(sub_dataframes, dict):
        raise ValueError("sub_dataframes deve ser um dicionario.")
    if tema not in ['light', 'dark']:
        raise ValueError("O tema deve ser 'light' ou 'dark'.")
    if turma not in sub_dataframes:
        raise ValueError(f"A turma '{turma}' nao foi encontrada no dicionario de DataFrames.")
    
    required_columns = ['disciplina_#bimestre', 'nota']
    for df in sub_dataframes.values():
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Os DataFrames devem conter as colunas: {required_columns}")

    template = 'plotly_dark' if tema == 'dark' else 'plotly'
    
    #filtra o DataFrame da turma especificada
    df_turma = sub_dataframes[turma]

    #calculando as medias das notas para cada disciplina (independentemente do bimestre)
    df_turma['disciplina'] = df_turma['disciplina_#bimestre'].str.extract(r'(\D+)')
    
    #calculando as medias das notas para cada disciplina
    medias_por_disciplina = df_turma.groupby('disciplina')['nota'].mean().sort_values()

    fig = go.Figure()

    # adiciona as barras ao grafico
    fig.add_trace(
        go.Bar(
            x=medias_por_disciplina.values,
            y=medias_por_disciplina.index,
            orientation='h',
            marker=dict(
                color=[disciplina_colors.get(disciplina, 'gray') for disciplina in medias_por_disciplina.index]
            ),
            name=f'Turma {turma}'
        )
    )
 
    fig.update_layout(
        title=f'Media das Notas por Disciplina para a Turma {turma}',
        xaxis_title='Media das Notas',
        yaxis_title='Disciplina',
        template=template,
        xaxis=dict(showline=True, showgrid=True, zeroline=False),
        yaxis=dict(showline=True, showgrid=True, zeroline=False),        
        title_x=0.5,
        title_y=0.9
    )
    return fig


#plot  iterativo  com plotly (PG 3)
def plot_boxplot_com_interatividade(sub_dataframes, disciplina, tema):
    """
    boxplot interativo das notas por turma para uma disciplina especifica.

    O boxplot exibe a distribuiçao das notas, incluindo pontos individuais e as medias de cada turma.
    e o tema (claro ou escuro).

    """

    if not isinstance(sub_dataframes, dict):
        raise ValueError("sub_dataframes deve ser um dicionario.")
    if tema not in ['light', 'dark']:
        raise ValueError("O tema deve ser 'light' ou 'dark'.")
 
    required_columns = ['disciplina_#bimestre', 'turma', 'nota']
    for df in sub_dataframes.values():
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Os DataFrames devem conter as colunas: {required_columns}")

    template = 'plotly_dark' if tema == 'dark' else 'plotly'
    
    # pra combinar todos os DataFrames em um único DF
    combined_df = pd.concat(sub_dataframes.values())
    
    # filtra o DataFrame para a disciplina e bimestre desejados
    filtered_df = combined_df[combined_df['disciplina_#bimestre'].str.contains(disciplina)]
    
    # criando o boxplot com plotly
    fig = px.box(
        filtered_df,
        x='turma',
        y='nota',
        points="all",  # add pontos individuais para visualizaçao detalhada
        title=f'Boxplot das Notas para {disciplina}',
        labels={'nota': 'Nota', 'turma': 'Ano'}
    )
    
    # checar a media para cada grupo (ano)
    for ano in filtered_df['turma'].unique():
        media_nota = filtered_df[filtered_df['turma'] == ano]['nota'].mean()
        fig.add_trace(
            go.Scatter(
                x=[ano],
                y=[media_nota],
                mode='markers',
                marker=dict(color='Blue', size=5),
                text=[f'Media: {media_nota:.2f}'],
                textposition='top center',
                showlegend=False
            )
        )
    
    # interatividade do grafico
    fig.update_traces(
        marker=dict(color='blue', size=8),  # configura o estilo dos pontos no boxplot
        selector=dict(mode='markers+text')
    )
    
    fig.update_layout(
        xaxis_title='Ano',
        yaxis_title='Nota',
        template=template,
        title=f'Boxplot Interativo para {disciplina}',
        title_x=0.5,
        title_y=0.9
    )
    return fig


#pbimestral

# (PB 1)
def plot_4_bimestres_disciplina_por_turma_plotly(sub_dataframes, disciplina, tema):
    """
    O grafico de linhas exibe as medias das notas por turma para cada bimestre, alem de poder alternar a visibilidade dos bimestres e filtrar por uma disciplina por vez.
    O bimestre com a media mais baixa e destacado como "bimestre critico". 
    (o valor e obtido calculando as medias das notas por bimestre (media global) e selecionando o com a menor media)

    """
   
    if not isinstance(sub_dataframes, dict):
        raise ValueError("sub_dataframes deve ser um dicionario.")
    if tema not in ['light', 'dark']:
        raise ValueError("O tema deve ser 'light' ou 'dark'.")
    
    required_columns = ['disciplina_#bimestre', 'turma', 'nota']
    for df in sub_dataframes.values():
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Os DataFrames devem conter as colunas: {required_columns}")

    template = 'plotly_dark' if tema == 'dark' else 'plotly'
    annotation_color = "white" if tema == 'dark' else "black"

    fig = go.Figure()

    #dicionario para armazenar as medias de cada bimestre
    medias_bimestres = {}

    for idx, bimestre in enumerate(bimestres):
        disciplina_bimestre = f'{disciplina}{bimestre}'
        
        # dicionario para armazenar medias das notas por ano
        media_por_turma = {}
        
        for turma, df in sub_dataframes.items():
            #filtrar o dataframe para a disciplina e bimestre especificados
            df_filtrado = df[df['disciplina_#bimestre'] == disciplina_bimestre]
            #calcular a media das notas dele
            media = df_filtrado['nota'].mean()
            #armazena essa media no dicionario
            media_por_turma[turma] = media
        
        #visibilidade com base no indice: visivel para o primeiro bimestre e 'legendonly' para os outros
        visibility = True if idx == 0 else 'legendonly'
        
        #  Adiciona uma linha para o bimestre
        fig.add_trace(go.Scatter(
            x=list(media_por_turma.keys()),
            y=list(media_por_turma.values()),
            mode='lines+markers',
            name=f'Bimestre {bimestre}',
            visible=visibility
        ))

        # armazenar a media global do bimestre
        medias_bimestres[bimestre] = sum(media_por_turma.values()) / len(media_por_turma)

    # identificar o bimestre com a media mais baixa (aka bimestre critico)
    bimestre_critico = min(medias_bimestres, key=medias_bimestres.get)
    media_bimestre_critico = medias_bimestres[bimestre_critico]
 
    fig.update_layout(
        title=f'Media das Notas para {disciplina.upper()} por Bimestre ao Longo dos Anos',
        xaxis_title='Ano',
        yaxis_title='Media das Notas',        
        title_x=0.5,
        title_y=0.9,
        legend_title='Bimestres',
        template=template, 
        annotations=[
            go.layout.Annotation(
                text=f'Bimestre mais critico: Bimestre {bimestre_critico} com media {media_bimestre_critico:.2f}',
                xref='paper', yref='paper',
                x=0, y=-0.2,
                showarrow=False,
                font=dict(size=12, color=annotation_color)
            )
        ]
    )
    return fig

## (PB 2)
def plot_boxplot_disc_bim_interativo(sub_dataframes, disciplina, bimestre, tema):
    """
    boxplot interativo das notas por turma para uma disciplina e bimestre que podem ser escolhidos.

    O boxplot exibe a distribuiçao das notas, incluindo pontos individuais e as medias de cada turma.
    """
   
    if not isinstance(sub_dataframes, dict):
        raise ValueError("sub_dataframes deve ser um dicionario.")
    if tema not in ['light', 'dark']:
        raise ValueError("O tema deve ser 'light' ou 'dark'.")

    required_columns = ['disciplina_#bimestre', 'nota', 'turma']
    for df in sub_dataframes.values():
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Os DataFrames devem conter as colunas: {required_columns}")

    template = 'plotly_dark' if tema == 'dark' else 'plotly'
    
    disciplina_bimestre = f'{disciplina}{bimestre}'
 
    combined_df = pd.concat(sub_dataframes.values())
    
    filtered_df = combined_df[combined_df['disciplina_#bimestre'] == disciplina_bimestre]

    fig = go.Figure()

    fig = px.box(
        filtered_df,
        x='turma',
        y='nota',
        points="all",  
        title=f'Boxplot das Notas para {disciplina} - {bimestre}º Bimestre',
        labels={'nota': 'Nota', 'turma': 'Ano'}
    )
 
    for ano in filtered_df['turma'].unique():
        media_nota = filtered_df[filtered_df['turma'] == ano]['nota'].mean()
        fig.add_trace(
            go.Scatter(
                x=[ano],
                y=[media_nota],
                mode='markers',
                marker=dict(color='blue', size=8),
                text=[f'Media: {media_nota:.2f}'],
                textposition='top center',
                showlegend=False
            )
        )
 
    fig.update_layout(
        xaxis_title='Ano',
        yaxis_title='Nota',
        template=template, 
        title=f'Boxplot Interativo para {disciplina} - {bimestre}º Bimestre',
        title_x=0.5,
        title_y=0.9
    )
    return fig


# (PB 3)
def plot_heatmap_bimestres_criticos(sub_dataframes, tema):
    """
    Funçao q gera o heatmap das medias das notas por disciplina e bimestre.

    exibe as medias das notas para cada disciplina e bimestre, permitindo identificar
    padrões e bimestres criticos (com medias mais baixas).

    """
   
    if not isinstance(sub_dataframes, dict):
        raise ValueError("sub_dataframes deve ser um dicionario.")
    if tema not in ['light', 'dark']:
        raise ValueError("O tema deve ser 'light' ou 'dark'.")

    
    required_columns = ['disciplina_#bimestre', 'nota']
    for df in sub_dataframes.values():
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Os DataFrames devem conter as colunas: {required_columns}")

    template = 'plotly_dark' if tema == 'dark' else 'plotly'
    
    # lista para armazenar as medias por disciplina e bimestre
    dados_heatmap = []

    # para cada disciplina, calcular a media para cada bimestre
    for disciplina in disciplinas:
        for bimestre in range(1, 5):  # 4 bimestres
            disciplina_bimestre = f'{disciplina}{bimestre}'
            medias_bimestres = []
            
            # pegar as medias de cada turma para a disciplina e bimestre
            for turma, df in sub_dataframes.items():
                df_filtrado = df[df['disciplina_#bimestre'] == disciplina_bimestre]
                media = df_filtrado['nota'].mean()
                medias_bimestres.append(media)
            
            # media geral para essa disciplina e bimestre ao longo dos anos
            media_geral = sum(medias_bimestres) / len(medias_bimestres) if medias_bimestres else None
            dados_heatmap.append({'disciplina': disciplina, 'bimestre': bimestre, 'media': media_geral})
    
    # converter para DataFrame
    df_heatmap = pd.DataFrame(dados_heatmap)

    # usar o pivot com argumentos pro heatmap - criando a tabela
    df_pivot = df_heatmap.pivot(index='disciplina', columns='bimestre', values='media')

    # plotar o Heatmap
    try:
        fig = px.imshow(df_pivot,
                        title='Media das Notas por Disciplina e Bimestre',
                        labels={'color': 'Media das Notas'},
                        aspect='auto',
                        color_continuous_scale='Blues',
                        text_auto=True  # feature pra exibir os valores no heatmap
                        )  
        
        fig.update_layout(
            xaxis_title='Bimestre',
            yaxis_title='Disciplina',
            template=template,
            height=600,
            title_x=0.5,
            title_y=0.99,
            title_pad=dict(t=10),
            margin=dict(l=20, r=20, t=40, b=20)
        )    
        return fig
    
    except Exception as e:
        print(f"Erro ao gerar o heatmap: {e}")
        return go.Figure() 
    

# pperfil

# (PP 1)
def plot_histogram_idade_turma(sub_dataframes, tema):
    """
    grafico histograma interativo com a distribuiçao de idades dos alunos por turma.
    (ideia utilizada no PNAIC)
    
    """
   
    if not isinstance(sub_dataframes, dict):
        raise ValueError("sub_dataframes deve ser um dicionario.")
    if tema not in ['light', 'dark']:
        raise ValueError("O tema deve ser 'light' ou 'dark'.")

    required_columns = ['index', 'idade', 'turma']
    for df in sub_dataframes.values():
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Os DataFrames devem conter as colunas: {required_columns}")

    template = 'plotly_dark' if tema == 'dark' else 'plotly'
    
    try:
        combined_df = pd.concat(sub_dataframes.values())
        
        # Remove duplicatas com base na coluna 'index' para garantir que cada aluno eh contado apenas uma vez
        combined_df_unique = combined_df.drop_duplicates(subset='index')
        
        fig = go.Figure()

        # adiciona um grafico de barras para cada turma
        for turma in combined_df_unique['turma'].unique():
            df_turma = combined_df_unique[combined_df_unique['turma'] == turma]
            idade_counts = df_turma['idade'].value_counts().sort_index()
            
            fig.add_trace(
                go.Bar(
                    x=idade_counts.index,
                    y=idade_counts.values,
                    name=f'Turma {turma}',
                    opacity=0.75
                )
            )
        
        fig.update_layout(
            title='Distribuiçao das Idades por Turma',
            xaxis_title='Idade',
            yaxis_title='Quantidade de Alunos',
            barmode='group',  
            template=template,  
            xaxis=dict(
                showline=True,
                showgrid=True,
                zeroline=False,
                tickvals=list(range(int(combined_df_unique['idade'].min()), int(combined_df_unique['idade'].max()) + 1)),
                ticktext=[str(i) for i in range(int(combined_df_unique['idade'].min()), int(combined_df_unique['idade'].max()) + 1)]
            ),
            yaxis=dict(showline=True, showgrid=True, zeroline=False),
            title_x=0.5,
            title_y=0.9
        )    
        return fig

    except Exception as e:
        print(f"Erro ao gerar o histograma: {e}")
        return go.Figure() 

# (PP 2)
def plot_boxplot_idade_turma(sub_dataframes, tema):
    """
    boxplot interativo mostrando a distribuiçao das idades dos alunos por turma.
    """
   
    if not isinstance(sub_dataframes, dict):
        raise ValueError("sub_dataframes deve ser um dicionario.")
    if tema not in ['light', 'dark']:
        raise ValueError("O tema deve ser 'light' ou 'dark'.")
    
    required_columns = ['index', 'idade', 'turma']
    for df in sub_dataframes.values():
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Os DataFrames devem conter as colunas: {required_columns}")
    
    template = 'plotly_dark' if tema == 'dark' else 'plotly'
    
    try:    
        combined_df = pd.concat(sub_dataframes.values())

        combined_df_unique = combined_df.drop_duplicates(subset='index')
 
        fig = px.box(
            combined_df_unique,
            x='turma',
            y='idade',
            points="all",  
            title='Boxplot das Idades por Turma',
            labels={'idade': 'Idade', 'turma': 'Ano'}
        )

        for ano in combined_df_unique['turma'].unique():
            media_idade = combined_df_unique[combined_df_unique['turma'] == ano]['idade'].mean()
            fig.add_trace(
                go.Scatter(
                    x=[ano],
                    y=[media_idade],
                    mode='markers',
                    marker=dict(color='blue', size=5),
                    text=[f'Media: {media_idade:.2f}'],
                    textposition='top center',
                    showlegend=False
                )
            )

        fig.update_traces(
            marker=dict(color='blue', size=8),  
            selector=dict(mode='markers+text')
        )

        fig.update_layout(
            xaxis_title='Ano',
            yaxis_title='Idade',
            template=template, 
            title='Boxplot Interativo das Idades por Turma',
            title_x=0.5,
            title_y=0.9
        )
        return fig
    
    except Exception as e:
        print(f"Erro ao gerar o boxplot: {e}")
        return go.Figure()  


# (PP 3)
# utilizado no proximo plot alunos e taxa aprovacao
def calcular_taxa_aprovacao(sub_dataframes):

    if not isinstance(sub_dataframes, dict):
        raise ValueError("sub_dataframes deve ser um dicionario.")

    required_columns = ['index', 'disciplina_#bimestre', 'nota']
    for df in sub_dataframes.values():
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Os DataFrames devem conter as colunas: {required_columns}")

    aprovacao_por_turma = {}

    # iterar sobre o dicionario de DataFrames
    for ano, df in sub_dataframes.items(): 
        medias_finais = df.groupby(['index', df['disciplina_#bimestre'].str[:-1]])['nota'].mean().reset_index()
 
        total_alunos = df['index'].nunique()

        # contar o número de alunos aprovados (pra nota media ≥ 6)
        aprovados = medias_finais[medias_finais['nota'] >= 6]['index'].nunique()
 
        taxa_aprovacao = (aprovados / total_alunos) * 100
 
        aprovacao_por_turma[ano] = taxa_aprovacao
    
    return aprovacao_por_turma

# funcao plot 
def plot_alunos_e_taxa_aprovacao(sub_dataframes, tema):
    """
    grafico de barras interativo que exibe a quantidade de alunos e a taxa de aprovaçao por turma.

    possui um eixo Y para a quantidade de alunos e um eixo Y secundario para a taxa de aprovaçao.
    As barras sao coloridas com um gradiente azul baseado na taxa de aprovaçao.
    
    """

    if not isinstance(sub_dataframes, dict):
        raise ValueError("sub_dataframes deve ser um dicionario.")
    if tema not in ['light', 'dark']:
        raise ValueError("O tema deve ser 'light' ou 'dark'.")
    
    
    required_columns = ['turma', 'index']
    for df in sub_dataframes.values():
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Os DataFrames devem conter as colunas: {required_columns}")
    
    template = 'plotly_dark' if tema == 'dark' else 'plotly'
    
    combined_df = pd.concat(sub_dataframes.values())
    
    # calcular a quantidade de alunos únicos por turma (ano)
    alunos_por_turma = combined_df.groupby('turma')['index'].nunique()
    
    # calcular a taxa de aprovaçao por turma (ano)
    taxa_aprovacao = calcular_taxa_aprovacao(sub_dataframes)
    
    taxa_aprovacao_values = [taxa_aprovacao.get(ano, 0) for ano in alunos_por_turma.index]
    
    # ajuste dinâmico do colormap para evitar problemas com valores menores que 90%
    if taxa_aprovacao_values:  
        norm = plt.Normalize(vmin=60, vmax=100)
        cmap = cm.get_cmap('Blues', 256)
        colors = cmap(norm(taxa_aprovacao_values))
        colors = ['rgba({}, {}, {}, 1.0)'.format(int(c[0]*255), int(c[1]*255), int(c[2]*255)) for c in colors]
    else:
        colors = ['blue'] * len(alunos_por_turma)  # cor azul padrao caso nao haja dados
    
    # intervalo do eixo Y
    max_alunos = alunos_por_turma.max()
    intervalo_max = max_alunos * 1.25 if max_alunos > 0 else 10  # pra evitar range zero

    fig = go.Figure()

    # barra com as quantidades de alunos e cores gradativas
    fig.add_trace(go.Bar(
        x=alunos_por_turma.index,
        y=alunos_por_turma.values,
        name='Quantidade de Alunos',
        marker=dict(color=colors, line=dict(color='black', width=1)),  
        text=['{:.1f}%'.format(taxa_aprovacao.get(ano, 0)) for ano in alunos_por_turma.index],
        textposition='inside',
        insidetextanchor='middle'
    ))

    # layout com dois eixos Y
    fig.update_layout(
        title='Quantidade de Alunos e Taxa de Aprovaçao por Ano',
        xaxis_title='Ano',
        xaxis=dict(
            tickvals=alunos_por_turma.index,  # define as posições dos ticks no eixo x
            ticktext=[str(ano) for ano in alunos_por_turma.index],  # define os rotulos dos ticks no eixo x
            title_standoff=20,  # espaço entre o eixo e o titulo
            tickangle=-45  # rotaciona os rotulos do eixo x
        ),
        yaxis=dict(
            title='Quantidade de Alunos',
            side='left',
            title_standoff=20,  
            range=[0, intervalo_max],  # intervalo do eixo y ajustado
            dtick=5  # define o espaçamento dos ticks do eixo y para 5 unidades
        ),
        yaxis2=dict(
            title='Taxa de Aprovaçao (%)',
            side='right',
            overlaying='y',
            range=[0, 100],  # intervalo para a taxa de aprovaçao de 0 a 100%
            title_standoff=20,  
            anchor='x',  # pro eixo y2 se alinhar com o eixo x
            showgrid=False  # desativar a grade para o eixo y2
        ),
        template=template, 
        barmode='group',  
        margin=dict(l=40, r=20, t=40, b=100), 
        title_x=0.5,
        #title_y=0.9, 
    )
    return fig

# import libs 
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from matplotlib import cm

#
def load_sub_dataframes():
    # Importando o dicionário de dataframes
    file_path = "../../datasets/processados/sub_dataframes.pkl"
    with open(file_path, 'rb') as file:
        return pickle.load(file)

# Carregar o dicionário de dataframes
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
    gráfico de linhas com marcadores para comparar as médias das notas de diferentes disciplinas ao longo dos anos,
    utilizando o Plotly e permitindo a visualização individual das disciplinas através da legenda.

    arguments:
        sub_dataframes (dict): Dicionário com os DataFrames de cada turma. As chaves são os nomes das turmas, e os valores
                          são DataFrames contendo as colunas 'disciplina_#bimestre' e 'nota'.
        tema (str): Tema do gráfico (light ou dark) - útil para locais com pouca/muita luminosidade     

    Returns:
        plotly.graph_objects.Figure: Figura do gráfico.
    """
    # Validação de entrada
    if not isinstance(sub_dataframes, dict):
        raise ValueError("sub_dataframes deve ser um dicionário.")
    if tema not in ['light', 'dark']:
        raise ValueError("O tema deve ser 'light' ou 'dark'.")

    # Verifica se as colunas necessárias estão presentes
    required_columns = ['disciplina_#bimestre', 'nota']
    for df in sub_dataframes.values():
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Os DataFrames devem conter as colunas: {required_columns}")
    
    # Definir template e cor das anotações com base no tema
    template = 'plotly_dark' if tema == 'dark' else 'plotly'
    #annotation_color = "white" if tema == 'dark' else "black"

    fig = go.Figure()

    # Adiciona as linhas das disciplinas
    for idx, disciplina in enumerate(disciplinas):
        media_da_turma = {}

        # Filtra os dados por disciplina
        for turma, df in sub_dataframes.items():
            # Usando uma comparação exata para evitar problemas com o filtro
            df_filtrado = df[df['disciplina_#bimestre'].str.contains(disciplina, case=False, na=False)]
            if not df_filtrado.empty:
                media = df_filtrado['nota'].mean()
                media_da_turma[turma] = media

        # Se for a primeira disciplina (idx == 0) fica visível, senao só na legenda
        visibilidade = True if idx == 0 else 'legendonly'

        # Adiciona a linha ao gráfico
        fig.add_trace(go.Scatter(
            x=list(media_da_turma.keys()),
            y=list(media_da_turma.values()),
            mode='lines+markers',
            name=disciplina,
            visible=visibilidade 
        ))

    # Ajustes do layout
    fig.update_layout(
        title='Média das Notas por Disciplina ao Longo dos Anos',
        xaxis_title='Ano',
        yaxis_title='Média das Notas',
        template=template,
        xaxis=dict(showline=True, showgrid=True, zeroline=False),
        yaxis=dict(showline=True, showgrid=True, zeroline=False),
        showlegend=True,  # Certifique-se de que a legenda seja mostrada        
        title_x=0.5,
        title_y=0.9
    )
    return fig

# (PG 2)
#definindo uma cor padrão para determinada disciplina, facilitando comparação ao trocar de turma:
# paleta de cores qualitative do Plotly
cores_plotly = px.colors.qualitative.Plotly

# dicionário para mapear disciplinas a cores
disciplina_colors = dict(zip(disciplinas, cores_plotly))

def plot_medias_disciplina_por_turma(sub_dataframes, turma, tema):
    """
    gráfico de barras horizontais das médias anuais das notas por disciplina para uma turma específica. 
    (utiliza a média das 'médias das notas finais' dos estudantes daquela turma)

    As barras são coloridas de acordo com a disciplina, usando uma paleta de cores qualitativas do Plotly.

    """
    # Validação de entrada
    if not isinstance(sub_dataframes, dict):
        raise ValueError("sub_dataframes deve ser um dicionário.")
    if tema not in ['light', 'dark']:
        raise ValueError("O tema deve ser 'light' ou 'dark'.")
    if turma not in sub_dataframes:
        raise ValueError(f"A turma '{turma}' não foi encontrada no dicionário de DataFrames.")
    
    # Verifica se as colunas necessárias estão presentes
    required_columns = ['disciplina_#bimestre', 'nota']
    for df in sub_dataframes.values():
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Os DataFrames devem conter as colunas: {required_columns}")

    # Definir template e cor das anotações com base no tema
    template = 'plotly_dark' if tema == 'dark' else 'plotly'
    #annotation_color = "white" if tema == 'dark' else "black"


    # Filtra o DataFrame da turma especificada
    df_turma = sub_dataframes[turma]

    # Calcula as médias das notas para cada disciplina (independentemente do bimestre)
    df_turma['disciplina'] = df_turma['disciplina_#bimestre'].str.extract(r'(\D+)')
    
    # Calcula as médias das notas para cada disciplina
    medias_por_disciplina = df_turma.groupby('disciplina')['nota'].mean().sort_values()


    fig = go.Figure()

    # Adiciona as barras ao gráfico
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

    # Configura o layout do gráfico
    fig.update_layout(
        title=f'Média das Notas por Disciplina para a Turma {turma}',
        xaxis_title='Média das Notas',
        yaxis_title='Disciplina',
        template=template,  # Alterar para outro tema, se necessário
        xaxis=dict(showline=True, showgrid=True, zeroline=False),
        yaxis=dict(showline=True, showgrid=True, zeroline=False),        
        title_x=0.5,
        title_y=0.9
    )
    return fig


#plot  iterativo  com plotly (PG 3)
def plot_boxplot_com_interatividade(sub_dataframes, disciplina, tema):
    """
    boxplot interativo das notas por turma para uma disciplina específica.

    O boxplot exibe a distribuição das notas, incluindo pontos individuais e as médias de cada turma.
    e o tema (claro ou escuro).

    """


    # validação de entrada
    if not isinstance(sub_dataframes, dict):
        raise ValueError("sub_dataframes deve ser um dicionário.")
    if tema not in ['light', 'dark']:
        raise ValueError("O tema deve ser 'light' ou 'dark'.")

    # verificar se as colunas necessárias existem 
    required_columns = ['disciplina_#bimestre', 'turma', 'nota']
    for df in sub_dataframes.values():
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Os DataFrames devem conter as colunas: {required_columns}")


    # Definir template e cor das anotações com base no tema
    template = 'plotly_dark' if tema == 'dark' else 'plotly'
    #annotation_color = "white" if tema == 'dark' else "black"

    # pra combinar todos os DataFrames em um único DF
    combined_df = pd.concat(sub_dataframes.values())
    
    # filtra o DataFrame para a disciplina e bimestre desejados
    filtered_df = combined_df[combined_df['disciplina_#bimestre'].str.contains(disciplina)]
    
    # criando o boxplot com plotly
    fig = px.box(
        filtered_df,
        x='turma',
        y='nota',
        points="all",  # adiciona pontos individuais para visualização detalhada
        title=f'Boxplot das Notas para {disciplina}',
        labels={'nota': 'Nota', 'turma': 'Ano'}
    )
    
    # checar a média para cada grupo (ano)
    for ano in filtered_df['turma'].unique():
        media_nota = filtered_df[filtered_df['turma'] == ano]['nota'].mean()
        fig.add_trace(
            go.Scatter(
                x=[ano],
                y=[media_nota],
                mode='markers',
                marker=dict(color='Blue', size=5),
                text=[f'Média: {media_nota:.2f}'],
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
    O gráfico de linhas exibe as médias das notas por turma para cada bimestre, além de poder alternar a visibilidade dos bimestres e filtrar por uma disciplina por vez.
    O bimestre com a média mais baixa é destacado como "bimestre crítico". 
    (o valor é obtido calculando as médias das notas por bimestre (média global) e selecionando o com a menor média)

    """
    
    # validação de entrada
    if not isinstance(sub_dataframes, dict):
        raise ValueError("sub_dataframes deve ser um dicionário.")
    if tema not in ['light', 'dark']:
        raise ValueError("O tema deve ser 'light' ou 'dark'.")

    # Verifica se as colunas necessárias estão presentes
    required_columns = ['disciplina_#bimestre', 'turma', 'nota']
    for df in sub_dataframes.values():
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Os DataFrames devem conter as colunas: {required_columns}")

    
    # Definir template e cor das anotações com base no tema
    template = 'plotly_dark' if tema == 'dark' else 'plotly'
    annotation_color = "white" if tema == 'dark' else "black"


    # Cria uma figura vazia
    fig = go.Figure()

    # Dicionário para armazenar as médias de cada bimestre
    medias_bimestres = {}

    for idx, bimestre in enumerate(bimestres):
        disciplina_bimestre = f'{disciplina}{bimestre}'
        
        # Dicionário para armazenar médias das notas por ano
        media_por_turma = {}
        
        for turma, df in sub_dataframes.items():
            # Filtrar o dataframe para a disciplina e bimestre especificados
            df_filtrado = df[df['disciplina_#bimestre'] == disciplina_bimestre]
            # Calcular a média das notas
            media = df_filtrado['nota'].mean()
            # Armazenar a média no dicionário
            media_por_turma[turma] = media
        
        # Definir visibilidade com base no índice: visível para o primeiro bimestre e 'legendonly' para os outros
        visibility = True if idx == 0 else 'legendonly'
        
        # Adiciona uma linha para o bimestre
        fig.add_trace(go.Scatter(
            x=list(media_por_turma.keys()),
            y=list(media_por_turma.values()),
            mode='lines+markers',
            name=f'Bimestre {bimestre}',
            visible=visibility
        ))

        # Armazenar a média global do bimestre
        medias_bimestres[bimestre] = sum(media_por_turma.values()) / len(media_por_turma)

    # Identificar o bimestre com a média mais baixa
    bimestre_critico = min(medias_bimestres, key=medias_bimestres.get)
    media_bimestre_critico = medias_bimestres[bimestre_critico]

    # Atualiza o layout do gráfico
    fig.update_layout(
        title=f'Média das Notas para {disciplina.upper()} por Bimestre ao Longo dos Anos',
        xaxis_title='Ano',
        yaxis_title='Média das Notas',        
        title_x=0.5,
        title_y=0.9,
        legend_title='Bimestres',
        template=template,  # Tema escuro, pode ser ajustado conforme preferir
        annotations=[
            go.layout.Annotation(
                text=f'Bimestre mais crítico: Bimestre {bimestre_critico} com média {media_bimestre_critico:.2f}',
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

    O boxplot exibe a distribuição das notas, incluindo pontos individuais e as médias de cada turma.
    """
    # Validação de entrada
    if not isinstance(sub_dataframes, dict):
        raise ValueError("sub_dataframes deve ser um dicionário.")
    if tema not in ['light', 'dark']:
        raise ValueError("O tema deve ser 'light' ou 'dark'.")

    # Verifica se as colunas necessárias estão presentes
    required_columns = ['disciplina_#bimestre', 'nota', 'turma']
    for df in sub_dataframes.values():
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Os DataFrames devem conter as colunas: {required_columns}")


    # Definir template e cor das anotações com base no tema
    template = 'plotly_dark' if tema == 'dark' else 'plotly'
    #annotation_color = "white" if tema == 'dark' else "black"

    # Nome da coluna específica para a disciplina e bimestre
    disciplina_bimestre = f'{disciplina}{bimestre}'

    # Combina todos os DataFrames em um único DataFrame
    combined_df = pd.concat(sub_dataframes.values())

    # Filtra o DataFrame para a disciplina e bimestre desejados
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

    # Adiciona anotações de média para cada grupo (ano)
    for ano in filtered_df['turma'].unique():
        media_nota = filtered_df[filtered_df['turma'] == ano]['nota'].mean()
        fig.add_trace(
            go.Scatter(
                x=[ano],
                y=[media_nota],
                mode='markers',
                marker=dict(color='blue', size=8),
                text=[f'Média: {media_nota:.2f}'],
                textposition='top center',
                showlegend=False
            )
        )

    # Configura o layout da figura para a interatividade e estilo
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
    Função q gera o heatmap das médias das notas por disciplina e bimestre.

    exibe as médias das notas para cada disciplina e bimestre, permitindo identificar
    padrões e bimestres críticos (com médias mais baixas).

    """
    
    # Validação de entrada
    if not isinstance(sub_dataframes, dict):
        raise ValueError("sub_dataframes deve ser um dicionário.")
    if tema not in ['light', 'dark']:
        raise ValueError("O tema deve ser 'light' ou 'dark'.")

    # Verifica se as colunas necessárias estão presentes
    required_columns = ['disciplina_#bimestre', 'nota']
    for df in sub_dataframes.values():
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Os DataFrames devem conter as colunas: {required_columns}")


    # Definir template e cor das anotações com base no tema
    template = 'plotly_dark' if tema == 'dark' else 'plotly'
    #annotation_color = "white" if tema == 'dark' else "black"


    # lista para armazenar as médias por disciplina e bimestre
    dados_heatmap = []

    # para cada disciplina, calcular a média para cada bimestre
    for disciplina in disciplinas:
        for bimestre in range(1, 5):  # 4 bimestres
            disciplina_bimestre = f'{disciplina}{bimestre}'
            medias_bimestres = []
            
            # pegar as médias de cada turma para a disciplina e bimestre
            for turma, df in sub_dataframes.items():
                df_filtrado = df[df['disciplina_#bimestre'] == disciplina_bimestre]
                media = df_filtrado['nota'].mean()
                medias_bimestres.append(media)
            
            # media geral para essa disciplina e bimestre ao longo dos anos
            media_geral = sum(medias_bimestres) / len(medias_bimestres) if medias_bimestres else None
            dados_heatmap.append({'disciplina': disciplina, 'bimestre': bimestre, 'media': media_geral})
    
    # Converter para DataFrame
    df_heatmap = pd.DataFrame(dados_heatmap)

    # usar o pivot com argumentos pro heatmap - criando a tabela
    df_pivot = df_heatmap.pivot(index='disciplina', columns='bimestre', values='media')

    # plotar o Heatmap
    try:
        fig = px.imshow(df_pivot,
                        title='Média das Notas por Disciplina e Bimestre',
                        labels={'color': 'Média das Notas'},
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
        return go.Figure()  # retornar o gráfico vazio em caso de erro
    

# pperfil

# (PP 1)
def plot_histogram_idade_turma(sub_dataframes, tema):
    """
    grafico histograma interativo com a distribuição de idades dos alunos por turma.
    (ideia utilizada no PNAIC)
    
    """

    # Validação de entrada
    if not isinstance(sub_dataframes, dict):
        raise ValueError("sub_dataframes deve ser um dicionário.")
    if tema not in ['light', 'dark']:
        raise ValueError("O tema deve ser 'light' ou 'dark'.")


    # Verifica se as colunas necessárias estão presentes
    required_columns = ['index', 'idade', 'turma']
    for df in sub_dataframes.values():
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Os DataFrames devem conter as colunas: {required_columns}")


    # Definir template e cor das anotações com base no tema
    template = 'plotly_dark' if tema == 'dark' else 'plotly'
    #annotation_color = "white" if tema == 'dark' else "black"

    try:
        # Combina todos os DataFrames em um único DataFrame
        combined_df = pd.concat(sub_dataframes.values())
        
        # Remove duplicatas com base na coluna 'index' para garantir que cada aluno é contado apenas uma vez
        combined_df_unique = combined_df.drop_duplicates(subset='index')
        
        fig = go.Figure()

        # Adiciona um gráfico de barras para cada turma
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
        
        # Configura o layout da figura
        fig.update_layout(
            title='Distribuição das Idades por Turma',
            xaxis_title='Idade',
            yaxis_title='Quantidade de Alunos',
            barmode='group',  # Agrupa as barras para comparação
            template=template,  # ou 'plotly_white', dependendo da preferência
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
    boxplot interativo mostrando a distribuição das idades dos alunos por turma.
    """

    # Validação de entrada
    if not isinstance(sub_dataframes, dict):
        raise ValueError("sub_dataframes deve ser um dicionário.")
    if tema not in ['light', 'dark']:
        raise ValueError("O tema deve ser 'light' ou 'dark'.")

    # Verifica se as colunas necessárias estão presentes
    required_columns = ['index', 'idade', 'turma']
    for df in sub_dataframes.values():
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Os DataFrames devem conter as colunas: {required_columns}")


    # Definir template e cor das anotações com base no tema
    template = 'plotly_dark' if tema == 'dark' else 'plotly'
    #annotation_color = "white" if tema == 'dark' else "black"

    try:    
        # Combina todos os DataFrames em um único DataFrame
        combined_df = pd.concat(sub_dataframes.values())

        # Remove duplicatas com base na coluna 'index' para garantir que cada aluno é contado apenas uma vez
        combined_df_unique = combined_df.drop_duplicates(subset='index')

        # Cria o boxplot com Plotly Express
        fig = px.box(
            combined_df_unique,
            x='turma',
            y='idade',
            points="all",  
            title='Boxplot das Idades por Turma',
            labels={'idade': 'Idade', 'turma': 'Ano'}
        )

        # Adiciona anotações de média para cada grupo (ano)
        for ano in combined_df_unique['turma'].unique():
            media_idade = combined_df_unique[combined_df_unique['turma'] == ano]['idade'].mean()
            fig.add_trace(
                go.Scatter(
                    x=[ano],
                    y=[media_idade],
                    mode='markers',
                    marker=dict(color='blue', size=5),
                    text=[f'Média: {media_idade:.2f}'],
                    textposition='top center',
                    showlegend=False
                )
            )

        # Configura a interatividade do gráfico
        fig.update_traces(
            marker=dict(color='blue', size=8),  # Configura o estilo dos pontos no boxplot
            selector=dict(mode='markers+text')
        )

        fig.update_layout(
            xaxis_title='Ano',
            yaxis_title='Idade',
            template=template,  # Mantém o mesmo template
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

    # Validação de entrada
    if not isinstance(sub_dataframes, dict):
        raise ValueError("sub_dataframes deve ser um dicionário.")

    # Verifica se as colunas necessárias estão presentes
    required_columns = ['index', 'disciplina_#bimestre', 'nota']
    for df in sub_dataframes.values():
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Os DataFrames devem conter as colunas: {required_columns}")


    # Dicionário para armazenar a taxa de aprovação por turma
    aprovacao_por_turma = {}

    # Iterar sobre o dicionário de DataFrames
    for ano, df in sub_dataframes.items():
        # Filtrar e agrupar os dados por aluno e disciplina para calcular a média final
        medias_finais = df.groupby(['index', df['disciplina_#bimestre'].str[:-1]])['nota'].mean().reset_index()

        # Contar o número total de alunos na turma
        total_alunos = df['index'].nunique()

        # Contar o número de alunos aprovados (nota média ≥ 6)
        aprovados = medias_finais[medias_finais['nota'] >= 6]['index'].nunique()

        # Calcular a taxa de aprovação
        taxa_aprovacao = (aprovados / total_alunos) * 100

        # Armazenar a taxa de aprovação no dicionário
        aprovacao_por_turma[ano] = taxa_aprovacao
    
    return aprovacao_por_turma

# funcao plot 
def plot_alunos_e_taxa_aprovacao(sub_dataframes, tema):
    """
    gráfico de barras interativo que exibe a quantidade de alunos e a taxa de aprovação por turma.

    possui um eixo Y para a quantidade de alunos e um eixo Y secundário para a taxa de aprovação.
    As barras são coloridas com um gradiente azul baseado na taxa de aprovação.
    
    """

    # Validação de entrada
    if not isinstance(sub_dataframes, dict):
        raise ValueError("sub_dataframes deve ser um dicionário.")
    if tema not in ['light', 'dark']:
        raise ValueError("O tema deve ser 'light' ou 'dark'.")
    
    # Verifica se as colunas necessárias estão presentes
    required_columns = ['turma', 'index']
    for df in sub_dataframes.values():
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Os DataFrames devem conter as colunas: {required_columns}")

    # Definir template e cor das anotações com base no tema
    template = 'plotly_dark' if tema == 'dark' else 'plotly'
    #annotation_color = "white" if tema == 'dark' else "black"


    # Combina todos os DataFrames em um único DataFrame
    combined_df = pd.concat(sub_dataframes.values())
    
    # Calcular a quantidade de alunos únicos por turma (ano)
    alunos_por_turma = combined_df.groupby('turma')['index'].nunique()
    
    # Calcular a taxa de aprovação por turma (ano)
    taxa_aprovacao = calcular_taxa_aprovacao(sub_dataframes)
    
    taxa_aprovacao_values = [taxa_aprovacao.get(ano, 0) for ano in alunos_por_turma.index]
    
    # Ajuste dinâmico do colormap para evitar problemas com valores menores que 90%
    if taxa_aprovacao_values:  # Verifica se há dados
        norm = plt.Normalize(vmin=60, vmax=100)
        cmap = cm.get_cmap('Blues', 256)
        colors = cmap(norm(taxa_aprovacao_values))
        colors = ['rgba({}, {}, {}, 1.0)'.format(int(c[0]*255), int(c[1]*255), int(c[2]*255)) for c in colors]
    else:
        colors = ['blue'] * len(alunos_por_turma)  # Usa cor azul padrão caso não haja dados
    
    # Definir o intervalo do eixo Y
    max_alunos = alunos_por_turma.max()
    intervalo_max = max_alunos * 1.25 if max_alunos > 0 else 10  # Evita range zero

    fig = go.Figure()

    # Adicionar a barra com as quantidades de alunos e cores gradativas
    fig.add_trace(go.Bar(
        x=alunos_por_turma.index,
        y=alunos_por_turma.values,
        name='Quantidade de Alunos',
        marker=dict(color=colors, line=dict(color='black', width=1)),  # Adiciona bordas finas às barras
        text=['{:.1f}%'.format(taxa_aprovacao.get(ano, 0)) for ano in alunos_por_turma.index],
        textposition='inside',
        insidetextanchor='middle'
    ))

    # Configurar o layout do gráfico com dois eixos Y
    fig.update_layout(
        title='Quantidade de Alunos e Taxa de Aprovação por Ano',
        xaxis_title='Ano',
        xaxis=dict(
            tickvals=alunos_por_turma.index,  # Define as posições dos ticks no eixo x
            ticktext=[str(ano) for ano in alunos_por_turma.index],  # Define os rótulos dos ticks no eixo x
            title_standoff=20,  # Espaço entre o eixo e o título
            tickangle=-45  # Rotaciona os rótulos do eixo x
        ),
        yaxis=dict(
            title='Quantidade de Alunos',
            side='left',
            title_standoff=20,  # Espaço entre o eixo e o título
            range=[0, intervalo_max],  # Intervalo do eixo y ajustado
            dtick=5  # Define o espaçamento dos ticks do eixo y para 5 unidades
        ),
        yaxis2=dict(
            title='Taxa de Aprovação (%)',
            side='right',
            overlaying='y',
            range=[0, 100],  # Intervalo para a taxa de aprovação de 0 a 100%
            title_standoff=20,  # Espaço entre o eixo e o título
            anchor='x',  # Garante que o eixo y2 se alinhe com o eixo x
            showgrid=False  # Desativa a grade para o eixo y2
        ),
        template=template,  # Configura o tema do gráfico para escuro
        barmode='group',  # Para agrupar barras de alunos e taxa de aprovação
        margin=dict(l=40, r=20, t=40, b=100),  # Ajusta as margens do gráfico
        title_x=0.5,
        #title_y=0.9, 
    )
    return fig

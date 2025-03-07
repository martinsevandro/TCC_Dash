# import libs 
import pandas as pd


def processa_dados():
    
    # import dataset
    df = pd.read_csv("../../datasets/brutos/Dataset_Boletim_Completo.csv", sep=";", encoding="latin1")

    # informações iniciais do dataset

    #     
    df.head()

    #
    df.info()

    ## mostrando apenas turma, nascimento, pois são as únicas numéricas
    df.describe()

    # Verificar se existe algum valor ausente
    df.isnull().values.any()

    # Verificar se existe algum valor NaN
    df.isna().sum()

    #region formatacao
    # renomeando colunas
    #df.columns
    dataset_cols = ["turma", "idade", "gen", 
                    "cien1", "cien2", "cien3", "cien4", "geog1", "geog2", "geog3","geog4", 
                    "hist1", "hist2", "hist3", "hist4", "reli1", "reli2", "reli3", "reli4", 
                    "arte1", "arte2", "arte3", "arte4", "edfi1", "edfi2", "edfi3", "edfi4", 
                    "ingl1", "ingl2", "ingl3", "ingl4", "port1", "port2", "port3", "port4", 
                    "mate1", "mate2", "mate3", "mate4"]
    df.columns = dataset_cols

    
    # binarizando a coluna genero
    # colocando tudo minusculo:
    df['gen'] = df['gen'].str.lower()
    
    # Mapear valores 'm' para 0 e 'f' para 1
    df['gen'] = df['gen'].map({'m': 0, 'f': 1})

    # Mudando as notas com virgula para ponto e mudando seu tipo object para float
    df = df.apply(lambda col: col.str.replace(',', '.').astype(float) if col.dtype == 'object' else col)
    #df
    
    # calculando idade dos alunos
    df['idade'] = df.apply(lambda row: row['turma'] - row['idade'], axis=1).astype(int)
    #df

    # quaisquer alterações feitas em df_horizontal não afetam o DataFrame original df
    df_horizontal = df.copy()

    # df_horizontal.head()

    # Exportando o dataset horizontal - util para predições com séries temporais
    df_horizontal.to_csv('../../datasets/processados/df_horizontal.csv', index=False)

    # Criando coluna index para representar cada aluno
    df = df.reset_index()
    # df

    # definindo o index que não será usado na stack
    df = df.set_index(["index", "turma", "gen", "idade"])

    # verificando o novo index e a parte restante pré stack
    #df

    #region stack: verticalizar dataset
    df = df.stack().reset_index().rename(columns={"level_4":"disciplina_#bimestre",
                                                    0:"nota"})
    #df

    # dicionário de sub-dataframes usando groupby
    sub_dataframes = {name: group for name, group in df.groupby("turma")}
    sub_dataframes

    # o df da primeira turma no dicionario
    df_primeira_turma = next(iter(sub_dataframes.values()))
    df_primeira_turma
    
    # As 9 disciplinas = remover os números e coletar os valores únicos 
    disciplinas = list(set(df_primeira_turma['disciplina_#bimestre'].apply(lambda x: ''.join(filter(str.isalpha, x)))))
    disciplinas

    # Verificar tipos das informações e espaço em memoria
    df.info(memory_usage="deep")

    #Exportando o dicionario de dataframes
    import pickle
    file_path = "../../datasets/processados/sub_dataframes.pkl"

    with open(file_path, 'wb') as file:
        pickle.dump(sub_dataframes, file)

if __name__ == "__main__":
    processa_dados()
   


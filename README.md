# Projeto TCC - Análise de Dados com Dash

Este projeto permite visualizar e analisar dados de forma interativa utilizando o Dash e Plotly. O aplicativo foi desenvolvido com Python e utiliza bibliotecas como Pandas, Plotly e Scikit-learn.

## Requisitos

Certifique-se de ter as seguintes ferramentas instaladas em seu sistema:

- [Python 3.12+](https://www.python.org/downloads/)
- [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) (Opcional, mas recomendado para gerenciar dependências)

## Passo a Passo para Instalação e Execução

1. **Clone este repositório:**

   ```
   git clone https://github.com/martinsevandro/tcc_dash.git
   cd tcc_dash
   ```

2. Instale o ambiente Conda:

   Caso não tenha o Conda instalado, siga o link disponível na seção *Requisitos* para instalá-lo.

3. Crie e ative o ambiente Conda:

    Basta rodar o comando abaixo para criar o ambiente:
      ```
      conda env create -f environment.yml
      ```
    Depois de criado, ative o ambiente:
      ```
      conda activate novo_ambiente_tcc
      ```
    Caso prefira usar apenas o `<pip>` para instalar as dependências, utilize o arquivo **requirements.txt**:
      ```
      pip install -r requirements.txt
      ```

4. Navegue até a pasta onde o arquivo `<app.py>` está localizado:
   ```
   cd src/app
   ```
5. Execute o aplicativo:

   Com o ambiente ativo e dentro da pasta `</src/app>`, execute o comando:
      ```
      python app.py
      ```
6. Acesse o aplicativo:

   Abra o navegador e acesse o endereço:
     ```
     http://127.0.0.1:8050
     ```

     O aplicativo estará disponível e você poderá interagir com ele!

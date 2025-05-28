# Projeto APII

Projeto desenvolvido para a disciplina de Algoritimos e Programação II, com o intuito de desenvolver habilidades como:
* Organização de Projeto (Modularização)
* Paradigmas de Programação
* Persistência de Dados (Em arquivo ou Banco de Dados)
* Git/GitHub
* Trabalho em Equipe

### Objetivo do Projeto

Explorar as particularidades da Região Cariri, propondo uma solução inovadora e prática que contribua para o desenvolvimento do Cariri Cearense.

## Solução

Escolhemos trabalhar com o desenvolvimento de um jogo, que possibilita o aprimoramento de todas as habilidades destacadas anteriormente, além de destacar a importância do uso das diversas mídias para resgatar a cultura regional.

O jogo apresentará: personagens da história da região, elementos do cotidiano cearense, ambientação no cariri, etc.

| Objetivo  | Solução |
| ------------- | ------------- |
| Modularização  | Separation of Concerns (SoC)  |
| Paradigma  | Object-Oriented Programming (OOP)  |
| Dados  | SQLite  |
| Abordagem  | Criação de um jogo  |
| Objetivo  | Importância do uso das diversas mídias para resgatar a cultura regional  |

### Separation of Concerns (SoC)

Cada parte do código tem uma responsabilidade clara.

```
projeto/
|
|---main.py             #arquivo principal, iniciará o jogo e chamará as outras funções
|---settings.py         #Configurações globais
|
|---database/
|   |---weapons.py      #Persistência das informações
|
|---core/
|   |---game.py         #Lógica principal do jogo
|   |---events.py       #Manipulação dos eventos (Teclado, controle, sair do jogo, etc.)
|
|---entities/           #Classes dos objetos do jogo
|   |---player.py
|   |---enemy.py
|
|---utils/
|   |---assets.py       #Carrega imagens, sons, etc.
|
|---assets/             #Recursos do jogo
|   |---images\
|   |---sounds\
```

## Dependências/Ferramentas

- [UV](https://github.com/astral-sh/uv): Gerenciador de ambiente de desenvolvimento e dependências do projeto
- [PyGame](https://www.pygame.org): Biblioteca para criação de jogos com python

## Instalação

Instale a ferramenta UV:

```bash
# macOS e Linux.
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```bash
# Windows.
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Copie o projeto no seu computador e vá para o diretório do projeto:

```bash
git clone https://github.com/w4ll-y/projeto-APII.git
cd projeto-APII
```

Sincronize as dependências:

```bash
uv sync
```

### Iniciar

Para iniciar o jogo, rode o comando:

```bash
uv run main.py
```


## Autores

- Heitor Gomes: 
- Erik Pinheiro: [@0Erik1](https://github.com/0Erik1)
- Laura Galvão: [@laura-galvao](https://github.com/laura-galvao)
- José Wallacy: [@W4ll-y](https://github.com/w4ll-y)
- Matheus da Silva: [@mate00ss](https://github.com/mate00ss)

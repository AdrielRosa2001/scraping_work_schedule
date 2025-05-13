# Scraping Work Schedule

Script destinado ao scraping dos dados referente a escala de trabalho na plataforma TTV da empresa TP.

## 💻 Pré-requisitos

Antes de começar, verifique se você atendeu aos seguintes requisitos:

- Você ter um projeto no google cloud e uma chave de API por meio de arquivo `.json` contendo suas credênciais de acesso para gerenciamento do seu google calendar. Caso ainda não tenha esse arquivo json, você pode seguir o seguinte tutórial: `https://www.youtube.com/watch?v=B2E82UPUnOY&t=1236s` _(do minuto 0:00 até o minuto 5:52 é ensinado a criar o projeto no google clound gratuitamente e baixar o arquivo `.json`)_.
- Você possui instalado em sua maquina o gerenciador de pacotes python `UV` caso não tenha, pode acessar o link de instalação da propria ASTRAL: `https://docs.astral.sh/uv/getting-started/installation/`
- Você ter uma máquina `Windows`. Para rodar em sistema Linux, talvez seja necessário um ajuste no código do selenium e na forma como o código salva os arquivos de token.

## ☕ Usando o Script

Para usar Scraping Work Schedule, siga estas etapas:

1 - Clone ou baixe um zip do repositório.

2 - No diretório raiz do repositório, crie um arquivo de variaveis de ambiente `.env` contendo os seguintes dados:

```
URL_LOGIN=https://<DOMINIO DA EMPRESA>/pt_BR/group/webstation/home
URL_SCHEDULE=https://<DOMINIO DA EMPRESA>/pt_BR/group/webstation/my-schedule?startDay=1250107&viewFormat=monthly
USERNAME_SCHEDULE=<SEU LOGIN DO TOTALVIEW>
PASSWORD_SCHEDULE=<SUA SENHA DO TOTALVIEW>
```

3 - Renomeie seu arquivo `.json` contendo as credênciais de acesso a API do google calendar para `credentials.json` e copie esse arquivo para o diretório raiz do projeto.

4 - Agora basta executar o comando:

```
uv run ./run_script_cli.py
```

Desse modo, o ambiente virtual será criado pelo UV, ja instalando todos os pacotes necessários e prosseguindo para execução do script, no qual deve ser realizado de acordo com a sequencia do menu.

<img src="medias_repo\example_exec.PNG" alt="Exemplo imagem">

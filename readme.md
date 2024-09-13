# Sistema de Faltas

Este projeto foi desenvolvido por **Gabriel**, estudante da **Uniararas FHO**. O sistema de faltas utiliza reconhecimento facial e RFID, e foi construído em Python, rodando em um ambiente virtual (venv).

## Requisitos

O projeto utiliza um ambiente virtual do Python. Para instalar o `venv` no seu sistema, siga as instruções abaixo:

### Arch Linux (via AUR)

```bash
yay -S python-venv
```

Windows
```bash
python -m pip install venv
```

### Iniciando o Projeto
1. Crie o ambiente virtual:
 
```bash
python -m venv embarcados
```

2. Ative o ambiente virtual:<br>
No Linux:

```bash
source /etc/bin/activate
```
No Windows:

```bash
(O Visual Studio Code inicia automaticamente o ambiente virtual no Windows/Linux).
```

3. Instale as bibliotecas necessárias:

```bash
python -m pip install -r requirements.txt
```

Nota: A biblioteca de reconhecimento facial é de um repositório do GitHub. No Windows, é necessário ter o CMake instalado e configurado no PATH para compilar.

Executando o Projeto

```
    Para iniciar o servidor, rode o script run.py na máquina desejada.
    Para os clientes, rode o script run.py nos dispositivos clientes.
```

O sistema verificará automaticamente a necessidade de criar as tabelas no banco de dados.

# TODO

⏹️ - Sistema para configuração inicial do projeto em JSON.<br>
⏹️ - Implementar sistema de multi-chamadas.<br>
⏹️ - Implementar sistema de matérias (a tabela já existe).<br>
⏹️ - Validação da presença (atualmente, só verifica se já foi registrada).

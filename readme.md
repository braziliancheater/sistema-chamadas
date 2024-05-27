# feito por gabriel
# uniararas fho - sistema de faltas
1. projeto e construido dentro do venv do python portanto para usar as libs instale
    venv

    **archlinux aur**:
    yay -S python-venv

    **windows:**
    python -m pip install venv

2. iniciar o projeto usando o virtual enviroment
    1. python -m venv embarcados

    2. source /etc/bin/activate
    
    * vscode inicializa sozinho o virtual env no windows/linux

3. instalar bibliotecas utilizadas pelo projeto
    python -m pip install -r requirements.txt
    * lib de reconhecimento facil e de uma repo do git, requer cmake instalado no windows (e o path devidamente configurado) para compilar

4. iniciando o projeto
    rodar o run.py do server na maquina desejada
    rodar o run.py do cliente nos clientes

    * o script verifica necessidade de criar as tabelas automaticamente

# TODO
    * sistema para configuração inicial do projeto em json
    * implementar o sistema de multi-chamadas
    * implementar sistema de materias (so tem a tabela)
    * não verificamos se a presença e valida, somente se ja foi registrada

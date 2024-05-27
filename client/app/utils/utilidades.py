import os
from colorama import init, Fore, Style

# inicializa o colorama
init(autoreset=True)

class Logger:
    """
    Uma classe para logar mensagens no terminal.
    """

    @staticmethod
    def log_sucesso(func, msg):
        print(f'{Fore.GREEN}[SUCESSO][{func}] {msg}{Style.RESET_ALL}')

    @staticmethod
    def log_erro(func, msg):
        print(f'{Fore.RED}[ERRO][{func}] {msg}{Style.RESET_ALL}')

    @staticmethod
    def log_aviso(func, msg):
        print(f'{Fore.YELLOW}[AVISO][{func}] {msg}{Style.RESET_ALL}')


class Utilidades(Logger):
    """
    Uma classe com métodos úteis para o sistema.
    """

    @staticmethod
    def mostar_logo():
        """
        Mostra o logo do sistema no terminal.
        """
        try:
            import subprocess
            
            def obter_branch_git() -> str:
                return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('ascii').strip()
        except ImportError:
            subprocess = None
            Utilidades.log_error(__name__, 'Erro ao importar o módulo subprocess')
        
        print('fho - sistema de presenças\n'
              f'cliente | git: {obter_branch_git()} | porta: 5001\n')

    @staticmethod
    def limpar_tela():
        """
        Limpa a tela do terminal.
        """
        try:
            os.system('cls' if os.name == 'nt' else 'clear')
        except Exception as e:
            Utilidades.log_warning(__name__, f'Erro ao limpar a tela: {e}')
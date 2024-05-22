import os

class Logs:
    def __init__(self) -> None:
        pass     
    
    @staticmethod
    def msg_sucesso(func, msg):
        print(f'[+][{func}] {msg}')
    
    @staticmethod
    def msg_erro(func, msg):
        print(f'[-][{func}] {msg}')
        
    @staticmethod
    def msg_aviso(func, msg):
        print(f'[~][{func}] {msg}')
    
class Utilidades:
    @staticmethod
    def logo():
        print(f'fho - sistema de presencas\n\
              servidor | versão 2.0 | base: homologação\n')
    
    @staticmethod
    def limpa():
        try:
            # Tente limpar a tela
            os.system('cls' if os.name == 'nt' else 'clear')
        except Exception as e:
            # Em caso de erro, imprima uma mensagem de aviso
            Logs.aviso(__name__, f'Erro ao limpar a tela: {e}')

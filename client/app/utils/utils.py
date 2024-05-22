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
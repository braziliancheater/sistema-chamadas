from main import os

class logs:     
    def sucesso(msg):
        print(f'[+] {msg}')
    
    def erro(msg):
        print(f'[-] {msg}')
        
    def aviso(msg):
        print(f'[~] {msg}')
    
class utils:
    def logo():
        print(f'sistema de presença - backend\nversão: 1.0 | base: HOMOLOGAÇÃO')
    
    def limpa():
        # e windows?
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
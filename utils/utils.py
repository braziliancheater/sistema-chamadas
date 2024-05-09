import os

class logs:     
    def sucesso(msg):
        print(f'[+] {msg}')
    
    def erro(msg):
        print(f'[-] {msg}')
        
    def aviso(msg):
        print(f'[~] {msg}')
    
class utils:
    def logo():
        print(f'                                            .__  .__               __            \n\
                _________.__. ______   ____ |  | |__| ____   _____/  |_  ____    \n\
                /  ___<   |  |/  ___/ _/ ___\|  | |  |/ __ \ /    \   __\/ __ \  \n\
                \___ \ \___  |\___ \  \  \___|  |_|  \  ___/|   |  \  | \  ___/  \n\
               /____  >/ ____/____  >  \___  >____/__|\___  >___|  /__|  \___  >\n\
                    \/ \/         \/       \/             \/     \/          \/ \n\
              versão 2.0 | base: homologação\n')
    
    def limpa():
        # e windows?
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
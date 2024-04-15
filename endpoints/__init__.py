import os
import importlib

# obtem o caminho absouluto do diretorio atual
current_dir = os.path.dirname(os.path.abspath(__file__))

# obtem todos os arquivos no diretorio atual
items = os.listdir(current_dir)

# faz um loop para obter todos os arquivos de todas as subpastas desta
for item in items:
    item_path = os.path.join(current_dir, item)
    
    # verifica se e uma pasta
    if os.path.isdir(item_path):
        folder_files = [f for f in os.listdir(item_path) if f.endswith(".py")] # tem o final como .py?
        
        # importa tudo
        for file in folder_files:
            module_name = f"endpoints.{item}.{file[:-3]}"
            importlib.import_module(module_name)
            print('Endpoint ' + file + ' importado com sucesso.')
print("") # Pula linha
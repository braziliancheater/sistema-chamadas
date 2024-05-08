import os
from app import criar_sistema

#config_name = os.getenv('FLASK_CONFIG')
app = criar_sistema()

if __name__ == '__main__':
    app.run()
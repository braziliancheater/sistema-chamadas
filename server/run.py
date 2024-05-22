import os
from app import criar_sistema

app = criar_sistema()

app.run(debug=True, port=5000)
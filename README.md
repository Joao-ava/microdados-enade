# microdados-enade

## Instalar

O projeto requer Python 3.10 ou superior.

```sh
python -m venv venv
source venv/bin/activate  # Linux/macOS
# .\venv\Scripts\Activate.ps1  # Windows PowerShell
pip install -r requirements.txt
```

## Comandos

### Baixar dados

```sh
python enade/commands.py --download
```

Os microdados ficam em `data/2021/` e o dicionário de variáveis do INEP (com manual e questionários) em `data/2021_leia-me/`.

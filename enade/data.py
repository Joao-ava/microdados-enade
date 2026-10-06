import shutil
import requests
from os import makedirs
from pathlib import Path
from zipfile import ZipFile
from tempfile import TemporaryDirectory


CURRENT_PATH = Path(__file__).parent
DATA_PATH = CURRENT_PATH / '..' / 'data'

ENADE_DADOS_URL = 'http://download.inep.gov.br/microdados/microdados_enade_2023.zip'
ENADE_DICIO_URL = 'http://download.inep.gov.br/microdados/microdados_censo_da_educacao_superior_2023.zip'


def download_file(url: str, destionation: str | Path):
    response = requests.get(url, stream=True, timeout=60 * 3)
    response.raise_for_status()

    with open(destionation, 'wb') as file:
        idx = 0
        for chunk in response.iter_content(chunk_size=8192):
            print(f'\r{idx}', end='')
            idx += 1
            if chunk:
                file.write(chunk)

    print('')


def download_curso_dict():
    content_path = DATA_PATH / 'MICRODADOS_CADASTRO_CURSOS_2023.csv'
    if content_path.exists():
        return

    with TemporaryDirectory() as temp_dir:
        directory = Path(temp_dir)

        temp_file = directory / 'file_dict.zip'
        download_file(ENADE_DICIO_URL, temp_file)

        with ZipFile(temp_file) as zip_file:
            zip_file.extractall(directory)

        data_file = directory / 'microdados_censo_da_educacao_superior_2023' / 'dados' / 'MICRODADOS_CADASTRO_CURSOS_2023.CSV'

        if not DATA_PATH.exists():
            makedirs(DATA_PATH)

        shutil.copy(data_file, content_path)


def download_data():
    content_path = DATA_PATH / '2023'
    if content_path.exists():
        return

    with TemporaryDirectory() as temp_dir:
        directory = Path(temp_dir)

        temp_file = directory / 'file.zip'
        download_file(ENADE_DADOS_URL, temp_file)

        with ZipFile(temp_file) as zip_file:
            zip_file.extractall(directory)

        print(list(directory.glob('*')))
        data_dir = directory / 'Microdados_Enade_2023' / 'DADOS'
        data_dir.copy(content_path)


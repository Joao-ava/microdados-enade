import shutil
import requests
from os import makedirs
from pathlib import Path
from zipfile import ZipFile
from tempfile import TemporaryDirectory


CURRENT_PATH = Path(__file__).parent
DATA_PATH = CURRENT_PATH / '..' / 'data'

ENADE_DADOS_URL = 'http://download.inep.gov.br/microdados/microdados_enade_2021.zip'
ENADE_DICIO_URL = 'http://download.inep.gov.br/microdados/microdados_censo_da_educacao_superior_2021.zip'


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
    content_path = DATA_PATH / 'MICRODADOS_CADASTRO_CURSOS_2021.csv'
    if content_path.exists():
        return

    with TemporaryDirectory() as temp_dir:
        directory = Path(temp_dir)

        temp_file = directory / 'file_dict.zip'
        download_file(ENADE_DICIO_URL, temp_file)

        with ZipFile(temp_file) as zip_file:
            zip_file.extractall(directory)

        extracted_path = directory / 'Microdados do Censo da Educaç╞o Superior 2021' / 'dados'
        data_files = [
            extracted_path / 'MICRODADOS_CADASTRO_CURSOS_2021.CSV',
            extracted_path / 'MICRODADOS_CADASTRO_IES_2021.CSV',
        ]

        if not DATA_PATH.exists():
            makedirs(DATA_PATH)

        for data_file in data_files:
            shutil.copy(data_file, DATA_PATH / data_file.name)


def download_data():
    content_path = DATA_PATH / '2021'
    if content_path.exists():
        return

    with TemporaryDirectory() as temp_dir:
        directory = Path(temp_dir)

        temp_file = directory / 'file.zip'
        download_file(ENADE_DADOS_URL, temp_file)

        with ZipFile(temp_file) as zip_file:
            zip_file.extractall(directory)

        data_dir = directory / 'microdados_Enade_2021_LGPD' / '2.DADOS'
        data_dir.copy(content_path)


def get_unifor_codes():
    """
    retorna os códigos da UNIFOR e do curso de Ciência da Computação
    :return: (UNIFOR_IES_CODE, COMPUTER_SCIENCE_CODE)
    """
    import pandas as pd

    course_codes = pd.read_csv(DATA_PATH / 'MICRODADOS_CADASTRO_CURSOS_2021.csv', encoding='ISO-8859-1', sep=';')
    universities = pd.read_csv(DATA_PATH / 'MICRODADOS_CADASTRO_IES_2021.CSV', encoding='ISO-8859-1', sep=';')
    courses = pd.merge(course_codes, universities, on='CO_IES')

    # Pegar código da UNIFOR
    UNIFOR_CO = courses[courses['SG_IES'] == 'UNIFOR']['CO_IES'].values[0]
    courses_in_unifor = courses[courses['CO_IES'] == UNIFOR_CO]

    # Pegar código de ciência da computação
    computer_science_like = courses_in_unifor['NO_CURSO'].str.contains('da computa', case=False, na=False)
    result = courses_in_unifor[computer_science_like][['NO_CURSO', 'CO_CURSO']]
    COMPUTER_SCIENCE_CODE = result['CO_CURSO'].values[0]

    return UNIFOR_CO, COMPUTER_SCIENCE_CODE

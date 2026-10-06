import argparse
import data


def main():
    parser = argparse.ArgumentParser(
        "enade",
        description="CLI simples para facilitar o acesso aos dados do enade"
    )
    parser.add_argument(
        "--download",
        action="store_true",
        help="Baixa os arquivos de dados e dicionário"
    )

    args = parser.parse_args()

    if args.download:
        print("Baixando dicionário de cursos...")
        data.download_curso_dict()
        print("Baixando microdados ENADE...")
        data.download_data()
        print("Download concluído!")
        return


if __name__ == '__main__':
    main()

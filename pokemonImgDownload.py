from datetime import datetime
from requests import get
from os import makedirs
from os.path import exists
from urllib.parse import urljoin
from pprint import pprint
from shutil import rmtree, copyfileobj

base_url = "https://pokeapi.co/api/v2/"
path = "download"

if exists(path):
    rmtree(path)
makedirs(path)


def download_file(name, url, *, path=path, type='png'):
    response = get(url, stream=True) # https://requests.readthedocs.io/en/latest/user/quickstart/#raw-response-content
    fname = f'{path}/{name}.{type}'
    with open(fname, 'wb') as file:
        copyfileobj(response.raw, file)
    return fname


def get_sprite_url(url, sprite='front_default'):
    return get(url).json()['sprites'][sprite]


def main():
    start_time = datetime.now()

    pokemons = get(urljoin(base_url, 'pokemon/?limit=10')).json()['results']
    image_url = {pokemon['name']: get_sprite_url(pokemon['url']) for pokemon in pokemons} # Ele está acessando os objetos do array chamado Pokemon, através da chave nome e url
    files = [download_file(name, url) for name, url in image_url.items()]
    time = datetime.now() - start_time

    print(f'Tempo total {time.total_seconds():.2f} segundos')
    pprint(files)


if __name__ == '__main__':
    main()

from datetime import datetime
from requests import get
from os import makedirs
from os.path import exists
from urllib.parse import urljoin
from shutil import rmtree, copyfileobj
from concurrent.futures.process import ProcessPoolExecutor
import multiprocessing as multi

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


def access_pokemons(pokemons):
    image_url = {pokemon['name']: get_sprite_url(pokemon['url']) for pokemon in pokemons} # Ele está acessando os objetos do array chamado Pokemon, através da chave nome e url
    [download_file(name, url) for name, url in image_url.items()]


def main():
    start_time = datetime.now()
    count_cores = multi.cpu_count()
    pokemons = get(urljoin(base_url, 'pokemon/?limit=10')).json()['results']
    with ProcessPoolExecutor(max_workers=count_cores) as execute:
       execute.submit(access_pokemons, pokemons)
    time_elapsed = datetime.now() - start_time
    print(f'Tempo total {time_elapsed.total_seconds():.2f} segundos')


if __name__ == '__main__':
    main()

import json
import os
import subprocess
from itertools import zip_longest
from typing import Iterable, List

from PIL import Image

from metadata_embedding_explorer.models import Embedding


def is_image(image_path: str) -> bool:
    try:
        Image.open(image_path)
    except OSError:
        print("NOT AN IMAGE: ", image_path)
        return False
    with open(image_path, 'rb') as img_bin:
        check_chars = img_bin.read()[-2:]
        if check_chars != b'\xff\xd9':
            print("PREMATURE END OF JPEG: ", image_path)
            return False
    return True


def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def compute_embeddings(algorithm_container: str, host_path: str, image_paths: List[str],
                       chunk_size: int) -> Iterable[List[Embedding]]:
    container_paths = [
        '/data/' + image_path for image_path in image_paths if is_image(os.path.join(host_path, image_path))
    ]
    for chunk in grouper(container_paths, chunk_size):
        paths = [path for path in chunk if path]
        docker_command = ['docker', 'run', '-v', host_path + ':' + '/data', algorithm_container] + paths
        print("SPINNING UP DOCKER CONTAINER")
        output = subprocess.run(docker_command, stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
        print("DONE WITH DOCKER CONTAINER...")
        embeddings_list = json.loads(output)['faceVectors']
        print("LENGTH OF EMBEDDINGS LIST == LENGTH OF IMAGE_PATHS: ", len(embeddings_list) == len(paths))
        yield [
            Embedding(
                image_path=path.replace('/data/', '').replace('/', '__').replace('.thumb', ''),
                embedding=json.dumps(embedding)) for path, embeddings in zip(paths, embeddings_list)
            for embedding in embeddings
        ]

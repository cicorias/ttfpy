import json
from itertools import zip_longest
from typing import Iterable, List

from sklearn.metrics.pairwise import cosine_similarity

from metadata_embedding_explorer.database_manager import get_session
from metadata_embedding_explorer.models import Comparison, Embedding


def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def compute_comparisons(db_connection: str, chunk_size: int) -> Iterable[List[Comparison]]:
    session = get_session(db_connection)
    image_paths = []
    embeddings = []

    for model in session.query(Embedding).all():
        image_paths.append(model.image_path)
        embeddings.append(json.loads(model.embedding))

    offset = 0
    existing_comparisons = set()
    for chunked_embeddings in grouper(embeddings, chunk_size):
        emb_slice = [emb for emb in chunked_embeddings if emb]
        similarities = cosine_similarity(emb_slice, embeddings)
        comparisons = []
        for i in range(len(similarities)):
            for j in range(len(similarities[i])):
                if i != j:
                    this_comparison_indices = i + offset, j
                    that_comparison_indices = j, i + offset
                    if (this_comparison_indices not in existing_comparisons) and (that_comparison_indices not in existing_comparisons):
                        comparisons.append(Comparison(this_image_path=image_paths[i + offset],
                                                      that_image_path=image_paths[j],
                                                      cosine_similarity=similarities[i][j]))
                        existing_comparisons.add(this_comparison_indices)
                        existing_comparisons.add(that_comparison_indices)
        yield comparisons
        offset += len(emb_slice)

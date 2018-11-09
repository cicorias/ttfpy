import json
from typing import List

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from metadata_embedding_explorer.database_manager import get_session
from metadata_embedding_explorer.models import Comparison, Embedding


def compute_comparisons(db_connection: str) -> List[Comparison]:
    session = get_session(db_connection)
    embedding_models = session.query(Embedding).all()
    image_paths = []
    embeddings = []

    for model in embedding_models:
        image_paths.append(model.image_path)
        embeddings.append(np.array(json.loads(model.embedding)))
    embeddings = np.array(embeddings)

    similarities = cosine_similarity(embeddings, embeddings)
    return [
        Comparison(
            this_image_path=image_paths[i], that_image_path=image_paths[j], cosine_similarity=similarities[i][j])
        for i in range(len(image_paths)) for j in range(i + 1, len(image_paths))
    ]

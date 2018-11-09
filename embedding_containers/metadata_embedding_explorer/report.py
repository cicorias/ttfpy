from metadata_embedding_explorer.database_manager import get_session
from metadata_embedding_explorer.models import Comparison, Metadata


def generate_tsv_report(db_connection: str, output_fpath: str) -> None:

    session = get_session(db_connection)
    comparisons = session.query(Comparison, Metadata).filter(Comparison.this_image_path == Metadata.image_path).all()

    tsv = ''.join(
        '{}\t{}\t{}\n'.format(comparison.this_image_path, comparison.that_image_path, comparison.cosine_similarity)
        for comparison, _ in comparisons)
    with open(output_fpath, 'w', encoding='utf-8') as tsv_report:
        tsv_report.write(tsv)


if __name__ == '__main__':
    generate_tsv_report('sqlite:///sqlalchemy_example.db', 'embedding_metadata.tsv')

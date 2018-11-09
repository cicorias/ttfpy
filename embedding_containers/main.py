import os
from argparse import ArgumentParser, Namespace

from metadata_embedding_explorer.comparison import compute_comparisons
from metadata_embedding_explorer.database_manager import initialize_database, store_in_database
from metadata_embedding_explorer.embedding import compute_embeddings
from metadata_embedding_explorer.metadata import compute_metadata
from metadata_embedding_explorer.report import generate_tsv_report


def _main(args: Namespace) -> None:
    print("INITIALIZING DATABASE")
    initialize_database(args.DB_CONNECTION)
    print("DATABASE INITIALIZED")

    print("COMPUTING METADATA")
    metadata = compute_metadata(args.XL_FILE_PATH, args.XL_SHEET_NAME)
    store_in_database(args.DB_CONNECTION, metadata)
    print("METADATA IN DATABASE")

    print("COMPUTING EMBEDDINGS")
    for i, embeddings in enumerate(
            compute_embeddings(args.ALGORITHM_CONTAINER, args.IMAGE_DIR_PATH, os.listdir(args.IMAGE_DIR_PATH),
                               args.CHUNK_SIZE)):
        if embeddings:
            store_in_database(args.DB_CONNECTION, embeddings)
            print("ITERATION {} OF EMBEDDINGS, USING CHUNK_SIZE {} IN DATABASE".format(i, args.CHUNK_SIZE))
    print("EMBEDDINGS IN DATABASE")

    if args.SHOULD_COMPUTE_COMPARISONS:
        print("COMPUTING COMPARISONS")
        comparisons = compute_comparisons(args.DB_CONNECTION)
        store_in_database(args.DB_CONNECTION, comparisons)
        print("COMPARISONS IN DATABASE")

    if args.TSV_REPORT_FILE_PATH:
        print("GENERATING REPORT")
        generate_tsv_report(args.DB_CONNECTION, args.TSV_REPORT_FILE_PATH)
        print("REPORT GENERATED")


def _validate_parsed_args(args: Namespace) -> None:
    if args.TSV_REPORT_FILE_PATH and not args.SHOULD_COMPUTE_COMPARISONS:
        raise ValueError("TSV_REPORT_FILE_PATH specified, but SHOULD_COMPUTE_COMPARISONS is false. \
To generate the report, comparisons are required")


def _parse_arguments() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument('--DB_CONNECTION', type=str, required=True, help='database connection string.')
    parser.add_argument('--XL_FILE_PATH', type=str, required=True, help='path to excel metadata.')
    parser.add_argument('--XL_SHEET_NAME', type=str, required=True, help='name of sheet in excel metadata')
    parser.add_argument('--IMAGE_DIR_PATH', type=str, required=True, help='path to images to vectorize')
    parser.add_argument('--CHUNK_SIZE', type=int, required=True, help='amount of images to vectorize at once.')
    parser.add_argument('--ALGORITHM_CONTAINER', type=str, required=True, help='facenet or insightface')
    parser.add_argument(
        '--SHOULD_COMPUTE_COMPARISONS',
        type=bool,
        required=True,
        help='should compute comparisons and store in database')
    parser.add_argument(
        '--TSV_REPORT_FILE_PATH',
        type=str,
        required=False,
        help='tsv report file path, if you want to generate tsv report')
    return parser.parse_args()


def _cli() -> None:
    args = _parse_arguments()
    _validate_parsed_args(args)
    _main(args)


if __name__ == '__main__':
    _cli()

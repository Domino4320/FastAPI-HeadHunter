from pathlib import Path
import argparse


def create_folder_with_structure():
    parser = argparse.ArgumentParser(
        description="Script for auto generation of packages which works with tables in Db"
    )
    parser.add_argument("folder_name", help="name of a package")
    parser.add_argument(
        "--path", default=None, help="Optional path, default path is upper directory"
    )
    args = parser.parse_args()
    BASE_DIR = Path(__file__).resolve().parent.parent
    folder_path = (
        Path(args.path) / args.folder_name if args.path else BASE_DIR / args.folder_name
    )

    folder_path.mkdir()
    for file in (
        "__init__.py",
        "crud.py",
        "schemas.py",
        "routes.py",
    ):
        full_path = folder_path / file
        full_path.touch()


if __name__ == "__main__":
    create_folder_with_structure()

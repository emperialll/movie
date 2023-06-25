from storage_json import StorageJson
from storage_csv import StorageCsv
from movie_app import MovieApp
import argparse


# The main function which is being executed upon running the program
def main() -> None:
    """
    This function runs the Movie App, which provides a menu to interact with
    a movie database. It prompts the user to choose functions for managing
    movies and performs the corresponding actions.

    Command-line arguments:
    file_path (str): Path to the storage file (JSON or CSV)

    Returns: None
    """
    # Create an instance of ArgumentParser
    parser = argparse.ArgumentParser(description='Movie App')

    # Define the command-line argument
    parser.add_argument('file_path',
                        help='Path to the storage file (JSON or CSV)')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Access the value of the parsed argument
    file_path = args.file_path

    if file_path.endswith('.json'):
        storage = StorageJson(file_path)
        movie_app = MovieApp(storage)
        movie_app.run()
    elif file_path.endswith('.csv'):
        storage = StorageCsv(file_path)
        movie_app = MovieApp(storage)
        movie_app.run()
    else:
        print('Invalid file type. Only JSON or CSV files are supported.')


if __name__ == "__main__":
    main()

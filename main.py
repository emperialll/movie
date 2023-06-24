from storage_json import StorageJson
from storage_csv import StorageCsv
from movie_app import MovieApp
import argparse


# The main function which is being executed upon running the program
def main() -> None:
    """
    This function constantly shows the movie menu and asking user to choose
    his/her preferred function and thereafter calls the respective function
    :return: None
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

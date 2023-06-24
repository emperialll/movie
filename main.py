from storage_json import StorageJson
from storage_csv import StorageCsv
from movie_app import MovieApp
import sys


# The main function which is being executed upon running the program
def main() -> None:
    """
    This function constantly shows the movie menu and asking user to choose
    his/her preferred function and thereafter calls the respective function
    :return: None
    """
    # storage = StorageJson('movies.json')
    # movie_app = MovieApp(storage)
    # movie_app.run()
    arg = sys.argv[1]
    if 'json' in arg:
        storage = StorageJson(arg)
        movie_app = MovieApp(storage)
        movie_app.run()
    elif 'csv' in arg:
        storage = StorageCsv(arg)
        movie_app = MovieApp(storage)
        movie_app.run()


if __name__ == "__main__":
    main()

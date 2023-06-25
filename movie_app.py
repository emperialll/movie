# Movie menu display dictionary
MENU: dict = {
    0: 'Exit',
    1: 'List movies',
    2: 'Add movie',
    3: 'Delete movie',
    4: 'Update movie',
    5: 'Stats',
    6: 'Random movie',
    7: 'Search movie',
    8: 'Movies sorted by rating',
    9: 'Generate website'
}


class MovieApp:
    def __init__(self, storage):
        self._storage = storage

    def _command_list_movies(self):
        movies = self._storage.list_movies()
        for movie in movies:
            print(f'{movie["title"]}, Rating: {movie["rating"]}, '
                  f'Released: {movie["year"]}')

    def _command_add_movies(self, title):
        self._storage.add_movie(title)

    def _command_delete_movies(self, title):
        self._storage.delete_movie(title)

    def _command_update_movies(self, title, note):
        self._storage.update_movie(title, note)

    def _command_movie_stats(self):
        self._storage.stats()

    def _command_movie_random(self):
        self._storage.random_movie()

    def _command_search(self, title):
        self._storage.search_movie(title)

    def _command_movie_sort(self):
        self._storage.movies_sorted_by_rating()

    def _command_webpage_generator(self):
        self._storage.generate_website()

    def run(self):
        """
        Runs the MovieApp program, displaying the movie menu and executing
        user-selected commands.

        The function repeatedly displays the movie menu and prompts the user
        to enter a choice (0-9). Based on the user's input, the corresponding
        command is executed to perform the desired operation.
        The program continues running until the user chooses to exit by
        entering '0'.

        Menu Options:
        0: Exit
        1: List movies
        2: Add movie
        3: Delete movie
        4: Update movie
        5: Stats
        6: Random movie
        7: Search movie
        8: Movies sorted by rating
        9: Generate website

        Raises:
            ValueError: If the user enters a non-integer choice.

        Returns:
            None
        """
        while True:
            print('\n********** My Movies Database **********\n\nMenu:')
            for key, val in MENU.items():
                print(f'{key}. {val}')
            user_choice = input('\nEnter your choice (0-9):\n')
            try:
                user_choice = int(user_choice)
                if user_choice == 0:
                    break
                elif user_choice == 1:
                    self._command_list_movies()
                elif user_choice == 2:
                    title = input('Enter the movie title:\n')
                    self._command_add_movies(title)
                elif user_choice == 3:
                    title = input('Enter the movie title:\n')
                    self._command_delete_movies(title)
                elif user_choice == 4:
                    title = input('Enter the movie title:\n')
                    note = input('Enter the movie note:\n')
                    self._command_update_movies(title, note)
                elif user_choice == 5:
                    self._command_movie_stats()

                elif user_choice == 6:
                    self._command_movie_random()
                elif user_choice == 7:
                    title = input('Enter the movie title:\n')
                    self._command_search(title)
                elif user_choice == 8:
                    self._command_movie_sort()
                elif user_choice == 9:
                    self._command_webpage_generator()
                else:
                    print(
                        'Invalid choice. Please select within the range 0 - 9')
            except ValueError:
                print('Please select within the range 0 - 9')

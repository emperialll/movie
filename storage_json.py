from istorage import IStorage
import requests
import json
import statistics
import random
import os


# OMDB API to get movie data
API: str = 'http://www.omdbapi.com/?apikey=6f0c3bf6&t='
# IMDB URL to redirect user to each movie IMDB page
IMDB: str = 'https://www.imdb.com/title/'
# The API to get country name from country code
COUNTRY_API: str = "https://restcountries.com/v3.1/name/"
FLAG_API: str = "https://flagsapi.com/"


class StorageJson(IStorage):
    def __init__(self, file_path):
        self.file_path = file_path

    def list_movies(self):
        """
        Returns a list of dictionaries that
        contains the movies information in the database.

        The function loads the information from the JSON
        file and returns the data.

        For example, the function may return:
        {
            "Titanic": {
            "rating": 9,
            "year": 1999
            },
            "..." {
            ...
            },
        }
        """
        if not os.path.exists(self.file_path):
            # Create the file if it doesn't exist
            with open(self.file_path, 'w') as handler:
                handler.write(json.dumps([]))  # Write an empty dictionary

        with open(self.file_path, 'r') as handler:
            movies_data = handler.read()
            movies = json.loads(movies_data)
        return movies

    def add_movie(self, title):
        """
        Adds a movie to the movies' database.
        Loads the information from the JSON file, add the movie,
        and saves it. The function doesn't need to validate the input.
        """
        try:
            response = requests.get(API + title)
            response.raise_for_status()
            movie_dict_data = json.loads(response.text)
            movies = self.list_movies()
            movies.append({'title': movie_dict_data['Title'],
                           'rating': float(movie_dict_data['imdbRating']),
                           'year': int(movie_dict_data['Year']),
                           'poster': movie_dict_data['Poster'],
                           'imdbID': movie_dict_data['imdbID'], 'note': '',
                           'country': movie_dict_data['Country']})
            json_object = json.dumps(movies, indent=4)  # Serializing json
            with open(self.file_path, "w") as outfile:  # Writing to movie.json
                outfile.write(json_object)
        except KeyError:
            print("The movie not found")
        except requests.exceptions.HTTPError as errh:
            print("HTTP Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print("Error:", err)

    def delete_movie(self, title):
        """
        Deletes a movie from the movies' database.

        Loads the movie information from the JSON file, searches for movies
        matching the given title, and deletes them from the database.
        If multiple movies match the title, the user is prompted to enter the
        complete movie name for deletion. The updated movie database is then
        saved.

        Args:
            title (str): The title of the movie(s) to delete.

        Raises:
            FileNotFoundError: If the JSON file is not found.
            PermissionError: If there is a permission issue while accessing or
            modifying the file.
            json.JSONDecodeError: If the JSON file contains invalid data.
            IOError: If there is an error reading or writing the JSON file.

        Returns:
            None
        """
        try:
            movies = self.list_movies()
            target_movies_for_deletion = []
            for movie in movies:
                if title in movie['title']:
                    target_movies_for_deletion.append(movie)

            if len(target_movies_for_deletion) == 1:  # If only one movie found
                movies.remove(target_movies_for_deletion[0])
                json_object = json.dumps(movies, indent=4)  # Serializing json
                with open(self.file_path,
                          "w") as outfile:  # Writing to movie.json
                    outfile.write(json_object)
                print(
                    f'\nThe movie "{target_movies_for_deletion[0]["title"]}" '
                    f'has been removed from the movie list successfully.')
                return

            elif len(target_movies_for_deletion) == 0:  # If no movie found
                print("The movie was not found.")

            else:  # If more than one movie found
                print(f'{len(target_movies_for_deletion)} movies '
                      f'with "{title}" found: ')
                for movie in target_movies_for_deletion:
                    print(movie['title'])
                new_title = input('Please enter the complete movie name: ')
                for movie in movies:
                    if new_title == movie['title']:
                        movies.remove(movie)
                        json_object = json.dumps(movies,
                                                 indent=4)  # Serializing json
                        with open(self.file_path,
                                  "w") as outfile:  # Writing to movie.json
                            outfile.write(json_object)
                        print(
                            f'\nThe movie "{new_title}" has been removed from '
                            f'the movie list successfully.')
                        return

            print(f'\nError: The movie "{title}" does not exist '
                  f'in the movie list.')

        except FileNotFoundError:
            print("Error: The JSON file was not found.")

        except PermissionError:
            print(
                "Error: Permission denied while accessing or "
                "modifying the file.")

        except json.JSONDecodeError:
            print("Error: The JSON file contains invalid data.")

        except IOError:
            print(
                "Error: There was an error reading or writing the JSON file.")

    def update_movie(self, title, note):
        """
        Updates a movie in the movies' database.

        Loads the movie information from the JSON file, searches for movies
        matching the given title, and updates their note with the provided
        value. If multiple movies match the title, the user is prompted to
        enter the complete movie name for the update. The updated movie
        database is then saved.

        Args:
            title (str): The title of the movie(s) to update.
            note (str): The new note for the movie(s).

        Raises:
            FileNotFoundError: If the JSON file is not found.
            PermissionError: If there is a permission issue while accessing or
            modifying the file.
            json.JSONDecodeError: If the JSON file contains invalid data.
            IOError: If there is an error reading or writing the JSON file.

        Returns:
            None
        """
        try:
            movies = self.list_movies()
            target_movies_for_update = []
            for movie in movies:
                if title in movie['title']:
                    target_movies_for_update.append(movie)

            if len(target_movies_for_update) == 0:  # If no movie found
                print("The movie was not found.")

            elif len(target_movies_for_update) == 1:  # If only one movie found
                val_list = list(target_movies_for_update[0].values())
                for movie in movies:
                    if list(movie.values()) == val_list:
                        movie['note'] = note
                json_object = json.dumps(movies, indent=4)  # Serializing json
                with open(self.file_path,
                          "w") as outfile:  # Writing to movie.json
                    outfile.write(json_object)
                print(f'\nMovie "{title}" successfully updated.')
                return

            else:  # If multiple movies found
                print(f'{len(target_movies_for_update)} movies '
                      f'with "{title}" found: ')
                for movie in target_movies_for_update:
                    print(movie['title'])
                new_title = input('Please enter the complete movie name: ')
                for movie in movies:
                    if new_title == movie['title']:
                        movie['note'] = note
                        json_object = json.dumps(movies,
                                                 indent=4)  # Serializing json
                        with open(self.file_path,
                                  "w") as outfile:  # Writing to movie.json
                            outfile.write(json_object)
                        print(f'\nMovie "{new_title}" successfully updated.')
                        return

            print(f'\nError: The movie "{title}" does not exist '
                  f'in the movie list.')

        except FileNotFoundError:
            print("Error: The JSON file was not found.")

        except PermissionError:
            print(
                "Error: Permission denied while accessing or "
                "modifying the file.")

        except json.JSONDecodeError:
            print("Error: The JSON file contains invalid data.")

        except IOError:
            print(
                "Error: There was an error reading or writing the JSON file.")

    # Function to report statistical information
    def stats(self):
        """
        Prints statistical data for the movies in the movie list.

        This function calculates and displays the following statistical
        information about the movies:
        - The average movie rating
        - The median movie rating
        - The best movie(s) with the highest rating
        - The worst movie(s) with the lowest rating

        Raises:
            FileNotFoundError: If the JSON file is not found.
            PermissionError: If there is a permission issue while accessing
            the file.
            json.JSONDecodeError: If the JSON file contains invalid data.
            IOError: If there is an error reading the JSON file.

        Returns:
            None
        """
        try:
            value_list = []
            best_movie = []
            worst_movie = []
            movies = self.list_movies()
            for movie in movies:
                value_list.append(movie['rating'])

            highest_rate = max(value_list)
            lowest_rate = min(value_list)
            for movie in movies:
                if movie['rating'] == highest_rate:
                    best_movie.append(movie['title'])
                elif movie['rating'] == lowest_rate:
                    worst_movie.append(movie['title'])

            average_rating = statistics.mean(value_list)
            median_rating = statistics.median(value_list)

            print(f'The average movie rating is {average_rating}.')
            print(f'The median movie rating is {median_rating}.')

            if len(best_movie) == 1:
                print(f'The best movie is: {best_movie[0]}.')
            else:
                print(f'The best movies are: {", ".join(best_movie)}')

            if len(worst_movie) == 1:
                print(f'The worst movie is: {worst_movie[0]}.')
            else:
                print(f'The worst movies are: {", ".join(worst_movie)}')

        except FileNotFoundError:
            print("Error: The JSON file was not found.")

        except PermissionError:
            print("Error: Permission denied while accessing the file.")

        except json.JSONDecodeError:
            print("Error: The JSON file contains invalid data.")

        except IOError:
            print("Error: There was an error reading the JSON file.")

    # This function allows user to pick a random movie
    def random_movie(self) -> None:
        """
        Prints a randomly selected movie from the movie list.

        This function selects a random movie from the list of movies and prints
         its title
        and rating in the terminal.

        Returns:
            None
        """
        try:
            movies = self.list_movies()
            movie = random.choice(movies)
            print(
                f'Your random movie is "{movie["title"]}" with '
                f'rating {movie["rating"]}')

        except FileNotFoundError:
            print("Error: The JSON file was not found.")

        except PermissionError:
            print("Error: Permission denied while accessing the file.")

        except json.JSONDecodeError:
            print("Error: The JSON file contains invalid data.")

        except IOError:
            print("Error: There was an error reading the JSON file.")

    # This function allows user to search for a movie by using a keyword
    def search_movie(self, title):
        """
        Searches for movies in the movie list using a keyword.

        This function takes a movie title keyword as input from the user and
        searches for all the movies in the list that contain the keyword.
        It prints the title and rating of each matching movie in the terminal.

        Args:
            title (str): The keyword to search for in movie titles.

        Returns:
            None
        """
        try:
            movies = self.list_movies()
            for movie in movies:
                if title.lower() in movie['title'].lower():
                    print(f'{movie["title"]}, {movie["rating"]}')

        except FileNotFoundError:
            print("Error: The JSON file was not found.")

        except PermissionError:
            print("Error: Permission denied while accessing the file.")

        except json.JSONDecodeError:
            print("Error: The JSON file contains invalid data.")

        except IOError:
            print("Error: There was an error reading the JSON file.")

    # This function sorts the movie list  with descending ratings
    def movies_sorted_by_rating(self):
        """
        Sorts and prints the movies in the movie list by rating in
        descending order.

        This function retrieves the movies from the list, sorts them based on
        their rating in descending order, and then prints the sorted list in
        the terminal. Each movie is displayed with its title and rating.

        Returns:
            None
        """
        try:
            movies = self.list_movies()
            sorted_movies = sorted(movies, key=lambda item: item['rating'],
                                   reverse=True)
            print(f'{len(sorted_movies)} movies in total\n')
            for movie in sorted_movies:
                print(f'{movie["title"]}, {movie["rating"]}')

        except FileNotFoundError:
            print("Error: The JSON file was not found.")

        except PermissionError:
            print("Error: Permission denied while accessing the file.")

        except json.JSONDecodeError:
            print("Error: The JSON file contains invalid data.")

        except IOError:
            print("Error: There was an error reading the JSON file.")

    # This function generates the html code for movie thumbnail
    def movie_thumbnail(self):
        """
        Generates HTML code for movie thumbnails using API data.

        This function retrieves the movie data from the list, calls an API
        to get the full country name from the country code, and generates HTML
        code for each movie thumbnail. The movie thumbnail includes the movie
        poster, IMDb rating, title, year, and flag representing the movie's
        country.

        Returns:
            movie_thumbnail_html (str): HTML code for the movie thumbnails.
        """
        try:
            movies = self.list_movies()
            movie_thumbnail_html = ''
            for movie in movies:
                imdb_url = IMDB + movie["imdbID"]
                if 'United States' in movie["country"]:
                    country = 'United States of America'
                elif ',' in movie["country"]:
                    country = movie["country"][:movie["country"].index(',')]
                else:
                    country = movie["country"]
                country_data_url = COUNTRY_API + country
                country_raw_data = requests.get(country_data_url)
                country_data = country_raw_data.json()
                country_code = country_data[0]["cca2"]
                flag_api_call = f'{FLAG_API}{country_code}/shiny/24.png'
                movie_tile_template = [
                    '<li>\n',
                    '<div class="movie">\n',
                    f'<div class="parent">\n',
                    f'<a href="{imdb_url}" target="blank">'
                    f'<img class="movie-poster" '
                    f'src="{movie["poster"]}" '
                    f'alt="{movie["title"]} poster image" '
                    f'title="{movie["note"]}"></a>\n',
                    f'<img class="flag" src="{flag_api_call}">\n',
                    '</div>\n',
                    f'<div class="score"> IMDB Rate: {movie["rating"]}</div>\n',
                    f'<div class="movie-title">{movie["title"]}</div>\n',
                    f'<div class="movie-year">{movie["year"]}</div>\n',
                    '</div>\n',
                    '</li>\n'
                ]

                for item in movie_tile_template:
                    movie_thumbnail_html += item
            return movie_thumbnail_html

        except FileNotFoundError:
            print("Error: The JSON file was not found.")

        except PermissionError:
            print("Error: Permission denied while accessing the file.")

        except json.JSONDecodeError:
            print("Error: The JSON file contains invalid data.")

        except requests.exceptions.RequestException:
            print("Error: Failed to connect to the API or retrieve data.")

        except KeyError:
            print("Error: Invalid data format received from the API.")

        except IndexError:
            print("Error: Country data not found for a movie.")

    # This function generate a html webpage
    def generate_website(self):
        """
        Generates a new webpage by incorporating movie thumbnails into a template.

        This function calls the `movie_thumbnail()` function to generate HTML code
        for movie thumbnails. It then includes the generated HTML code in a
        template file named `index_template.html` to create a new webpage named
        `build.html`. The webpage represents a grid of movie thumbnails.

        Returns:
            None

        Raises:
            FileNotFoundError: If the template file `index_template.html` is not found.
            PermissionError: If permission is denied while accessing the files.
        """
        try:
            template_movie_grid = self.movie_thumbnail()
            with open("./_static/index_template.html", "r") as handler:
                template_str = handler.read()
                output_str = template_str.replace('__TEMPLATE_MOVIE_GRID__',
                                                  f'{template_movie_grid}')
            with open("build.html", "w") as file_output:
                file_output.write(output_str)
            print('Website was generated successfully.')

        except FileNotFoundError:
            print(
                "Error: The template file 'index_template.html' was not found.")

        except PermissionError:
            print("Error: Permission denied while accessing the files.")

import json
import csv
import requests
import statistics
import random
from istorage import IStorage
import os

# OMDB API to get movie data
API: str = 'http://www.omdbapi.com/?apikey=6f0c3bf6&t='
# IMDB URL to redirect user to each movie IMDB page
IMDB: str = 'https://www.imdb.com/title/'
# The API to get country name from country code
COUNTRY_API: str = "https://restcountries.com/v3.1/name/"
FLAG_API: str = "https://flagsapi.com/"


class StorageCsv(IStorage):
    def __init__(self, file_path):
        self.file_path = file_path

    def list_movies(self):
        """
        Returns a list of dictionaries that
        contains the movies information in the database.

        The function loads the information from the CSV
        file and returns the data.

        For example, the function may return:
        [
            {
                "title": "Titanic",
                "rating": 9,
                "year": 1999
            },
            {
                ...
            }
        ]
        """
        movies = []
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w', newline='') as handler:
                writer = csv.writer(handler)
                writer.writerow(["Title", "Rating", "Year"])  # Write headers
                return movies

        with open(self.file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                movies.append(row)
        return movies

    def add_movie(self, title):
        """
        Adds a movie to the movies' database.
        Loads the information from the CSV file, adds the movie,
        and saves it. The function doesn't need to validate the input.
        """
        try:
            response = requests.get(API + title)
            response.raise_for_status()
            movie_dict_data = response.json()
            movies = self.list_movies()
            movies.append({
                'title': movie_dict_data['Title'],
                'rating': float(movie_dict_data['imdbRating']),
                'year': int(movie_dict_data['Year']),
                'poster': movie_dict_data['Poster'],
                'imdbID': movie_dict_data['imdbID'],
                'note': '',
                'country': movie_dict_data['Country']
            })
            fieldnames = movies[0].keys()
            with open(self.file_path, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(movies)
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

        Args:
            title (str): The title of the movie to delete.

        Raises:
            IOError: An error occurred while accessing the file.
            Exception: An error occurred during the deletion process.

        Notes:
            - The function loads the information from the CSV file, deletes the
             movie, and saves it.
            - If only one movie is found with the given title, it is deleted
            immediately.
            - If no movie is found, a message is printed indicating that the
            movie was not found.
            - If multiple movies are found with the given title, the user is
            prompted to enter the complete movie name for deletion.

        """
        try:
            movies = self.list_movies()
            target_movies_for_deletion = []
            for movie in movies:
                if title in movie['title']:
                    target_movies_for_deletion.append(movie)
            if len(target_movies_for_deletion) == 1:
                movies.remove(target_movies_for_deletion[0])
                fieldnames = movies[0].keys()
                with open(self.file_path, 'w', newline='') as file:
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(movies)
                print(
                    f'\nThe movie "{target_movies_for_deletion[0]["title"]}" '
                    f'has been removed from the movie list successfully.')
                return
            elif len(target_movies_for_deletion) == 0:
                print("The movie not found")
            else:
                print(
                    f'{len(target_movies_for_deletion)} movies with "{title}" '
                    f'found:')
                for movie in target_movies_for_deletion:
                    print(movie['title'])
                new_title = input('Please enter the complete movie name: ')
                for movie in movies:
                    if new_title == movie['title']:
                        movies.remove(movie)
                        fieldnames = movie.keys()
                        with open(self.file_path, 'w', newline='') as file:
                            writer = csv.DictWriter(file,
                                                    fieldnames=fieldnames)
                            writer.writeheader()
                            writer.writerows(movies)
                        print(
                            f'\nThe movie "{new_title}" has been removed from '
                            f'the movie list successfully.')
                        return
            print(
                f'\nError: The movie "{title}" does not exist in the '
                f'movie list.')
        except IOError:
            print("An error occurred while accessing the file.")
            raise
        except Exception as e:
            print(f"An error occurred during the deletion process: {str(e)}")
            raise

    def update_movie(self, title, note):
        """
        Updates a movie in the movies' database.
        Loads the information from the CSV file, updates the movie, and
        saves it.
        The function doesn't need to validate the input.

        Args:
            title (str): The title of the movie to update.
            note (str): The note or comment to add to the movie.
        """
        try:
            movies = self.list_movies()
            target_movies_for_update = []
            for movie in movies:
                if title in movie['title']:
                    target_movies_for_update.append(movie)
            if len(target_movies_for_update) == 0:
                print("The movie not found")
            elif len(target_movies_for_update) == 1:
                target_movie = target_movies_for_update[0]
                target_movie['note'] = note
                fieldnames = target_movie.keys()
                with open(self.file_path, 'w', newline='') as file:
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(movies)
                print(f'\nMovie "{title}" successfully updated')
                return
            else:
                print(f'{len(target_movies_for_update)} movies '
                      f'with "{title}" found: ')
                for movie in target_movies_for_update:
                    print(movie['title'])
                new_title = input('Please enter the complete movie name: ')
                for movie in movies:
                    if new_title == movie['title']:
                        movie['note'] = note
                        fieldnames = movie.keys()
                        with open(self.file_path, 'w', newline='') as file:
                            writer = csv.DictWriter(file,
                                                    fieldnames=fieldnames)
                            writer.writeheader()
                            writer.writerows(movies)
                        print(f'\nMovie "{new_title}" successfully updated')
                        return
            print(
                f'\nError: The movie "{title}" does not exist in '
                f'the movie list.'
            )
        except IOError:
            print("An error occurred while accessing the file.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def stats(self):
        """
        Prints statistical data of the movies in the movie list.

        The statistical data includes the best movie, worse movie,
        average rating, and median rating.

        Raises:
            ValueError: An error occurred while calculating the statistics.

        """
        try:
            value_list: list = []
            best_movie: list = []
            worst_movie: list = []
            movies: list = self.list_movies()
            for movie in movies:
                value_list.append(float(movie['rating']))
            highest_rate: float = max(value_list)
            lowest_rate: float = min(value_list)
            for movie in movies:
                if float(movie['rating']) == highest_rate:
                    best_movie.append(movie['title'])
                elif float(movie['rating']) == lowest_rate:
                    worst_movie.append(movie['title'])

            average_rating: float = statistics.mean(value_list)
            median_rating: float = statistics.median(value_list)
            print(f'The average movie rating is {average_rating}.')
            print(f'The median of movie ratings is {median_rating}.')
            if len(best_movie) == 1:
                print(f'The best movie is: {best_movie[0]}.')
            else:
                print(f'The best movies are: {", ".join(best_movie)}')

            if len(worst_movie) == 1:
                print(f'The worst movie is: {worst_movie[0]}.')
            else:
                print(f'The worst movies are: {", ".join(worst_movie)}.')
        except ValueError as e:
            print(
                f"An error occurred while calculating the "
                f"statistics: {str(e)}")
            raise

    def random_movie(self) -> None:
        """
        Picks a random movie from the movie list and prints its details.

        Raises:
            IndexError: The movie list is empty.

        """
        try:
            movies: list = self.list_movies()
            if len(movies) == 0:
                raise IndexError("The movie list is empty.")
            movie: dict = random.choice(movies)
            print(
                f'Your random movie is "{movie["title"]}" with '
                f'rating {movie["rating"]}.')
        except IndexError as e:
            print(f"An error occurred while picking a random movie: {str(e)}")
            raise

    def search_movie(self, title):
        """
        Prints all movies that match the given keyword.

        Args:
            title (str): The keyword to search for in movie titles.

        """
        try:
            movies: list = self.list_movies()
            for movie in movies:
                if title.lower() in movie['title'].lower():
                    print(f'{movie["title"]}, {movie["rating"]}')
        except Exception as e:
            print(f"An error occurred during the movie search: {str(e)}")
            raise

    # This function sorts the movie list  with descending ratings
    def movies_sorted_by_rating(self):
        """
        Prints the movies in the movie list sorted from highest to
        lowest rating.

        Raises:
            ValueError: An error occurred while sorting the movies.

        """
        try:
            movies: list = self.list_movies()
            sorted_movies: list = sorted(movies,
                                         key=lambda item: item['rating'],
                                         reverse=True)
            print(f'{len(sorted_movies)} movies in total\n')
            for movie in sorted_movies:
                print(f'{movie["title"]}, {movie["rating"]}')
        except ValueError as e:
            print(f"An error occurred while sorting the movies: {str(e)}")
            raise

    def movie_thumbnail(self):
        """
        Generates HTML code for the movie thumbnails based on the movie list.

        Returns:
            movie_thumbnail_html (str): The generated HTML code for movie
            thumbnails.

        Raises:
            requests.exceptions.RequestException: An error occurred while
            making an API call.
            json.JSONDecodeError: An error occurred while parsing the API
            response.

        """
        try:
            movies: list = self.list_movies()
            movie_thumbnail_html: str = ''
            for movie in movies:
                imdb_url: str = IMDB + movie["imdbID"]
                if 'United States' in movie["country"]:
                    country: str = 'United States of America'
                elif ',' in movie["country"]:
                    country: str = movie["country"][
                                   : movie["country"].index(',')]
                else:
                    country: str = movie["country"]
                country_data_url: str = COUNTRY_API + country
                country_raw_data = requests.get(country_data_url)
                country_data: list = country_raw_data.json()
                country_code: str = country_data[0]["cca2"]
                flag_api_call: str = f'{FLAG_API}{country_code}/shiny/24.png'
                movie_tile_template: list = [
                    '<li>\n',
                    '<div class = "movie">\n',
                    f'<div class="parent">\n',
                    f'<a href="{imdb_url}" target="blank">'
                    f'<img class="movie-poster" '
                    f'src="{movie["poster"]}" '
                    f'alt="{movie["title"]} poster image" '
                    f'title="{movie["note"]}"></a>\n',
                    f'<img class="flag" src="{flag_api_call}">\n',
                    '</div>\n',
                    f'<div class="score">IMDB Rate: {movie["rating"]}</div>\n',
                    f'<div class="movie-title">{movie["title"]}</div>\n',
                    f'<div class="movie-year">{movie["year"]}</div>\n',
                    '</div>\n',
                    '</li>\n'
                ]

                for item in movie_tile_template:
                    movie_thumbnail_html += item
            return movie_thumbnail_html
        except (requests.exceptions.RequestException,
                json.JSONDecodeError) as e:
            print(
                f"An error occurred while generating movie "
                f"thumbnails: {str(e)}")
            raise

    def generate_website(self):
        """
        Generates a new webpage named "build.html" using a template and
        movie thumbnails.

        Raises:
            FileNotFoundError: The template file could not be found.
            IOError: An error occurred while reading or writing the template
            or output file.

        """
        try:
            template_movie_grid = self.movie_thumbnail()
            with open("./_static/index_template.html", "r") as handler:
                template_str: str = handler.read()
                output_str: str = template_str.replace(
                    '__TEMPLATE_MOVIE_GRID__', f'{template_movie_grid}')
            with open("build.html", "w") as file_output:
                file_output.write(output_str)
            print('Website was generated successfully.')
        except FileNotFoundError as e:
            print(f"An error occurred while generating the website: {str(e)}")
            raise
        except IOError as e:
            print(
                f"An error occurred while reading or writing files: {str(e)}")
            raise

import csv
import requests
from istorage import IStorage
import os

# OMDB API to get movie data
API: str = 'http://www.omdbapi.com/?apikey=6f0c3bf6&t='
# IMDB URL to redirect user to each movie IMDB page
IMDB: str = 'https://www.imdb.com/title/'
# The API to get country name from country code
COUNTRY_API: str = "https://restcountries.com/v3.1/name/"


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
        Loads the information from the CSV file, deletes the movie,
        and saves it. The function doesn't need to validate the input.
        """
        movies = self.list_movies()
        target_movies_for_deletion = []
        for movie in movies:
            if title in movie['title']:
                target_movies_for_deletion.append(movie)
        if len(target_movies_for_deletion) == 1:  # If only one movie found
            movies.remove(target_movies_for_deletion[0])
            fieldnames = movies[0].keys()
            with open(self.file_path, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(movies)
            print(f'\nThe movie "{target_movies_for_deletion[0]["title"]}" '
                  f'has been removed from movie list successfully.')
            return
        elif len(target_movies_for_deletion) == 0:  # If no movie found
            print("The movie not found")
        else:  # If more than one movie found
            print(f'{len(target_movies_for_deletion)} movies '
                  f'with "{title}" found: ')
            for movie in target_movies_for_deletion:
                print(movie['title'])
            new_title = input('Please enter the complete movie name: ')
            for movie in movies:
                if new_title == movie['title']:
                    movies.remove(movie)
                    fieldnames = movie.keys()
                    with open(self.file_path, 'w', newline='') as file:
                        writer = csv.DictWriter(file, fieldnames=fieldnames)
                        writer.writeheader()
                        writer.writerows(movies)
                    print(f'\nThe movie "{new_title}" has been removed from '
                          f'movie list successfully.')
                    return
        print(f'\nError: The movie "{title}" does not exist '
              f'in the movie list.')

    def update_movie(self, title, note):
        """
        Updates a movie from the movies' database.
        Loads the information from the CSV file, updates the movie,
        and saves it. The function doesn't need to validate the input.
        """
        movies = self.list_movies()
        target_movies_for_update = []
        for movie in movies:
            if title in movie['title']:
                target_movies_for_update.append(movie)
        if len(target_movies_for_update) == 0:  # If no movie found
            print("The movie not found")
        elif len(target_movies_for_update) == 1:  # If only one movie found
            target_movie = target_movies_for_update[0]
            target_movie['note'] = note
            fieldnames = target_movie.keys()
            with open(self.file_path, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(movies)
            print(f'\nMovie "{title}" successfully updated')
            return
        else:  # If multiple movies found in movie list with the user's input
            print(
                f'{len(target_movies_for_update)} movies '
                f'with "{title}" found: '
            )
            for movie in target_movies_for_update:
                print(movie['title'])
            new_title = input('Please enter the complete movie name: ')
            for movie in movies:
                if new_title == movie['title']:
                    movie['note'] = note
                    fieldnames = movie.keys()
                    with open(self.file_path, 'w', newline='') as file:
                        writer = csv.DictWriter(file, fieldnames=fieldnames)
                        writer.writeheader()
                        writer.writerows(movies)
                    print(f'\nMovie "{new_title}" successfully updated')
                    return
        print(
            f'\nError: The movie "{title}" does not exist in the movie list.'
        )

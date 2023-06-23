from istorage import IStorage
import requests
import json
import statistics
import random


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
        Loads the information from the JSON file, deletes the movie,
        and saves it. The function doesn't need to validate the input.
        """
        movies = self.list_movies()
        target_movies_for_deletion = []
        for movie in movies:
            if title in movie['title']:
                target_movies_for_deletion.append(movie)
        if len(target_movies_for_deletion) == 1:  # If only one movie found
            movies.remove(target_movies_for_deletion[0])
            json_object = json.dumps(movies, indent=4)  # Serializing json
            with open("movies.json", "w") as outfile:  # Writing to movie.json
                outfile.write(json_object)
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
                    json_object = json.dumps(movies,
                                             indent=4)  # Serializing json
                    with open(self.file_path,
                              "w") as outfile:  # Writing to movie.json
                        outfile.write(json_object)
                    print(f'\nThe movie "{new_title}" has been removed from '
                          f'movie list successfully.')
                    return
        print(f'\nError: The movie "{title}" does not exist '
              f'in the movie list.')

    def update_movie(self, title, note):
        """
        Updates a movie from the movies' database.
        Loads the information from the JSON file, updates the movie,
        and saves it. The function doesn't need to validate the input.
        """
        movies = self.list_movies()
        target_movies_for_update = []
        for movie in movies:
            if title in movie['title']:
                target_movies_for_update.append(movie)
        if len(target_movies_for_update) == 0:  # If no movie found
            print("The movie not found")
        elif len(
                target_movies_for_update) == 1:  # If only one movie found
            val_list = list(target_movies_for_update[0].values())
            print(val_list)
            for movie in movies:
                if list(movie.values()) == val_list:
                    movie['note'] = note
                    print(movie)
            json_object = json.dumps(movies, indent=4)  # Serializing json
            with open(self.file_path, "w") as outfile:  # Writing to movie.json
                outfile.write(json_object)
            print(f'\nMovie {title} successfully updated')
            return
        else:  # If multiple movie found in movie list with the user's input
            print(
                f'{len(target_movies_for_update)} movies '
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
                    print(f'\nMovie {new_title} successfully updated')
                    return
        print(
            f'\nError: The movie "{title}" does not exist in the movie list.')

    # Function to report statistical information
    def stats(self):
        """
        This function prints the statistical data of the movies in the
        movie list. It includes the best movie, worse movie, average rating
        and median rate
        """
        value_list: list = []
        best_movie: list = []
        worst_movie: list = []
        movies: list = self.list_movies()
        for movie in movies:
            value_list.append(movie['rating'])

        highest_rate: float = max(value_list)
        lowest_rate: float = min(value_list)
        for movie in movies:
            if movie['rating'] == highest_rate:
                best_movie.append(movie['title'])
            elif movie['rating'] == lowest_rate:
                worst_movie.append(movie['title'])

        average_rating: float = statistics.mean(value_list)
        median_rating: float = statistics.median(value_list)
        print(f'The average movie rating is {average_rating}.')
        print(f'The median of movie rating is {median_rating}.')
        if len(best_movie) == 1:
            print(f'The best movie is: {best_movie[0]}.')
        else:
            # If multiple movies found with same rating
            print(f'The best movies are: {", ".join(best_movie)}')

        if len(worst_movie) == 1:
            print(f'The worst movie is: {worst_movie[0]}.')
        else:
            # If multiple movies found with same rating
            print(f'The worst movies are: {", ".join(worst_movie)}')

    # This function allows user to pick a random movie
    def random_movie(self) -> None:
        """
        Upon executing this function a random movie will be picked from movie
        list and gets printed in terminal
        """
        movies: list = self.list_movies()
        movie: dict = random.choice(movies)
        print(f'Your random movie is "{movie["title"]}" with '
              f'rating {movie["rating"]}')

    # This function allows user to search for a movie by using a keyword
    def search_movie(self, title):
        """
        This function gets a movie keyword from user and prints all the movies
        with the given keyword
        :param title: str
        :return: None
        """
        movies: list = self.list_movies()
        for movie in movies:
            if title.lower() in movie['title'].lower():
                print(f'{movie["title"]}, {movie["rating"]}')

    # This function sorts the movie list  with descending ratings
    def movies_sorted_by_rating(self):
        """
        Upon executing this function, the movies in movie list will be sorted
        from high to low and prints on terminal
        :return: None
        """
        movies: list = self.list_movies()
        sorted_movies: list = sorted(movies, key=lambda item: item['rating'],
                                     reverse=True)
        print(f'{len(sorted_movies)} movies in total\n')
        for movie in sorted_movies:
            print(f'{movie["title"]}, {movie["rating"]}')

    # This function generates the html code for movie thumbnail
    def movie_thumbnail(self):
        """
        This function calls the API to get the full country name from country
        code and generates html code for movie thumbnail to be used in template
        :return: movie_thumbnail_html str
        """
        movies: list = self.list_movies()
        movie_thumbnail_html: str = ''
        for movie in movies:
            imdb_url: str = IMDB + movie["imdbID"]
            if 'United States' in movie["country"]:
                country: str = 'United States of America'
            elif ',' in movie["country"]:
                country: str = movie["country"][: movie["country"].index(',')]
            else:
                country: str = movie["country"]
            country_data_url: str = COUNTRY_API + country
            country_raw_data = requests.get(country_data_url)
            country_data: list = country_raw_data.json()
            country_code: str = country_data[0]["cca2"]
            flag_api_call: str = f'{FLAG_API}{country_code}/shiny/24.png'
            movie_tile_template: list = ['<li>\n', '<div class = "movie">\n',
                                       f'<div class="parent">\n',
                                       f'<a href="{imdb_url}" target="blank">'
                                       f'<img class = "movie-poster" '
                                       f'src = "{movie["poster"]}" '
                                       f'alt = "{movie["title"]} poster image"'
                                       f' title = "{movie["note"]}"></a>\n',
                                       f'<img class="flag" '
                                       f'src="{flag_api_call}">\n',
                                       f'</div>\n',
                                       f'<div class = "score"> IMDB Rate: '
                                       f'{movie["rating"]}</div>\n',
                                       f'<div class = "movie-title">'
                                       f'{movie["title"]}</div>\n',
                                       f'<div class = "movie-year">'
                                       f'{movie["year"]}</div>\n', '</div>\n',
                                       f'</li>\n']

            for item in movie_tile_template:
                movie_thumbnail_html += item
        return movie_thumbnail_html

    # This function generate a html webpage
    def generate_website(self):
        """
        This function calls the function movie_thumbnail and include the movies
        ' html code in a template on a new webpage which is  named build.html
        :return: None
        """
        template_movie_grid= self.movie_thumbnail()
        with open("./_static/index_template.html", "r") as handler:
            template_str: str = handler.read()
            output_str: str = template_str.replace('__TEMPLATE_MOVIE_GRID__',
                                                   f'{template_movie_grid}')
        with open("build.html", "w") as file_output:
            file_output.write(output_str)
        print('Website was generated successfully.')
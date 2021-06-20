"""
This module contains the analisys of the books and films datasets.
It has 2 modes: the first one compares the chosen film to the books
for which this film is an adaptation if there are such or finds similar books.
The second mode gives book recommendations according to the genres and time frames chosen by user.
"""

import pandas as pd
title_basics = pd.read_csv('title.basics.tsv', sep= '\t', \
usecols= ['primaryTitle', 'titleType', 'tconst', 'startYear', 'genres'], \
dtype= {'primaryTitle': str, 'titleType': str, 'tconst': str, 'startYear': str, 'genres': str})
title_crew = pd.read_csv('title.crew.tsv', sep= '\t', usecols= ['tconst', 'writers'], \
dtype= {'tconst': str, 'writers': str})
title_principals = pd.read_csv('title.principals.tsv', sep= '\t', \
usecols= ['nconst', 'job'], dtype= {'nconst': str, 'job': str})
name_basics = pd.read_csv('name.basics.tsv', sep= '\t', \
usecols= ['nconst', 'primaryName'], dtype= {'nconst': str, 'primaryName': str})
book_titles = pd.read_csv('titles.csv')


def choose_mode() -> int:
    """
    Returns 1 or 2 - the mode of the app.
    >>> choose_mode() == 1 or choose_mode() == 2
    True
    """
    print('There are two modes of the app.\n\
The first one recommends books in relation to the entered film.\n\
The second one recommends books in relation to the chosen characteristics.\n')
    mode = input('Which mode would you like to choose?\nEnter 1 or 2.\n')
    while mode not in ('1', '2'):
        mode = input('Enter 1 or 2.\n')
    return int(mode)


def choose_film() -> str:
    """
    Returns the title of the chosen film.
    """
    film = input("Enter a film to see the books which served for the film adaptation.\n\
If the film is not an adaptation of any book, you will receive recommendations of \
similar to the film books.\n")
    return film


def film_identification(film_title: str) -> str:
    """
    Returns the film id of the film_title.
    If there is not one film with such title, there is a need to enter additional information.
    >>> len(film_identification('Alice in Wonderland'))
    9
    """
    films = title_basics[title_basics['primaryTitle'] == film_title]
    films = films[films['titleType'] == 'movie']
    ids = list(films['tconst'])
    if len(ids) > 1:
        release_year = input('Enter the release year of the film: ')
        films = films[films['startYear'] == release_year]
        ids = list(films['tconst'])
    if len(ids) > 1:
        print('Choose the film by its genres:')
        for ind, genre in enumerate(list(films['genres'])):
            print(f'{ind + 1}) {genre}')
        film_choice = int(input('Enter the number of the film: '))
        film_id = ids[film_choice - 1]
    elif len(ids) == 1:
        film_id = ids[0]
    else:
        print('There is no such film. Try again.')
        film_id = film_identification(choose_film())
    return film_id


def book_writer(film_id: str) -> list:
    """
    Returns the list of the ids of the book writers if the film with film_id is a book adaptation.
    >>> book_writer('tt1926979')
    ['nm2483359']
    >>> book_writer('tt1014759')
    ['nm0941314', 'nm0140902']
    """
    film_people = title_crew[title_crew['tconst'] == film_id]
    writers = list(film_people['writers'])
    writers_ids = ['Original film']
    if '\\N' not in writers:
        writers_ids = writers[0].split(',')
    return writers_ids


def adaptation_books(film_id: str) -> set:
    """
    Returns a set of all the books for which there are film adaptations.
    >>> adaptation_books('tt0004873') == {('Alice in Wonderland', 'Lewis Carroll'), \
('Through the Looking-Glass, and What Alice Found There', 'Lewis Carroll'), \
('Through the Looking Glass', 'Lewis Carroll'), \
('The Adventures of Alice in Wonderland', 'Lewis Carroll'), \
("Alice's Adventures in Wonderland", 'Lewis Carroll')}
    >>> len(adaptation_books('tt1014759'))
    7
    """
    books = []
    writers = book_writer(film_id)
    if writers != ['Original film']:
        for writer in writers:
            df_writer_name = name_basics[name_basics['nconst'] == writer]['primaryName']
            writer_name = list(df_writer_name)[0]
            writer_info = title_principals[title_principals['nconst'] == writer]
            book_works = list(writer_info[writer_info['job'].str.contains(pat = '"')]['job'])
            for book in book_works:
                new_books = book.split('"')
                for ind, elem in enumerate(new_books):
                    if ind % 2 == 1:
                        books.append((elem, writer_name))
    return set(books)


def film_genres(film_id: str) -> set:
    """
    Returns the genres of the film.
    >>> film_genres('tt0004873') == {'Family', 'Adventure', 'Fantasy'}
    True
    >>> film_genres('tt1926979')
    {'Documentary'}
    """
    film_info = title_basics[title_basics['tconst'] == film_id]
    df_genres = film_info['genres'].apply(lambda elem: elem.split(','))
    genres = set(list(df_genres)[0])
    return genres


def suitable_books(book_info: tuple) -> pd.DataFrame:
    """
    Returns a filtered book dataframe so that the needed information format there
    is the same as in the film dataframes.
    """
    book_title = book_info[0].upper()
    writer = book_info[1]
    upper_titles = book_titles['Title'].apply(lambda title: title.upper())
    books = book_titles[upper_titles == book_title]
    splitted_name = books['Name'].apply(lambda name: name.split(', ') \
if isinstance(name, str) else name)
    reversed_name = splitted_name.apply(lambda name: name[1] + ' ' + name[0] \
if isinstance(name, list) and len(name) > 1 else name)
    writer_books = books[reversed_name == writer]
    return writer_books


def book_genres(book_info: tuple) -> set:
    """
    Returns the genres of the book by its title and writer.
    >>> book_genres(('Through the looking-glass. Sambahsa', 'Lewis Carroll')) \
== {"Children's fiction", 'Fantasy'}
    True
    >>> book_genres(('Through the looking-glass', 'Lewis Carroll')) == {'Illustration', 'Fiction'}
    True
    """
    writer_books = suitable_books(book_info)
    genres = writer_books['Genre']
    genres_set = set()
    for elem in genres:
        if not isinstance(elem, float):
            genre_list = elem.split(' ; ')
            genres_set = set(genre_list)
    return genres_set


def genre_comparison(film_id: str, book_info: tuple) -> dict:
    """
    Returns the similarity of the book and the film and their common genres.
    >>> genre_comparison('tt0004873', ('Through the looking-glass', 'Lewis Carroll'))
    {0.0: set()}
    >>> genre_comparison('tt0004873', ('Alice in Wonderland', 'Lewis Carroll'))
    {0.2: {'Fantasy'}}
    """
    same_genres = film_genres(film_id) & book_genres(book_info)
    all_genres = film_genres(film_id) | book_genres(book_info)
    similarity = len(same_genres) / len(all_genres)
    genres_similarity = dict()
    genres_similarity.update({similarity: same_genres})
    return genres_similarity


def film_year(film_id: str) -> int:
    """
    Returns the release year of the film.
    >>> film_year('tt0004873')
    1915
    >>> film_year('tt1014759')
    2010
    """
    film_info = title_basics[title_basics['tconst'] == film_id]
    release = int(film_info['startYear'])
    return release


def book_year(book_info: tuple) -> int:
    """
    Returns the year of the book publication.
    >>> book_year(('Through the looking-glass', 'Lewis Carroll'))
    1893
    >>> book_year(('Alice in Wonderland', 'Lewis Carroll'))
    1907
    """
    writer_books = suitable_books(book_info)
    years = writer_books['Date of creation/publication']
    years = years[years.notna()].astype(int)
    return min(years) if years.any() else None


def year_comparison(film_id: str, book_info: tuple) -> int:
    """
    Returns the difference (in years) between the book publication and film release year.
    >>> year_comparison('tt0004873', ('Through the Looking-glass', 'Lewis Carroll'))
    22
    >>> year_comparison('tt0004873', ('Alice in Wonderland', 'Lewis Carroll'))
    8
    """
    film_release = film_year(film_id)
    book_publication = book_year(book_info)
    difference = (film_release - book_publication) if book_publication else None
    return difference


def comparison(film_id: str, books_from_films: set) -> None:
    """
    This is the comparison of the film and the books.
    The function prints the similarity in genres and the difference in years.
    """
    comparisons = dict()
    year_differences = set()
    for book in books_from_films:
        similarity_and_genres = genre_comparison(film_id, book)
        comparisons.update(similarity_and_genres)
        year_difference = year_comparison(film_id, book)
        if year_difference:
            year_differences.add(year_difference)
    max_similarity = max(comparisons.keys())
    print(f'The similarity between book and film genres is {round(max_similarity * 100)}%.')
    if max_similarity > 0:
        print(f'Similar genres are: {", ".join(comparisons[max_similarity])}')
    print(f'The film was released {max(year_differences)} years after the book was published.')


def books_time(start: int, end: int) -> set:
    """
    Returns books which where published between start and end.
    >>> books_time(1800, 1865) == {"An Index [by Charles Lutwidge Dodgson] to 'In Memoriam' \
[by Alfred Tennyson]", 'In Memoriam. Appendix', "Alice's adventures in Wonderland"}
    True
    """
    books = book_titles[book_titles['Date of creation/publication'].notna()]
    books = books[books['Date of creation/publication'].str.isdigit()]
    book_years = books['Date of creation/publication'].astype(int)
    suit_time = set(books[book_years.between(start, end)]['Title'])
    return suit_time


def similar_books(film_id: str) -> set:
    """
    Returns similar to the film books by checking their genres and publication years.
    """
    f_genres = film_genres(film_id)
    f_year = film_year(film_id)
    year_difference = int(input('What time difference between book creation and \
film release would be suitable for you (in years)?\n'))
    b_year = f_year - year_difference
    suit_genre = set()
    for genre in f_genres:
        all_book_genres = set(book_titles[book_titles['Genre'].str.contains(pat = genre, \
na = False)]['Title'])
        suit_genre = suit_genre | all_book_genres
    suit_time = books_time(b_year - 10, b_year + 10)
    sim_books = [book.lower().capitalize() for book in list(suit_time & suit_genre)]
    return set(sim_books)


def first_mode() -> None:
    """
    This if the first mode of the app. It gives the the books which served for the film adaptation
    or similar to film books if the film has no adaptation.
    """
    film_title = choose_film()
    film_id = film_identification(film_title)
    books_from_films = adaptation_books(film_id)
    if books_from_films:
        print(f'Here are the books for which this film is an adaptation:\n\
{books_from_films}')
        comparison(film_id, books_from_films)
    else:
        print('Unfortunately, this film is not an adaptation of a book. However, \
you may like the books which are similar to the film.')
        sim_books = similar_books(film_id)
        if sim_books:
            print(sim_books)
        else:
            print('There are no such books.')


def second_mode() -> None:
    """
    Gives the book recommendations according to the chosen genres and time period.
    """
    available_genres = book_titles[book_titles['Genre'].notna()]['Genre'].apply(lambda \
x: x.split(' ; '))
    all_genres = set()
    for genres in available_genres:
        for elem in genres:
            all_genres.add(elem)
    user_genres = set(input('Enter the genres you would like to read a book in \
(dividing with a comma):\n').split(','))
    possible_book_genres = all_genres & user_genres
    suitable_genres = set()
    for genre in possible_book_genres:
        suitable_genre = set(book_titles[book_titles['Genre'].str.contains(pat = genre, \
na = False)]['Title'])
        suitable_genres = suitable_genres | suitable_genre
    start_time = int(input('What time frames of the book creation would you like to have?\
\nStart year: '))
    end_time = int(input('End year: '))
    suit_time = books_time(start_time, end_time)
    recommendations = suit_time & suitable_genres
    if recommendations:
        recommended_books = [book.lower().capitalize() for book in \
list(recommendations)]
        print('Here are the books recommended to you:', set(recommended_books))
    else:
        print('There are no such books.')


def main_app() -> None:
    """
    This is the main function of the app.
    """
    mode = choose_mode()
    if mode == 1:
        first_mode()
    if mode == 2:
        second_mode()


if __name__ == "__main__":
    main_app()

"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 * Desarrollado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 """

import os
import csv
import time
import tracemalloc

from DataStructures.List import array_list as al
from DataStructures.Map import map_linear_probing as lp
from DataStructures.Map import map_separate_chaining as sc


data_dir = os.path.dirname(os.path.realpath('__file__')) + '/Data/GoodReads/'


def new_logic(load_factor=0.7):
    """
    Inicializa el catálogo de libros y crea las tablas de hash con el factor de carga indicado.
    """
    catalog = {
        "books": None,
        "books_by_id": None,
        "books_by_year_author": None,
        "books_by_authors": None,
        "tags": None,
        "book_tags": None
    }

    catalog['books'] = al.new_list()
    catalog['books_by_id'] = lp.new_map(1000, load_factor)
    catalog['books_by_authors'] = lp.new_map(1000, load_factor)
    catalog['tags'] = lp.new_map(1000, load_factor)
    catalog['book_tags'] = lp.new_map(1000, load_factor)
    catalog['books_by_year_author'] = lp.new_map(1000, load_factor)
    
    return catalog

# -------------------------------------------------------------
# Funciones para la carga de datos
# -------------------------------------------------------------

def load_data(catalog):
    """
    Carga los datos de los archivos y mide tiempo transcurrido y memoria utilizada.
    """
    start_time = getTime()
    tracemalloc.start()
    start_memory = getMemory()

    books, authors = load_books(catalog)
    tag_size = load_tags(catalog)
    book_tag_size = load_books_tags(catalog)

    stop_memory = getMemory()
    end_time = getTime()
    
    tiempo_transcurrido = deltaTime(end_time, start_time)
    memoria_usada = deltaMemory(start_memory, stop_memory)

    return books, authors, tag_size, book_tag_size, tiempo_transcurrido, memoria_usada


def load_books(catalog):
    booksfile = data_dir + "books.csv"
    input_file = csv.DictReader(open(booksfile, encoding='utf-8'))
    for book in input_file:
        add_book(catalog, book)
    return book_size(catalog), author_size(catalog)


def load_tags(catalog):
    tagsfile = data_dir + 'tags.csv'
    input_file = csv.DictReader(open(tagsfile, encoding='utf-8'))
    for tag in input_file:
        add_tag(catalog, tag)
    return tag_size(catalog)


def load_books_tags(catalog):
    bookstagsfile = data_dir + "book_tags.csv"
    input_file = csv.DictReader(open(bookstagsfile, encoding='utf-8'))
    for booktag in input_file:
        add_book_tag(catalog, booktag)
    return book_tag_size(catalog)


def new_tag(name, id):
    return {"name": name, "tag_id": id}


def new_book_tag(tag_id, book_id, count):
    return {'tag_id': tag_id, 'book_id': book_id, 'count': count}


# -----------------------------------------------   
# Funciones para agregar información al catálogo
# -----------------------------------------------

def add_book(catalog, book):
    al.add_last(catalog['books'], book)
    lp.put(catalog['books_by_id'], book['goodreads_book_id'], book)
    
    authors = book['authors'].split(",")
    for author in authors:
        author_name = author.strip()
        add_book_author(catalog, author_name, book)
        add_book_author_and_year(catalog, author_name, book)
    return catalog


def add_book_author(catalog, author_name, book):
    authors = catalog['books_by_authors']
    author_value = lp.get(authors, author_name)
    if author_value:
        al.add_last(author_value, book)
    else:
        authors_books = al.new_list()
        al.add_last(authors_books, book)
        lp.put(authors, author_name, authors_books)
    return catalog


def add_book_author_and_year(catalog, author_name, book):
    books_by_year_author = catalog['books_by_year_author']
    pub_year = book['original_publication_year'].strip()
    
    if not pub_year:
        pub_year = "Desconocido"

    author_map = lp.get(books_by_year_author, author_name)
    if author_map:
        year_list = lp.get(author_map, pub_year)
        if year_list:
            al.add_last(year_list, book)
        else:
            books_list = al.new_list()
            al.add_last(books_list, book)
            lp.put(author_map, pub_year, books_list)
    else:
        new_year_map = lp.new_map(100, 0.7)
        books_list = al.new_list()
        al.add_last(books_list, book)
        lp.put(new_year_map, pub_year, books_list)
        lp.put(books_by_year_author, author_name, new_year_map)
        
    return catalog


def add_tag(catalog, tag):
    t = new_tag(tag['tag_name'], tag['tag_id'])
    lp.put(catalog['tags'], tag['tag_name'], t)
    return catalog


def add_book_tag(catalog, book_tag):
    t = new_book_tag(book_tag['tag_id'], book_tag['goodreads_book_id'], book_tag['count'])
    book_tags_map = catalog['book_tags']
    
    if lp.contains(book_tags_map, t['tag_id']):
        tag_list = lp.get(book_tags_map, t['tag_id'])
        al.add_last(tag_list, t)
    else:
        new_tag_list = al.new_list()
        al.add_last(new_tag_list, t)
        lp.put(book_tags_map, t['tag_id'], new_tag_list)
        
    return catalog


# -------------------------------------------------------------
# Funciones de consulta
# -------------------------------------------------------------

def get_book_info_by_book_id(catalog, good_reads_book_id):
    start_time = getTime()
    tracemalloc.start()
    start_memory = getMemory()

    book = lp.get(catalog['books_by_id'], str(good_reads_book_id))

    stop_memory = getMemory()
    end_time = getTime()
    return book, deltaTime(end_time, start_time), deltaMemory(start_memory, stop_memory)


def get_books_by_author(catalog, author_name):
    start_time = getTime()
    tracemalloc.start()
    start_memory = getMemory()

    books_list = lp.get(catalog['books_by_authors'], author_name)

    stop_memory = getMemory()
    end_time = getTime()
    return author_name, books_list, deltaTime(end_time, start_time), deltaMemory(start_memory, stop_memory)


def get_books_by_tag(catalog, tag_name):
    start_time = getTime()
    tracemalloc.start()
    start_memory = getMemory()

    result_books = al.new_list()
    tag_info = lp.get(catalog['tags'], tag_name)
    
    if tag_info:
        tag_id = tag_info['tag_id']
        book_tags_list = lp.get(catalog['book_tags'], tag_id)
        if book_tags_list:
            for i in range(al.size(book_tags_list)):
                bt = al.get_element(book_tags_list, i)
                b_id = bt['book_id']
                book = lp.get(catalog['books_by_id'], b_id)
                if book:
                    al.add_last(result_books, book)

    stop_memory = getMemory()
    end_time = getTime()
    return result_books, deltaTime(end_time, start_time), deltaMemory(start_memory, stop_memory)


def get_books_by_author_pub_year(catalog, author_name, pub_year):
    start_time = getTime()
    tracemalloc.start()
    start_memory = getMemory()

    pub_year_str = str(pub_year).strip()
    if not pub_year_str:
        pub_year_str = "Desconocido"

    resultado = None
    author_map = lp.get(catalog['books_by_year_author'], author_name)
    if author_map:
        resultado = lp.get(author_map, pub_year_str)

    stop_memory = getMemory()
    end_time = getTime()
    tiempo_transcurrido = deltaTime(end_time, start_time)
    memoria_usada = deltaMemory(start_memory, stop_memory)

    return resultado, tiempo_transcurrido, memoria_usada


# -------------------------------------------------------------
# Funciones de tamaño
# -------------------------------------------------------------

def book_size(catalog):
    return lp.size(catalog['books_by_id'])

def author_size(catalog):
    return lp.size(catalog['books_by_authors'])

def tag_size(catalog):
    return lp.size(catalog['tags'])

def book_tag_size(catalog):
    return lp.size(catalog['book_tags'])


# -------------------------------------------------------------
# Funciones de métricas
# -------------------------------------------------------------

def getTime():
    return float(time.perf_counter() * 1000)

def getMemory():
    return tracemalloc.take_snapshot()

def deltaTime(end, start):
    return float(end - start)

def deltaMemory(start_memory, stop_memory):
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = sum(stat.size_diff for stat in memory_diff) / 1024.0
    return delta_memory
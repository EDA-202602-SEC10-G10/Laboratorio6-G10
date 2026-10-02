"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 """

import sys
import App.logic as logic
from DataStructures.List import array_list as al


def new_logic():
    return logic.new_logic()


def load_data(control):
    books, authors, tags, book_tags, tiempo, memoria = logic.load_data(control)
    return books, authors, tags, book_tags, tiempo, memoria


def print_menu():
    print("\nBienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Consultar la información de un libro según su id")
    print("3- Consultar los libros de un autor")
    print("4- Consultar los libros según un género dado")
    print("5- Consultar los libros de un autor para un año de publicación especifico")
    print("8- Salir")


def print_metrics(tiempo, memoria):
    print(f"Tiempo transcurrido: {tiempo:.2f} ms")
    print(f"Memoria utilizada: {memoria:.2f} kB\n")


def print_book_info(book, tiempo, memoria):
    if book:
        print('Titulo: ' + book['title'] + '  ISBN: ' +
              book['isbn'] + ' Rating: ' + book['average_rating'] +
              ' Work text reviews count : ' + book['work_text_reviews_count'])
    else:
        print('No se encontraron libros')
    print_metrics(tiempo, memoria)


def print_books_by_author(author, books_by_author, tiempo, memoria):
    if books_by_author and al.size(books_by_author) > 0:
        print(f"Para el autor {author} se encontraron los siguientes libros:")
        for book_pos in range(0, al.size(books_by_author)):
            book = al.get_element(books_by_author, book_pos)
            print('Titulo: ' + book['title'] + '  ISBN: ' +
                  book['isbn'] + ' Rating: ' + book['average_rating'] +
                  ' Work text reviews count : ' + book['work_text_reviews_count'])
    else:
        print("No se encontró el autor")
    print_metrics(tiempo, memoria)


def print_books_by_tag(tag_name, books_by_tag, tiempo, memoria):
    if books_by_tag and al.size(books_by_tag) > 0:
        print("Tag encontrado: " + tag_name)
        for book_pos in range(0, al.size(books_by_tag)):
            book = al.get_element(books_by_tag, book_pos)
            print('Titulo: ' + book['title'] + '  ISBN: ' +
                  book['isbn'] + ' Rating: ' + book['average_rating'] +
                  ' Work text reviews count : ' + book['work_text_reviews_count'])
    else:
        print("No se encontró el tag")
    print_metrics(tiempo, memoria)


def print_books_by_auth_year(author, pub_year, books_by_author_year, tiempo_transcurrido, memoria_usada):
    if books_by_author_year and al.size(books_by_author_year) > 0:
        print(f"Para el autor {author}, se encontraron los siguientes libros publicados en el año {pub_year}:")
        for book_pos in range(0, al.size(books_by_author_year)):
            book = al.get_element(books_by_author_year, book_pos)
            print(f"Titulo: {book['title']}  ISBN: {book['isbn']}  Rating: {book['average_rating']}  "
                  f"Work text reviews count: {book['work_text_reviews_count']}")
    else:
        print("No se encontraron libros para ese autor y año de publicación.")
    print_metrics(tiempo_transcurrido, memoria_usada)


exit_opt_lt = ("s", "S", "1", True, "true", "True", "si", "Si", "SI")


def main():
    working = True
    control = new_logic()

    while working:
        print_menu()
        inputs = input("Seleccione una opción para continuar\n")
        
        if not inputs.strip():
            continue

        option = inputs.strip()[0]

        if option == '1':
            print("Cargando información de los archivos ....")
            bk, at, tg, bktg, t_time, t_mem = load_data(control)
            print('Libros cargados: ' + str(bk))
            print('Autores cargados: ' + str(at))
            print('Géneros cargados: ' + str(tg))
            print('Asociación de Géneros a Libros cargados: ' + str(bktg))
            print_metrics(t_time, t_mem)

        elif option == '2':
            number = input("Ingrese el id del libro (good_read_book_id) que desea buscar: ")
            book, t_time, t_mem = logic.get_book_info_by_book_id(control, number)
            print_book_info(book, t_time, t_mem)

        elif option == '3':
            authorname = input("Nombre del autor a buscar: ")
            author, author_book_list, t_time, t_mem = logic.get_books_by_author(control, authorname)
            print_books_by_author(author, author_book_list, t_time, t_mem)

        elif option == '4':
            label = input("Etiqueta a buscar: ")
            book_list_by_tag, t_time, t_mem = logic.get_books_by_tag(control, label)
            print_books_by_tag(label, book_list_by_tag, t_time, t_mem)

        elif option == '5':
            author_name = input("Ingrese el nombre del autor que desea buscar:\n")
            pub_year = input("Ingrese la fecha de publicación que desea buscar:\n")
            books_by_author_pub_year, tiempo_transcurrido, memoria_usada = logic.get_books_by_author_pub_year(control, author_name, pub_year)
            print_books_by_auth_year(author_name, pub_year, books_by_author_pub_year, tiempo_transcurrido, memoria_usada)

        elif option == '8':
            opt_usr = input("¿Desea salir del programa? (s/n): ")
            if opt_usr in exit_opt_lt:
                working = False
                print("\nGracias por utilizar el programa.")

        else:
            continue

    sys.exit(0)


if __name__ == "__main__":
    main()
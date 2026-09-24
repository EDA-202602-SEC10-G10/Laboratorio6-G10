from DataStructures.List import list_node as ln

def default_sort_criteria(element_1, element_2):

   is_sorted = False
   if element_1 < element_2:
      is_sorted = True
   return is_sorted

def new_list():
    newlist = {
        "first": None,
        "last": None,
        "size" : 0,
    }
    
    return newlist

def add_first(my_list, element):
    nodo = ln.new_single_node(element)
    
    if my_list["size"] == 0:
        my_list["first"] = nodo
        my_list["last"] = nodo
    else:
        nodo["next"] = my_list["first"]
        my_list["first"] = nodo
    my_list["size"] += 1
    
    return my_list

def add_last(my_list, element):
    nodo = ln.new_single_node(element)
    
    if my_list["size"] == 0:
        my_list["first"] = nodo
        my_list["last"] = nodo
    else:
        my_list["last"]["next"] = nodo
        my_list["last"] = nodo

    my_list["size"] += 1
    return my_list



def first_element(my_list):
    if my_list["size"] == 0:
        raise Exception('IndexError: list index out of range')
    else:
       return my_list["first"]["info"]
   

def is_empty(my_list):
    if my_list["size"] == 0:
        return True
    else:
        return False
   

def size(my_list):
    return my_list["size"]


def last_element(my_list):
    if my_list["size"] == 0:
        raise Exception('IndexError: list index out of range')
    else:
        return my_list["last"]["info"]


def delete_element(my_list, pos):
    if pos < 0 or pos >= my_list["size"]:
        raise Exception('IndexError: list index out of range')
    else:
        if pos == 0:
            my_list["first"] = my_list ["first"]["next"]
        else:
            anterior = my_list["first"]
            for i in range(pos-1):
                anterior = anterior["next"]
            anterior["next"] = anterior["next"]["next"]
        my_list["size"] = my_list["size"] - 1
    return my_list


def remove_first(my_list):
    if my_list["size"] == 0:
        raise Exception('IndexError: list index out of range')
    else:
        eliminado = my_list["first"]["info"]
        my_list["first"] = my_list["first"]["next"]
        my_list["size"] = my_list["size"] -1
        return eliminado


def remove_last(my_list):
    if my_list["size"] == 0:
        raise Exception('IndexError: list index out of range')
    else:
        eliminado = my_list["last"]["info"]
        anterior = my_list["first"]
        for i in range(my_list["size"] - 2):
            anterior = anterior["next"]
        anterior["next"] = None
        my_list["last"] = anterior
        my_list["size"] = my_list["size"] -1
        return eliminado


def insert_element(my_list, element, pos):
    if pos < 0 or pos > my_list["size"]:
        raise Exception('IndexError: list index out of range')
    else:
        nodo = ln.new_single_node(element)
        if pos == 0:
            nodo["next"] = my_list["first"]
            my_list["first"] = nodo
            if my_list["size"] == 0:
                my_list["last"] = nodo
        else:
            anterior = my_list["first"]
            for i in range(pos - 1):
                anterior = anterior["next"]
            nodo["next"] = anterior["next"]
            anterior["next"] = nodo
            if nodo["next"] is None:
                my_list["last"] = nodo
        my_list["size"] += 1
        return my_list
    
def change_info(my_list, pos, new_info):
    if pos < 0 or pos >= my_list["size"]:
        raise Exception('IndexError: list index out of range')
    else:
        actual = my_list["first"]
        for i in range(pos):
            actual = actual["next"]
        actual["info"] = new_info
        return my_list

def exchange(my_list, pos_1, pos_2):
    if (pos_1 < 0 or pos_1 >= my_list["size"]) or (pos_2 < 0 or pos_2 >= my_list["size"]):
        raise Exception('IndexError: list index out of range')
    else:
        nodo_1 = my_list["first"]
        for i in range(pos_1):
            nodo_1 = nodo_1["next"]

        nodo_2 = my_list["first"]
        for i in range(pos_2):
            nodo_2 = nodo_2["next"]
            
        primera = nodo_1["info"]
        segunda = nodo_2["info"]
        nodo_2["info"] = primera
        nodo_1["info"] = segunda

        return my_list
    
def sub_list(my_list, pos, num_elements):
    if pos + num_elements > my_list["size"]: # Si los elementos uqe quieremos agregar superan el tamaño de la lista error.
        raise IndexError("List out of range")

    mi_sub_lista =  {"first":None,"last":None,"size":0} #esta es nuestra sublista que vamos a retornar
    cuantos_nodos = 0 # contamos cuantos nodos para saber hasta donde llegamos en pos para agregar el ultimo valor de pos 
    llegue_al_ultimo = my_list["first"]
    while cuantos_nodos < pos and llegue_al_ultimo != None:
          llegue_al_ultimo = llegue_al_ultimo["next"]
          cuantos_nodos += 1
    
    agregados = 0
    while agregados < num_elements and llegue_al_ultimo != None:
          copia_nodo = {"info": llegue_al_ultimo["info"], "next": None}
          if mi_sub_lista["first"] == None:
              mi_sub_lista["first"] = copia_nodo
              mi_sub_lista["last"] = copia_nodo
          else:
              mi_sub_lista["last"]["next"] = copia_nodo
              mi_sub_lista["last"] = copia_nodo

          mi_sub_lista["size"] += 1
          llegue_al_ultimo = llegue_al_ultimo["next"]
          agregados += 1

    return mi_sub_lista    




def get_element(my_list, pos):
    searchpos = 0
    node = my_list["first"]
    while searchpos < pos:
        node = node["next"]
        searchpos += 1
    return node["info"]

def is_present(my_list, element, cmp_function):
    is_in_array = False
    temp = my_list["first"]
    count = 0
    while not is_in_array and temp is not None:
        if cmp_function(element, temp["info"]) == 0:
            is_in_array = True
        else:
            temp = temp["next"]
            count += 1

    if not is_in_array:
        count = -1
    return count

def selection_sort(my_list, sort_criterio):
    n = my_list["size"]
    i = 0
    while i < n:
        min_idx = i
        j = i + 1
        while j < n:
            if sort_criterio(get_element(my_list, j), get_element(my_list, min_idx)):
                min_idx = j
            j += 1
            
        if min_idx != i:
            exchange(my_list, i, min_idx)
        i += 1
        
    return my_list

def insertion_sort(my_list, sort_crit):
    n = size(my_list)
    i = 1
    while i < n:
        j = i
        while j > 0 and sort_crit(get_element(my_list, j), get_element(my_list, j-1)):
            exchange(my_list, j, j-1)
            j -= 1
        i += 1
        
    return my_list

def shell_sort(my_list, cmp_function):
    n = my_list["size"]
    gap = n // 2
    while gap > 0:
        i = gap
        while i < n:
            temp = get_element(my_list, i)
            j = i
            while j >= gap and cmp_function(get_element(my_list, j - gap), temp) > 0:
                change_info(my_list, j, get_element(my_list, j - gap))
                j -= gap
            change_info(my_list, j, temp)
            i += 1
        gap //= 2
        
    return my_list

def merge(izquierda, derecha, sort_crit):
    """Combina dos sublistas ordenadas en una sola lista ordenada."""
    combinada = new_list()
    i = 0
    j = 0
    while i < size(izquierda) and j < size(derecha):
        elem_izq = get_element(izquierda, i)
        elem_der = get_element(derecha, j)
        if sort_crit(elem_izq, elem_der):
            add_last(combinada, elem_izq)
            i += 1
        else:
            add_last(combinada, elem_der)
            j += 1
    while i < size(izquierda):
        add_last(combinada, get_element(izquierda, i))
        i += 1
    while j < size(derecha):
        add_last(combinada, get_element(derecha, j))
        j += 1
    return combinada


def merge_sort(my_list, sort_crit):
    """Ordena la lista encadenada usando el algoritmo merge sort (mezcla)."""
    n = size(my_list)
    if n <= 1:
        return my_list

    mid = n // 2
    izquierda = sub_list(my_list, 0, mid)
    derecha = sub_list(my_list, mid, n - mid)

    izquierda = merge_sort(izquierda, sort_crit)
    derecha = merge_sort(derecha, sort_crit)

    combinada = merge(izquierda, derecha, sort_crit)

    my_list["first"] = combinada["first"]
    my_list["last"] = combinada["last"]
    my_list["size"] = combinada["size"]

    return my_list

def quick_sort(my_list, sort_crit):
    """
    Ordena una Single Linked List usando Quick Sort
    sin utilizar recursión.
    """

    # Lista donde iremos construyendo el resultado final
    resultado = new_list()

    # Stack explícito.
    # Cada elemento será:
    # ("sort", lista)  -> hay que ordenar la lista
    # ("append", lista) -> agregar lista al resultado
    stack = [("sort", my_list)]

    while len(stack) > 0:

        accion, lista = stack.pop()

        # -------------------------------------------------
        # ORDENAR UNA LISTA
        # -------------------------------------------------
        if accion == "sort":

            # Si tiene 0 o 1 elementos, ya está ordenada
            if lista["size"] <= 1:
                stack.append(("append", lista))
                continue

            # Elegimos el pivote del medio
            pivote = get_element(
                lista,
                lista["size"] // 2
            )

            # Tres partes
            menores = new_list()
            iguales = new_list()
            mayores = new_list()

            # Recorremos la lista
            actual = lista["first"]

            while actual is not None:

                info = actual["info"]

                antes_pivote = sort_crit(info, pivote)
                pivote_antes = sort_crit(pivote, info)

                # Caso de igualdad
                #
                # Funciona tanto si sort_crit usa < como si usa <=
                if antes_pivote and pivote_antes:
                    add_last(iguales, info)

                elif antes_pivote:
                    add_last(menores, info)

                elif pivote_antes:
                    add_last(mayores, info)

                else:
                    add_last(iguales, info)

                actual = actual["next"]

            # -------------------------------------------------
            # IMPORTANTE:
            #
            # Stack es LIFO.
            #
            # Queremos procesar:
            #
            # menores -> iguales -> mayores
            #
            # Por eso los metemos al stack al revés.
            # -------------------------------------------------

            if mayores["size"] > 0:
                stack.append(("sort", mayores))

            if iguales["size"] > 0:
                stack.append(("append", iguales))

            if menores["size"] > 0:
                stack.append(("sort", menores))

        # -------------------------------------------------
        # AGREGAR UNA PARTE AL RESULTADO
        # -------------------------------------------------
        elif accion == "append":

            if lista["size"] == 0:
                continue

            if resultado["size"] == 0:
                resultado["first"] = lista["first"]
                resultado["last"] = lista["last"]

            else:
                resultado["last"]["next"] = lista["first"]
                resultado["last"] = lista["last"]

            resultado["size"] += lista["size"]

    # Copiamos el resultado a my_list
    my_list["first"] = resultado["first"]
    my_list["last"] = resultado["last"]
    my_list["size"] = resultado["size"]

    return my_list
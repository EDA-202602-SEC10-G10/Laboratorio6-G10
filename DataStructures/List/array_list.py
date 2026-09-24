def default_sort_criteria(element_1, element_2):

   is_sorted = False
   if element_1 < element_2:
      is_sorted = True
   return is_sorted

def new_list():
    newlist = {
        "elements": [],
        "size" : 0,
    }
    return newlist


def add_first(new_list, element):
    """Agrega un elemento al inicio de la lista."""
    new_list["elements"].insert(0, element)
    new_list["size"] += 1
    return new_list


def add_last(new_list, element):
    """Agrega un elemento al final de la lista."""
    new_list["elements"].append(element)
    new_list["size"] += 1
    return new_list

def size(newlist):
    return newlist["size"]


def is_empty(new_list):
    return new_list["size"] == 0


def first_element(new_list):
    if is_empty(new_list):
        raise IndexError("list index out of range")
    return new_list["elements"][0]

def last_element(new_list):
    if is_empty(new_list):
        raise IndexError("list index out of range")
    return new_list["elements"][-1]


def change_info(new_list, pos, new_element):
    if pos < 0 or pos >= new_list["size"]:
        raise IndexError("list index out of range")
    new_list["elements"][pos] = new_element
    return new_list

def get_element(new_list,pos):
    if pos >= new_list["size"] or pos < 0:
        raise IndexError("list index out of range")
    variable = new_list["elements"][pos]
    return variable

def remove_last(new_list):
    if is_empty(new_list):
        raise IndexError("list index out of range")
    remove = new_list["size"] -1 
    new_list["elements"].pop(-1)
    return remove

def remove_first(my_list):
    if is_empty(my_list):
        raise IndexError("list index out of range")
    
    element = my_list["elements"].pop(0)
    my_list["size"] -= 1  # <-- ESTA LÍNEA ES VITAL
    return element

def insert_element(new_list,element,pos):
    if pos < 0 or pos > new_list["size"]:
        raise IndexError("list index out of range")
    new_list["elements"].insert(pos,element)
    new_list["size"] += 1
    return new_list

def is_present(new_list,element,cmp_function):
    """
    Invocamos cmp_function para que realice la comparación con el elemnt y si se encuentra igual da 0 mayor da 1 menor -1.
    """
    pos = -1
    centi = False
    i = 0
    while i < new_list["size"] and centi == False:  
        if cmp_function(new_list["elements"][i],element) == 0:
            centi = True
            pos = i
        i += 1
    return pos   

def delete_element(new_list,pos):
    if 0 > pos or pos > new_list["size"] :
        raise IndexError("list index out of range")
    new_list["elements"].pop(pos) #mismo espacio de memoria
    new_list["size"] -= 1
    return new_list

def exchange(my_list,pos_1,pos_2):
    if (pos_1 < 0 ) or (pos_2 < 0) or (pos_1 >= my_list["size"]) or (pos_2 >= my_list["size"]):
        raise IndexError("list out index of range")
    temp = my_list["elements"][pos_1]
    my_list["elements"][pos_1] = my_list["elements"][pos_2]
    my_list["elements"][pos_2] = temp
    return my_list

def sub_list(my_list,pos_i,num_elements):
    if (pos_i < 0 ) or (pos_i >= my_list["size"]) or (pos_i + num_elements > my_list["size"]): 
        raise IndexError("list index out of range")
    nueva_lista = new_list()
    for i in range(pos_i, pos_i + num_elements):
        add_last(nueva_lista,my_list["elements"][i])

    return nueva_lista

def selection_sort(my_list, sort_criterio):
    n = my_list["size"]
    for i in range(0,n):
        min_idx = i
        for j in range(i + 1, n):
            if sort_criterio(get_element(my_list, j), get_element(my_list, min_idx)) :
                min_idx = j
        if min_idx != i:
            exchange(my_list, i, min_idx)
    return my_list

def insertion_sort(my_list, sort_crit):
    for i in range(1, size(my_list)):
        j = i
        while j > 0 and sort_crit(get_element(my_list, j), get_element(my_list, j-1)):
            exchange(my_list, j, j-1)
            j -= 1
    return my_list

def shell_sort(my_list,cmp_function):
    n = my_list["size"]
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = my_list["elements"][i]
            j = i
            while j >= gap and cmp_function(my_list["elements"][j - gap], temp) > 0:
                my_list["elements"][j] = my_list["elements"][j - gap]
                j -= gap
            my_list["elements"][j] = temp
        gap //= 2
    return my_list

def merge(my_list, left, right, sort_crit):
   
    merged = new_list()
    i = 0
    j = 0
    while i < size(left) and j < size(right):
        elem_left = get_element(left, i)
        elem_right = get_element(right, j)
        if sort_crit(elem_left, elem_right):
            add_last(merged, elem_left)
            i += 1
        else:
            add_last(merged, elem_right)
            j += 1
    while i < size(left):
        add_last(merged, get_element(left, i))
        i += 1
    while j < size(right):
        add_last(merged, get_element(right, j))
        j += 1
    return merged


def merge_sort(my_list, sort_crit):
    
    n = size(my_list)
    if n <= 1:
        return my_list

    mid = n // 2
    left = sub_list(my_list, 0, mid)
    right = sub_list(my_list, mid, n - mid)

    left = merge_sort(left, sort_crit)
    right = merge_sort(right, sort_crit)

    merged = merge(my_list, left, right, sort_crit)

    my_list["elements"] = merged["elements"]
    my_list["size"] = merged["size"]

    return my_list

def partition(my_list, lo, hi, sort_crit):
    """Particiona my_list[lo..hi] usando como pivote el elemento del medio.
    Retorna la posición final del pivote."""
    mid = (lo + hi) // 2
    exchange(my_list, mid, hi)          # el pivote queda al final
    pivot = get_element(my_list, hi)
 
    i = lo - 1                          # frontera de los elementos "menores"
    for j in range(lo, hi):
        if sort_crit(get_element(my_list, j), pivot):
            i += 1
            exchange(my_list, i, j)
 
    exchange(my_list, i + 1, hi)        # pivote a su posición definitiva
    return i + 1
 
 
def quick_sort_rec(my_list, lo, hi, sort_crit):
    if lo < hi:
        p = partition(my_list, lo, hi, sort_crit)
        quick_sort_rec(my_list, lo, p - 1, sort_crit)
        quick_sort_rec(my_list, p + 1, hi, sort_crit)
 
 
def quick_sort(my_list, sort_crit):
    """Ordena la lista (array_list) con el algoritmo Quick Sort."""
    quick_sort_rec(my_list, 0, my_list["size"] - 1, sort_crit)
    return my_list
 
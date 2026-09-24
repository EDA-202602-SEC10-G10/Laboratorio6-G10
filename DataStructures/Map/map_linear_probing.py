import random
from DataStructures.Map import map_entry as me
from DataStructures.Map import map_functions as mf


def new_map(num_elements, load_factor=0.5, prime=109345121):
    """
    Crea una nueva tabla de símbolos (map) sin elementos utilizando linear probing.
    """
    prime_val = prime
    capacity = mf.next_prime(int(num_elements / load_factor))
    if capacity < 5:
        capacity = 5

    scale = random.randint(1, prime_val - 1)
    shift = random.randint(0, prime_val - 1)

    # Inicializamos la tabla con entradas vacías (None)
    table = [None] * capacity

    my_map = {
        "prime": prime_val,
        "capacity": capacity,
        "scale": scale,
        "shift": shift,
        "table": table,
        "current_factor": 0.0,
        "limit_factor": load_factor,
        "size": 0,
    }
    return my_map


def default_compare(key1, key2):
    """
    Función de comparación por defecto entre dos llaves.
    """
    if key1 == key2:
        path = 0
    elif key1 > key2:
        path = 1
    else:
        path = -1
    return path


def is_available(table, index):
    """
    Verifica si una posición en la tabla está disponible (vacía o marcada como disponible/eliminada).
    """
    entry = table[index]
    return entry is None or me.get_key(entry) is None


def find_slot(my_map, key):
    """
    Busca la ranura (slot) correspondiente a una llave utilizando linear probing.
    Retorna una tupla (encontrado: bool, index: int).
    """
    table = my_map["table"]
    capacity = my_map["capacity"]
    start_index = mf.hash_value(my_map, key)
    index = start_index

    first_available = -1

    while True:
        entry = table[index]
        if entry is None:
            if first_available == -1:
                first_available = index
            return False, first_available
        elif me.get_key(entry) is None:
            if first_available == -1:
                first_available = index
        elif default_compare(me.get_key(entry), key) == 0:
            return True, index

        index = (index + 1) % capacity
        if index == start_index:
            break

    if first_available != -1:
        return False, first_available

    return False, -1


def rehash(my_map):
    """
    Realiza un rehash de la tabla duplicando su capacidad y reubicando los elementos.
    """
    old_table = my_map["table"]
    old_capacity = my_map["capacity"]

    new_capacity = mf.next_prime(old_capacity * 2)
    prime_val = my_map["prime"]

    my_map["capacity"] = new_capacity
    my_map["scale"] = random.randint(1, prime_val - 1)
    my_map["shift"] = random.randint(0, prime_val - 1)
    my_map["table"] = [None] * new_capacity
    my_map["size"] = 0
    my_map["current_factor"] = 0.0

    for entry in old_table:
        if entry is not None and me.get_key(entry) is not None:
            put(my_map, me.get_key(entry), me.get_value(entry))


def put(my_map, key, value):
    """
    Inserta o actualiza una pareja llave-valor en la tabla.
    """
    found, index = find_slot(my_map, key)
    table = my_map["table"]

    if found:
        # Actualiza el valor si la llave ya existe
        me.set_value(table[index], value)
    else:
        # Inserta nueva entrada
        entry = me.new_map_entry(key, value)
        table[index] = entry
        my_map["size"] += 1
        my_map["current_factor"] = my_map["size"] / my_map["capacity"]

        # Verificar si se debe hacer rehash
        if my_map["current_factor"] >= my_map["limit_factor"]:
            rehash(my_map)


def contains(my_map, key):
    """
    Verifica si una llave existe en el mapa.
    """
    found, _ = find_slot(my_map, key)
    return found


def get(my_map, key):
    """
    Obtiene el valor asociado a una llave dada. Retorna None si no existe.
    """
    found, index = find_slot(my_map, key)
    if found:
        return me.get_value(my_map["table"][index])
    return None


def remove(my_map, key):
    """
    Elimina una entrada de la tabla usando lazy deletion (marcando la llave como None).
    """
    found, index = find_slot(my_map, key)
    if found:
        entry = my_map["table"][index]
        me.set_key(entry, None)
        me.set_value(entry, None)
        my_map["size"] -= 1
        my_map["current_factor"] = my_map["size"] / my_map["capacity"]
        return entry
    return None


def size(my_map):
    """
    Retorna el número de elementos almacenados en el mapa.
    """
    my_map["size"]
    return my_map["size"]


def is_empty(my_map):
    """
    Retorna True si el mapa está vacío, False de lo contrario.
    """
    return my_map["size"] == 0


def key_set(my_map):
    """
    Retorna una lista con todas las llaves del mapa.
    """
    # Nota: Se puede retornar como una lista de Python o usando ArrayList según prefieras
    keys = []
    for entry in my_map["table"]:
        if entry is not None and me.get_key(entry) is not None:
            keys.append(me.get_key(entry))
    return keys


def value_set(my_map):
    """
    Retorna una lista con todos los valores del mapa.
    """
    values = []
    for entry in my_map["table"]:
        if entry is not None and me.get_key(entry) is not None:
            values.append(me.get_value(entry))
    return values
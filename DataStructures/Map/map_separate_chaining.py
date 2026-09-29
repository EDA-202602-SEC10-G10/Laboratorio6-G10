import random
from DataStructures.Map import map_entry as me
from DataStructures.Map import map_functions as mf
from DataStructures.List import list_node as ln
from DataStructures.List import single_linked_list as sll
from DataStructures.List import array_list as al

def new_map(num,load_factor,prime):
    capacity = mf.next_prime(int(num/load_factor))
    scale = rd.randint(1,prime-1)
    shift = rd.randint(0,prime-1)
    my_map = {"prime":prime,"scale":scale,"shift":shift,"capacity":capacity,"table":al.new_list(),"current_factor":0,"limit_factor":0,"size":0}
    for i in range(0,capacity):
        lista = sll.new_list()
        al.add_last(my_map["table"]["elements"],lista)
    return  my_map

def default_compare(key,entry):
    if key == me.get_key(entry):
        return 0 
    if key > me.get_key(entry):
        return 1
    return -1

def contains(my_map,key):
    hash_value = mf.hash_value(my_map,key)
    grupo = my_map["table"]["elements"][hash_value]
    t = grupo["size"]
    i = 0
    actual = grupo["first"]
    existe = False
    while i < t:
        if actual["info"]["key"] == key:
            existe = True
            break
        i += 1
        actual = actual["next"]
    return existe

def remove(my_map, key):
    hash_value = mf.hash_value(my_map, key)
    ubicacion = my_map["table"]["elements"][hash_value]
    
    # ERRATA 1: t1 debe medir la sublista 'ubicacion', no el arreglo de la tabla
    t1 = sll.size(ubicacion) 
    
    # ERRATA 2: Verificar que no esté vacía la lista antes de pedir actual["next"]
    if ubicacion["first"] is None:
        return my_map
        
    i = 0
    actual = ubicacion["first"]
    siguiente = actual["next"]
    
    if contains(my_map, key):
        # ERRATA 3: 't' era una variable no definida; usamos t1
        if t1 <= 2 and t1 != 0:
            if t1 <= 1:
                # ERRATA 4: Limpiar la lista en memoria en lugar de crear un diccionario nuevo
                ubicacion["first"] = None
                ubicacion["last"] = None
                ubicacion["size"] = 0
                return my_map
            else:
                if actual["info"]["key"] == key:
                    # ERRATA 5: Asignar el nodo 'siguiente', no 'siguiente["info"]'
                    ubicacion["first"] = siguiente
                    ubicacion["last"] = siguiente
                    ubicacion["size"] = 1
                    return my_map
                else:
                    # ERRATA 6: Corregir sintaxis size=1 -> "size": 1 y asignar el nodo 'actual'
                    actual["next"] = None
                    ubicacion["first"] = actual
                    ubicacion["last"] = actual
                    ubicacion["size"] = 1
                    return my_map
        
        if actual["info"]["key"] != key:
            while i < t1 - 2:
                if siguiente["info"]["key"] == key:
                    actual["next"] = siguiente["next"]
                    return my_map
                i += 1
                actual = actual["next"]
                # ERRATA 7: Avanzar también el puntero 'siguiente' en cada paso del loop
                siguiente = actual["next"]
                
            # ERRATA 8: Sangría fuera del while para no cortar la primera iteración
            actual["next"] = None
            return my_map
        else:
            ubicacion["first"] = siguiente
            return my_map
    
    return my_map
           
          
def put(my_map, key, value):
    hash_value = mf.hash_value(my_map, key)
    grupo = my_map["table"]["elements"][hash_value]
    
    # 1. Si la llave ya existe, actualizamos su valor
    actual = grupo["first"]
    while actual is not None:
        if actual["info"]["key"] == key:
            actual["info"]["value"] = value
            return my_map
        actual = actual["next"]
        
    # 2. Si no existe, creamos el map_entry y lo insertamos al inicio de la sublista
    entry = me.new_map_entry(key, value)
    sll.add_first(grupo, entry)  # O insertas creando el nodo directamente
    
    # 3. Actualizamos contadores
    my_map["size"] += 1
    my_map["current_factor"] = my_map["size"] / my_map["capacity"]
    
    # 4. Verificamos si se debe hacer rehash
    if my_map["current_factor"] > my_map["limit_factor"]:
        rehash(my_map)
        
    return my_map    


def rehash(my_map):
    viejos_elementos = my_map["table"]["elements"]
    nueva_capacidad = my_map["capacity"] * 2
    
    # Reconfiguramos el mapa con la nueva tabla vacía
    my_map["capacity"] = nueva_capacidad
    my_map["table"] = al.new_list(nueva_capacidad)
    for _ in range(nueva_capacidad):
        al.add_last(my_map["table"], sll.new_list())
        
    my_map["size"] = 0
    
    # Reinsertamos los elementos que teníamos guardados
    for i in range(len(viejos_elementos)):
        sublista = viejos_elementos[i]
        actual = sublista["first"]
        while actual is not None:
            put(my_map, actual["info"]["key"], actual["info"]["value"])
            actual = actual["next"]
            
    return my_map

def size(my_map):
    return my_map["size"]

def is_empty(my_map):
    return my_map["size"] == 0

def key_set(my_map):
    keys = sll.new_list()
    elementos = my_map["table"]["elements"]
    for i in range(my_map["capacity"]):
        actual = elementos[i]["first"]
        while actual is not None:
            sll.add_last(keys, actual["info"]["key"])
            actual = actual["next"]
    return keys

def value_set(my_map):
    values = sll.new_list()
    elementos = my_map["table"]["elements"]
    for i in range(my_map["capacity"]):
        actual = elementos[i]["first"]
        while actual is not None:
            sll.add_last(values, actual["info"]["value"])
            actual = actual["next"]
    return values
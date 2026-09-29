import random
from DataStructures.Map import map_entry as me
from DataStructures.Map import map_functions as mf
from DataStructures.List import array_list as al

def new_map(num_elementos,load_factor=0.5,prime=109345121):
    capacity = mf.next_prime(int(num_elementos / load_factor))
    scale = random.randint(1,prime-1)
    shift = random.randint(0,prime-1)
    elementos = al.new_list()
    for i in range(0,capacity):
        al.add_last(elementos,me.new_map_entry(None,None))
    
    mapa = {"capacity":capacity,
            "prime" : prime,
            "scale": scale,
            "shift" : shift,
            "table": elementos,
            "current_factor": 0,
            "size" : 0,
            "limit_factor" : load_factor}
    
    return mapa



def is_available(table,pos):
    if me.get_key(table[pos]) == None:
        return True
    return False

    
def default_compare(key1, entry):
    """
    Función de comparación por defecto entre dos llaves.
    """
    if key1 == me.get_key(entry):
        path = 0
    elif key1 > me.get_key(entry):
        path = 1
    else:
        path = -1
    return path

def find_slot(my_map,key,hash_value):
    encontrado = False
    pos = None
    
    while encontrado == False:
        if me.get_key(my_map["table"]["elements"][hash_value]) == None:
            pos = hash_value
            break 
        else:
            if me.get_key(my_map["table"][hash_value]) == key:
               pos = hash_value
               encontrado = True
        hash_value = (hash_value + 1) % my_map["capacity"]
        
    return (encontrado,pos)

def contains(my_map,key):
    hash_value = mf.hash_value(my_map,key)
    verdad,pos = find_slot(my_map,key,hash_value)
    return verdad               
    

def get(my_map,key):
    hash_value = mf.hash_value(my_map,key)
    valor,pos = find_slot(my_map,key,hash_value)
    if valor:
       return me.get_value(my_map["table"]["elements"][pos])
    return None 

def remove(my_map,key):
    """Funciona ya que, find_slot me busca es por break, contador modular 
    entonces va a existir no importa cuantos asubk sumados base a N sean
    """
    hash_values = mf.hash_value(my_map,key)
    valor,pos = find_slot(my_map,key,hash_values)
    if valor:
        me.set_key(my_map["table"]["elements"][pos],None)
        me.set_value(my_map["table"]["elements"][pos],None)
        my_map["size"] -= 1
        my_map["current_factor"] = my_map["size"] / my_map["capacity"]
        return my_map
    return None

def put(my_map, key, value):
    hash_value = mf.hash_value(my_map,key)
    valor,pos = find_slot(my_map,key,hash_value)
    if valor:
       me.set_value(my_map["table"]["elements"][pos],value)
    else:
       me.set_value(my_map["table"]["elements"][pos],value)
       me.set_key(my_map["table"]["elements"][pos],key)
       my_map["size"] += 1
       my_map["current_factor"] = my_map["size"] / my_map["capacity"]
       if my_map["current_factor"]  > my_map["limit_factor"]:
           rehash(my_map)
           return my_map
    return my_map
    

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
    for i in range(0,my_map["table"]["size"]):
        if me.get_key(my_map["table"]["elements"][i]) != None:
            keys.append(me.get_key(my_map["table"]["elements"][i]))
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


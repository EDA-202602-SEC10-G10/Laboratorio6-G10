import random as rd
import DataStructures.Map.map_functions as mf
import DataStructures.Map.map_entry as me
import DataStructures.List.single_linked_list as sl
import DataStructures.List.array_list as al

def new_map(num, load_factor, prime):
    capacity = mf.next_prime(int(num / load_factor))
    scale = rd.randint(1, prime - 1)
    shift = rd.randint(0, prime - 1)
    
    table = al.new_list()
    for _ in range(capacity):
        al.add_last(table, sl.new_list())
        
    my_map = {
        "capacity": capacity,
        "current_factor": 0.0,
        "limit_factor": load_factor,
        "prime": prime,
        "scale": scale,
        "shift": shift,
        "size": 0,
        "table": table
    }
    return my_map

def put(my_map, key, value):
    hash_val = mf.hash_value(my_map, key)
    chain = al.get_element(my_map["table"], hash_val)
    
    # Buscar si la llave ya existe para actualizarla
    current_node = chain["first"]
    while current_node is not None:
        entry = current_node["info"]
        if me.get_key(entry) == key:
            me.set_value(entry, value)
            return my_map
        current_node = current_node["next"]
        
    # Si no existe, insertar nueva entrada al inicio de la lista encadenada
    new_entry = me.new_map_entry(key, value)
    sl.add_first(chain, new_entry)
    my_map["size"] += 1
    my_map["current_factor"] = my_map["size"] / my_map["capacity"]
    
    if my_map["current_factor"] > my_map["limit_factor"]:
        rehash(my_map)
        
    return my_map

def contains(my_map, key):
    return get(my_map, key) is not None

def get(my_map, key):
    hash_val = mf.hash_value(my_map, key)
    chain = al.get_element(my_map["table"], hash_val)
    
    current_node = chain["first"]
    while current_node is not None:
        entry = current_node["info"]
        if me.get_key(entry) == key:
            return me.get_value(entry)
        current_node = current_node["next"]
    return None

# def remove(my_map, key):
    hash_value = mf.hash_value(my_map,key)
    tamaño = my_map["table"]["elements"][hash_value]["size"]
    i = 0
    actual = my_map["table"]["elements"][hash_value]["first"] 
    if tamaño == 1:
       my_map["table"]["elements"][hash_value] = sl.new_list()
       return my_map
    
    while i < tamaño-1:
        if actual["info"]["key"] == key:
           sl.delete_element(my_map["table"]["elements"][hash_value],i)
           break
        i += 1
        actual = actual["next"]
        
    return my_map

def remove(my_map, key):
    hash_val = mf.hash_value(my_map, key)
    chain = al.get_element(my_map["table"], hash_val)
    
    current_node = chain["first"]
    index = 0
    
    while current_node is not None:
        entry = current_node["info"]
        
        if me.get_key(entry) == key:
            # Eliminar elemento de la lista enlazada
            removed = sl.delete_element(chain, index)
            
            # Desempaquetar en caso de que 'delete_element' devuelva un nodo o envoltorio
            if isinstance(removed, dict):
                if "info" in removed:
                    removed_entry = removed["info"]
                else:
                    removed_entry = removed
            else:
                removed_entry = removed
            
            # Si el result aún no tiene la llave 'value', extraer la entry del nodo buscado directamente
            if isinstance(removed_entry, dict) and "value" not in removed_entry:
                val = me.get_value(entry)
            else:
                val = me.get_value(removed_entry)
            
            # Actualizar tamaño y factor de carga del mapa
            my_map["size"] -= 1
            my_map["current_factor"] = my_map["size"] / my_map["capacity"]
            
            return val
            
        current_node = current_node["next"]
        index += 1
        
    return None
         

def size(my_map):
    return my_map["size"]

def is_empty(my_map):
    return my_map["size"] == 0

def key_set(my_map):
    keys = al.new_list()
    for i in range(al.size(my_map["table"])):
        chain = al.get_element(my_map["table"], i)
        current_node = chain["first"]
        while current_node is not None:
            entry = current_node["info"]
            al.add_last(keys, me.get_key(entry))
            current_node = current_node["next"]
    return keys

def value_set(my_map):
    values = al.new_list()
    for i in range(al.size(my_map["table"])):
        chain = al.get_element(my_map["table"], i)
        current_node = chain["first"]
        while current_node is not None:
            entry = current_node["info"]
            al.add_last(values, me.get_value(entry))
            current_node = current_node["next"]
    return values

def rehash(my_map):
    old_table = my_map["table"]
    old_capacity = my_map["capacity"]
    
    new_capacity = mf.next_prime(old_capacity * 2)
    new_table = al.new_list()
    for _ in range(new_capacity):
        al.add_last(new_table, sl.new_list())
        
    my_map["capacity"] = new_capacity
    my_map["table"] = new_table
    my_map["size"] = 0
    my_map["current_factor"] = 0.0
    
    for i in range(al.size(old_table)):
        chain = al.get_element(old_table, i)
        current_node = chain["first"]
        while current_node is not None:
            entry = current_node["info"]
            put(my_map, me.get_key(entry), me.get_value(entry))
            current_node = current_node["next"]
            
    return my_map
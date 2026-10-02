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


def is_available(table, pos):
    if table["elements"][pos]["key"] == None or table["elements"][pos]["key"] == "__EMPTY__":
        return True
    return False

def find_slot(my_map, key, hash_value):
    table = my_map["table"]
    capacity = my_map["capacity"]
    pos = hash_value
    first_avail = None
    
    for _ in range(capacity):
        entry = al.get_element(table, pos)
        entry_key = me.get_key(entry)
        
        if entry_key is None:
            if first_avail is None:
                first_avail = pos
            return False, first_avail
        elif entry_key == key:
            return True, pos
        elif entry_key == "__EMPTY__" and first_avail is None:
            first_avail = pos
            
        pos = (pos + 1) % capacity
        
    return False, first_avail

def put(my_map, key, value):
    hash_val = mf.hash_value(my_map, key)
    found, pos = find_slot(my_map, key, hash_val)
    table = my_map["table"]
    
    if found:
        entry = al.get_element(table, pos)
        me.set_value(entry, value)
    else:
        new_entry = me.new_map_entry(key, value)
        al.change_info(table, pos, new_entry)
        my_map["size"] += 1
        my_map["current_factor"] = my_map["size"] / my_map["capacity"]
        
        if my_map["current_factor"] > my_map["limit_factor"]:
            rehash(my_map)
            
    return my_map

def contains(my_map, key):
    hash_val = mf.hash_value(my_map, key)
    found, _ = find_slot(my_map, key, hash_val)
    return found

def get(my_map, key):
    hash_val = mf.hash_value(my_map, key)
    found, pos = find_slot(my_map, key, hash_val)
    if found:
        entry = al.get_element(my_map["table"], pos)
        return me.get_value(entry)
    return None

def remove(my_map, key):
    hash_val = mf.hash_value(my_map, key)
    found, pos = find_slot(my_map, key, hash_val)
    if found:
        table = my_map["table"]
        entry = al.get_element(table, pos)
        val = me.get_value(entry)
        
        # Marcar la casilla como removida con el centinela '__EMPTY__'
        tombstone = me.new_map_entry("__EMPTY__", None)
        al.change_info(table, pos, tombstone)
        
        my_map["size"] -= 1
        my_map["current_factor"] = my_map["size"] / my_map["capacity"]
        return val
    return None

def size(my_map):
    return my_map["size"]

def is_empty(my_map):
    return my_map["size"] == 0

def key_set(my_map):
    keys = al.new_list()
    table = my_map["table"]
    for i in range(al.size(table)):
        entry = al.get_element(table, i)
        k = me.get_key(entry)
        if k is not None and k != "__EMPTY__":
            al.add_last(keys, k)
    return keys

def value_set(my_map):
    values = al.new_list()
    table = my_map["table"]
    for i in range(al.size(table)):
        entry = al.get_element(table, i)
        k = me.get_key(entry)
        if k is not None and k != "__EMPTY__":
            al.add_last(values, me.get_value(entry))
    return values

def rehash(my_map):
    old_table = my_map["table"]
    old_capacity = my_map["capacity"]
    
    new_capacity = mf.next_prime(old_capacity * 2)
    new_table = al.new_list()
    for _ in range(new_capacity):
        al.add_last(new_table, me.new_map_entry(None, None))
        
    my_map["capacity"] = new_capacity
    my_map["table"] = new_table
    my_map["size"] = 0
    my_map["current_factor"] = 0.0
    
    for i in range(al.size(old_table)):
        entry = al.get_element(old_table, i)
        k = me.get_key(entry)
        if k is not None and k != "__EMPTY__":
            put(my_map, k, me.get_value(entry))
            
    return my_map
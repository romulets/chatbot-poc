class Footprint():

    def __init__(self, name, ttl, entities= {}):
        self.__name = name
        self.__ttl = ttl
        self.__entities = entities

    def decrease_life(self):
        return Footprint(self.__name, self.__ttl - 1, self.__entities)

    def is_alive(self):
        return self.__ttl > 0

    def name(self):
        return self.__name

    def __str__(self):
        return self.__name


def run_footprint_cicle(legacy_footprints, new_footprints): 
    result_footprints = {}

    for footprint in legacy_footprints:
        result_footprints[footprint.name()] = footprint.decrease_life()
    
    for footprint in new_footprints:
        result_footprints[footprint.name()] = footprint

    return list(filter(lambda f: f.is_alive(), result_footprints.values()))
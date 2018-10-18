import table

class State:
    tbl = None #таблица расстояний (приведенных к нулю)
    n = None #количество пуктов назначения
    cost = None #оценка минимально возможного маршрута это его расстояние определяется как Sum(min_from + min_to)
    min_from = [] #соответсвует строке i и содержит минимальное рассотояние из пункта i
    min_to = [] #соответсвует столбцу j и содержит минимальное добавочное рассотояние до пункта j 

    def __init__(self, tbl):
        self.tbl = tbl;
        n = len(tbl)
        
        for i in range(n):
            self.min_from.append(0)
            self.min_to.append(0)

        

    def define_cost(self):
        

def unittest():
    tbl = simple_generator_distance_table(5, 9))

    

    print_distance(tbl)

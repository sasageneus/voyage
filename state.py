import lib

from route import Jump

# пункт отправления
class PointFrom:
    name = None # наименование,
    row = None # строка таблицы расстояний
    min_dist = 0 # расстояние до ближайшего пункта
    penalty = None # размер штрафа если не воспользоваться ближайшим пунктом назначения

    def init(self, name, row):
        self.name = name
        self.row = row
        return self

    def minimaze(self):
        m, self.penalty = lib.minimaze(self.row)
        self.min_dist += m

    def find_penalty(self):
        m, self.penalty = lib.min_and_penalty(self.row)

    def clone(self, delete):
        new = PointFrom()
        new.init(self.name, self.row[0:delete] + self.row[delete+1:])
        new.minimaze()
        new.min_dist += self.min_dist
        return new

    def print_row(self):
        for dist in self.row:
            print('%s' % (str(dist) if dist != None else '-'), end = '\t')
        print('')

# пункт прибытия
class PointTo:
    min_dist = 0 # расстояние до ближайшего пункта
    penalty = None # размер штрафа если не воспользоваться ближайшим пунктом назначения
    def __init__(self, points_from, j, name):
        self.points_from = points_from #ссылается на одноименное поле в State, используется для доступа к таблице расстояний
        self.j = j # индекс колонки в таблице расстояний
        self.name = name

    def clone(self, points_from, j):
        new = PointTo(points_from, j, self.name)
        new.min_dist = self.min_dist
        return new, new.minimaze()

    def get_column(self):
        return [pf.row[self.j] for pf in self.points_from]

    def set_column(self, col):
        i = 0
        for pf in self.points_from:
            pf.row[self.j] = col[i]
            i += 1

    # Вычисляет min_dist и penalty, нормализует столбец
    def minimaze(self):
        col = self.get_column()
        m, self.penalty = lib.minimaze(col)
        if m > 0:
            self.min_dist += m
            self.set_column(col)
        return m > 0

#   Хранит текущее состояние и позволяет перейти в следующее
#   при этом порождает новый экземпляр State
class State:
    def __init__(self):
        self.cost = None #оценка минимально возможного маршрута это его расстояние определяется как Sum(point_from + point_to)
        self.points_from = [] # PointFrom - строки таблица расстояний, приведенных к нулю
        self.points_to = [] # PointTo - столбец в таблице расстояний
        self.zero = [] # (penalty, PointFrom, PointTo) список нулевых элементов в приведенной таблице расстояний

    # point_names - имена пуктов назначения
    # tbl - таблица расстояний между пунктами назначения
    def init(self, point_names, tbl):
        n = len(tbl)

        for i in range(n):
            point_from = PointFrom().init(point_names[i], tbl[i][:])
            assert(point_from.row is not tbl[i])
            point_from.minimaze()
            self.points_from.append(point_from)

        for j in range(n):
            point_to = PointTo(self.points_from, j, point_names[j])
            point_to.minimaze()
            self.points_to.append(point_to)

        for pf in self.points_from:
            pf.find_penalty()

        #делаем оценку минимального маршрута
        self.cost = sum(pf.min_dist for pf in self.points_from) + sum(pt.min_dist for pt in self.points_to)

        self.find_zero()

        return self

    def reproduce(self):
        #use self here to customize the new organism ...
        return self.__class__()  # same as cls = type(self); return cls()

    #Создает новое состояние после перехода from_point -> to_point
    def new_state_after_jump(self, point_from, point_to):
        new_state = State()

        print('jump %s -> %s' % (point_from.name, point_to.name))

        #клонируем таблицу расстояний исключая строку "point_from" и столбец "point_to"
        for pf in self.points_from:
            if pf is not point_from:
                new_state.points_from.append(pf.clone(delete = point_to.j))
        assert( len(new_state.points_from) + 1 == len(self.points_from) )

        #копируем points_to в новое сотояние исключая один элемент point_to
        j = 0 #новые индексы для столбцов
        for pt in self.points_to:
            if pt is not point_to:
                pt_clone, min_changed = pt.clone(new_state.points_from, j)
                new_state.points_to.append(pt_clone)
                assert(min_changed != (pt_clone.min_dist == pt.min_dist)) #минимум по пунктам назначения не должен измениться
                j += 1

        # так как минимум по пунктам назначения не изменился то пересчитывать штраф по пунктам отправления нет смысла
        if min_changed:
            for pf in new_state.points_from:
                pf.minimaze()


        #обратный путь помечаем как неиспользуемый
        new_state.mark_unused(point_to.name, point_from.name)

        #делаем оценку минимального маршрута
        new_state.calc_cost()

        new_state.find_zero()

        return new_state

    def mark_unused(self, from_name, to_name):
        for pf in self.points_from:
            if pf.name == from_name:
                break;
        else:
            return
            #raise Exception('not found from_name')

        for pt in self.points_to:
            if pt.name == to_name:
                break
        else:
            return
            #raise Exception('not found to_name')

        #print('from=%s   to=%s' % (pf.name, pt.name))
        pf.row[pt.j] = None
        pf.minimaze()
        pt.minimaze()


    def calc_cost(self): #!!!!!!!!!!!!!!!!!!!!! [0] +
        self.cost = sum([0] + [pf.min_dist for pf in self.points_from]) + sum([0] + [pt.min_dist for pt in self.points_to])

    def find_zero(self):
        for pf in self.points_from:
            for j in range(len(pf.row)):
                if pf.row[j] == 0:
                    pt = self.points_to[j]
                    self.zero.append((pf.penalty + pt.penalty, pf, pt))
        self.zero.sort(key=lambda item: item[0] )

    # выполняем переход на ноль и создаем новое состояние соотвтествующее этому переходу
    def next_zero_jump(self):
        penalty, pf, pt = self.zero[0]
        new_state = self.new_state_after_jump(pf, pt)
        return Jump(pf.name, pt.name, new_state)

    def find_last_tree_jump(self):
        return []

    def print(self):
        print('из\\в', end='\t')
        for pt in self.points_to:
            print('%s(%d)' % (pt.name, pt.min_dist), end = '\t')
        print('')
        print('--------------------------------------------------------------')
        for pf in self.points_from:
            print('%s(%d) |' % (pf.name, pf.min_dist), end='\t')
            pf.print_row()
        print('cost=%d' % self.cost)
        print('')

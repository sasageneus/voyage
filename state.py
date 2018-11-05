import lib
from point import PointFrom
from point import PointTo
from point import jump_distance
from route import Jump

#   Хранит текущее состояние и позволяет перейти в следующее
#   при этом порождает новый экземпляр State
class State:
    def __init__(self):
        self.cost = None #оценка минимально возможного маршрута это его расстояние определяется как Sum(point_from + point_to)
        self.points_from = [] # PointFrom - строки таблица расстояний, приведенных к нулю
        self.points_to = [] # PointTo - столбец в таблице расстояний
        self.zero = [] # (penalty, PointFrom, PointTo) список нулевых элементов в приведенной таблице расстояний
        self.odometer = 0 #пройденная дистанция до этого состояния


    # point_names - имена пуктов назначения
    # tbl - таблица расстояний между пунктами назначения
    def begin(self, point_names, tbl):
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

        new_state.odometer = self.odometer + jump_distance(point_from, point_to)

        #print('jump %s -> %s' % (point_from.name, point_to.name))

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
        #new_state.mark_unused(point_to.name, point_from.name)

        new_state.disable_comeback(point_from, point_to)

        #делаем оценку минимального маршрута
        new_state.calc_cost()

        new_state.find_zero()

        return new_state

    def disable_comeback(self, point_from, point_to):
        if point_to.last_in_chain is None:
            name_to = point_to.name
        else:
            # point_to является началом цепочки, а нам нужен конец цепочки
            name_to = point_to.last_in_chain

        for pf in self.points_from:
            if pf.name == name_to:
                break;
        else:
            raise Exception('not found pf=' + name_to)

        #------------------------------------------------
        if point_from.first_in_chain is None:
            name_from = point_from.name
        else:
            name_from = point_from.first_in_chain

        for pt in self.points_to:
            if pt.name == name_from:
                break
        else:
            # Значит мы продолжили цепочку тоесть вышли из ее конца
            raise Exception('not found pt=' + name_from)

        pf.first_in_chain = name_from
        pt.last_in_chain = name_to

        pf.row[pt.j] = None
        pf.minimaze()
        pt.minimaze()

        return

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
        return Jump(pf.name, pt.name, new_state, jump_distance(pf, pt))

    def find_last_two_jump(self):
        #находим
        pf0 = self.points_from[0]
        pt0 = self.points_to[0]
        pf1 = self.points_from[1]
        pt1 = self.points_to[1]
        if (jump_distance(pf0, pt0) + jump_distance(pf1, pt1)) < (jump_distance(pf1, pt0) + jump_distance(pf0, pt1)):
            return [Jump(pf0.name, pt0.name, self, jump_distance(pf0, pt0)), Jump(pf1.name, pt1.name, self, jump_distance(pf1, pt1))]
        else:
            return [Jump(pf1.name, pt0.name, self, jump_distance(pf1, pt0)), Jump(pf0.name, pt1.name, self, jump_distance(pf0, pt1))]


    def print(self):
        print('из\\в', end='\t')
        for pt in self.points_to:
            print('%s(%d)' % (pt.name, pt.min_dist), end = '\t')
        print('')
        print('--------------------------------------------------------------')
        for pf in self.points_from:
            print('%s(%d) |' % (pf.name, pf.min_dist), end='\t')
            pf.print_row()
        print('cost=%d (%d)' % (self.odometer + self.cost, self.cost))
        print('')


class Jump:
    def __init__(self, from_point, to_point, state, dist):
        self.from_point = from_point # from_point_name
        self.to_point = to_point
        self.state = state #состояние из которого был сделан этот переход
        self.dist = dist
        self.step_num = None # шаг на котором был найден этот переход

    def print(self):
        print('%2d.  %s -> %s distance %d cost %d' % (self.step_num, self.from_point, self.to_point, self.dist, self.state.odometer + self.state.cost) )


class Route:
    def __init__(self):
        self.rt = [] #of Jump

    def __iter__(self):
        jmp = self.rt[0]
        yield jmp
        cnt = 1
        while cnt < len(self.rt):
            jmp = self.find_next_jump(jmp)
            yield jmp
            cnt += 1


    #для восстановления последовательности маршрута
    def find_next_jump(self, jump):
        for next_jmp in self.rt:
            if next_jmp.from_point == jump.to_point:
                return next_jmp
        else:
            raise Exception('find_next_jump not found next point : ' + jump.to_point)


    def finished(self):
        #берем последнее состояние и получаем оставшиеся ходы
        jmp1, jmp2 = self.rt[-1].state.find_last_two_jump()
        self.append(jmp1)
        self.append(jmp2)


    def append(self, jmp):
        jmp.step_num = len(self.rt) + 1
        self.rt.append(jmp)

    # печатает маршрут и проверяет что все пункты пройдены
    def print_chain(self):
        point_names_set = set()
        for jmp in self:
            print(jmp.to_point + ' ', end = '')
            assert(jmp.to_point not in point_names_set)
            point_names_set.add(jmp.to_point)
        print('')

    def print(self):
        for jmp in self.rt:
            jmp.print()

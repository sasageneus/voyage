
class Jump:
    def __init__(self, from_point, to_point, state, dist):
        self.from_point = from_point # from_point_name
        self.to_point = to_point
        self.state = state #состояние из которого был сделан этот переход
        self.dist = dist

    def print(self):
        print('%s -> %s !%d(%d)' % (self.from_point, self.to_point, self.dist, self.state.odometer + self.state.cost) )

#для восстановления последовательности маршрута
def find_next_jump(route, jump):
    for next_jmp in route:
        if next_jmp.from_point == jump.to_point:
            return next_jmp
    else:
        raise Exception('find_next_jump not found next point : ' + jump.to_point)

class Route:
    def __init__(self):
        self.rt = [] #of Jump

    def append(self, jmp):
        self.rt.append(jmp)

    def print(self):
        route_print = self.rt + self.rt[-1].state.find_last_two_jump()
        #route_print[-2].print()
        #route_print[-1].print()
        print('--------------------------------------')
        # так как найденный маршрут не является последовательным,
        #   то надо восстановить правильную последовательность для печати
        jmp = route_print[0] # первый шаг, маршрут закольцован, поэтому не важно какая точка будет начальной!!!
        jmp.print()
        cnt = 1
        while cnt < len(route_print):
            jmp = find_next_jump(route_print, jmp)
            jmp.print()
            cnt += 1

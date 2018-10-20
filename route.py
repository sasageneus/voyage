
class Jump:
    from_point = ''
    to_point = ''
    state = None

    def print(self):
        print('%s -> %s (%d)' % (self.from_point, self.to_point, self.state.cost) )

def find_next_jump(route, jump):
    for next_jmp in route:
        if next_jmp.from_point == jump.to_point:
            return next_jmp
    else:
        raise Exception('find_next_jump not found next point : ' + jump.to_point)

class Route:
    route = [] #of Jump

    def print():
        route_print = self.route + self.route[-1].state.find_last_tree_point()

        jmp = route_print[0] 
        jmp.print()
        cnt = 1
        while cnt < len(route_print):
            jmp = find_next_jump(jmp)
            jmp.print()
            cnt += 1

        

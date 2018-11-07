
class Bruteforce:
    def __init__(self, point_names, tbl):
        self.point_names = point_names
        self.tbl = tbl

    def start(self, point_name):
        for i in range(len(self.point_names)):
            if self.point_names[i] == point_name:
                self.start_i = i
                break
        else:
            raise Exception('point_name not found : ' + point_name)

        self.start_i = 0

        self.visit = [False for i in range(len(self.tbl))]
        self.visit[self.start_i] = True

        d, r = self.min_route_from_i(self.start_i, 1)
        r = (self.start_i, *r)
        print('bruteforce total distance : %d' % d)

        for i in r:
            print(self.point_names[i], end=' ')
        print('')

    def min_route_from_i(self, i, nn):
        best_route = None
        min_dist = 100000000

        if nn == len(self.tbl):
            return self.tbl[i][self.start_i], () #Это последний пункт и тут не может быть вариантов он только один

        for j in range(len(self.tbl)):
            if self.tbl[i][j] is not None and not self.visit[j]:
                self.visit[j] = True
                dist, r = self.min_route_from_i(j, nn + 1)
                dist += self.tbl[i][j]
                if dist < min_dist:
                    min_dist = dist
                    best_route = (j, *r)

                self.visit[j] = False

        return min_dist, best_route

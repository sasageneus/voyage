import lib

def jump_distance(point_from, point_to):
    dist = point_from.row[point_to.j]
    return point_from.min_dist + point_to.min_dist + (dist if dist != None else float('inf'))

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

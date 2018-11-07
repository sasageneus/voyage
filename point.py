import lib

def jump_distance(point_from, point_to):
    dist = point_from.row[point_to.j]
    return point_from.min_dist + point_to.min_dist + (dist if dist != None else float('inf'))

# пункт отправления
class PointFrom:
    def init(self, name, row):
        self.name = None # наименование,
        self.row = None # строка таблицы расстояний
        self.min_dist = 0 # расстояние до ближайшего пункта
        self.penalty = None # размер штрафа если не воспользоваться ближайшим пунктом назначения
        self.first_in_chain = None # Если этот пункт конец цепочки, то здесь будет начало этой цепочки (если очередной шаг был продолжение цепочки то здесь начало этой цепочки )
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
        new.first_in_chain = self.first_in_chain
        return new

    def print_row(self):
        for dist in self.row:
            print('%s' % (str(dist) if dist != None else '-'), end = '\t')
        print('')

# пункт прибытия
class PointTo:
    def __init__(self, points_from, j, name):
        self.min_dist = 0 # расстояние до ближайшего пункта
        self.penalty = None # размер штрафа если не воспользоваться ближайшим пунктом назначения
        self.last_in_chain = None # если этот пункт начало цепочки то здесь будет конец
        self.points_from = points_from #ссылается на одноименное поле в State, используется для доступа к таблице расстояний
        self.j = j # индекс колонки в таблице расстояний
        self.name = name

    def clone(self, points_from, j):
        new = PointTo(points_from, j, self.name)
        new.min_dist = self.min_dist
        new.last_in_chain = self.last_in_chain
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


#возвращает два наименьших по порядку
def min_and_penalty(row):
    m = None
    p = None
    for dist in row:
        if dist != None:
            if m == None or dist < m:
                p = m
                m = dist
            elif p == None or dist < p:
                p = dist
    assert(m != None)
    #assert(p != None)
    return m, p if p else 0

def minimaze(row):
    min_dist, penalty = min_and_penalty(row)
    if min_dist > 0:
        for i in range(len(row)):
            if row[i] != None:
                row[i] -= min_dist
        penalty -= min_dist
    return min_dist, penalty

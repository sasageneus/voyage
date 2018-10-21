
import state as state_py

def common_test():
    lst = [23, 1,3,None,5,6,7,89, 3]
    print(lst)
    d = 8
    print(lst[0:d] + lst[d+1:])    
    print(min(item for item in lst if item is not None))

    min_dist = min(item for item in lst if item is not None)
    row = lst
    print( [dist - min_dist 
              if dist is not None else None 
                  for dist in row ] )
#common_test()

def point_form_test():
    row = [4, 9, 9, None, 3, 6, 7]
    print(row)
    pf = state_py.PointFrom().init('tst', row)
    print(pf.__dict__)
    delete = 4
    print('delete=%d' % delete)
    pf2 = pf.clone(delete)
    print(pf2.__dict__)

#point_form_test()

def point_to_test():
    row = [4, 9, 3, None, 3, 5, 7]
    points_from = []
    for i in range(len(row)):
        row.insert(0, row.pop())
        pf = state_py.PointFrom().init(str(i), row[:])
        points_from.append(pf)
        print(pf.row)
    print('')
    
    pt = state_py.PointTo(points_from, 2, 'col')
    
    col = pt.get_column()
    print(col)
    col[4] = None
    pt.set_column(col)
    col = None
    col = pt.get_column()
    print(col)

    pt.minimaze()
    col = pt.get_column()
    print(col)

    
  
    
    
    print(pt.__dict__)

point_to_test()



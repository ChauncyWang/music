def test():
    b = ['a']
    c = ['b']
    a = [b,c]
    del b
    print(a)

test()
try:
    time1 = raw_input('input a time[hh:mm:ss]:')
    [h1s, m1s, s1s] = time1.split(':')
    [h1, m1, s1] = [int(h1s), int(m1s), int(s1s)]
    foo = 0
    if 0 <= h1 <= 24 and 0 <= m1 <= 60 and 0 <= s1 <= 60:
        foo = 1
    else:
        print 'error time range! Try again!'

    [h2, m2, s2] = [0, 5, 30]
    [h0, m0, s0] = [h1 + h2, m1 + m2, s1 + s2]
    if s0 >= 60:
        m0 += 1
        s0 = s0 - 60
    if m0 >= 60:
        h0 += 1
        m0 = m0 - 60
    if h0 >= 24:
        h0 = h0 - 24

    if foo == 1:
        print 'After 5:30,it would be time [%s:%s:%s]' % (str(h0).zfill(2), str(m0).zfill(2), str(s0).zfill(2))


except ValueError:
    print 'error time format! Try again!'

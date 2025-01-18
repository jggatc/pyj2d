env = None
pg = None
implemented = None


# __pragma__ ('opov')


def init(environ):
    global env, pg
    env = environ
    pg = env['pg']
    check_implemented()
    tests = [test_surfarray_blit_array,
             test_surfarray_make_surface,
             test_surfarray_array2d,
             test_surfarray_array3d,
             test_surfarray_array_alpha]
    return tests


def check_implemented():
    global implemented
    if env['platform'] in ['jvm', 'pc']:
        #jvm uses jnumeric, pc uses numpy
        try:
            surface = pg.Surface((1,1))
            pg.surfarray.array2d(surface)
            implemented = True
        except:
            implemented = False
    elif env['platform'] == 'js':
        #js uses pyjsarray
        implemented = True


def test_surfarray_blit_array():
    if not implemented:
        raise NotImplementedError
    surface = pg.Surface((15,10))
    surface.fill((0,0,0))
    array2d = pg.surfarray.array2d(surface)
    surface.fill((255,0,0))
    assert surface.get_at((0,0)) == (255,0,0,255)
    pg.surfarray.blit_array(surface, array2d)
    assert surface.get_at((0,0)) == (0,0,0,255)
    surface = pg.Surface((15,10))
    surface.fill((0,0,0))
    array3d = pg.surfarray.array3d(surface)
    surface.fill((255,0,0))
    assert surface.get_at((0,0)) == (255,0,0,255)
    pg.surfarray.blit_array(surface, array3d)
    assert surface.get_at((0,0)) == (0,0,0,255)


def test_surfarray_make_surface():
    if not implemented:
        raise NotImplementedError
    surface = pg.Surface((15,10))
    surface.fill((255,0,0))
    if env['platform'] in ('jvm', 'js'):
        array2d = pg.surfarray.array2d(surface)
        surface2d = pg.surfarray.make_surface(array2d)
        assert surface2d.get_size() == (15,10)
        assert surface2d.get_at((0,0)) == (255,0,0,255)
    array3d = pg.surfarray.array3d(surface)
    surface3d = pg.surfarray.make_surface(array3d)
    assert surface3d.get_size() == (15,10)
    assert surface3d.get_at((0,0)) == (255,0,0,255)


def test_surfarray_array2d():
    if not implemented:
        raise NotImplementedError
    surface = pg.Surface((15,10))
    surface.fill((0,0,0))
    array = pg.surfarray.array2d(surface)
    for i in range(10):
        array[0,i] = 255
    assert array[0,0] == 255
    assert array[0,1]>>24 & 0xff == 0
    if env['platform'] == 'jvm':   #array has alpha
    	assert array[1,0]>>24 & 0xff == 255
    surface2 = pg.Surface((15,10), pg.SRCALPHA)
    array2 = pg.surfarray.array2d(surface2)
    for i in range(10):
        array2[0,i] = 255
    assert array2[0,0] == 255
    assert array2[1,0] == 0
    if env['platform'] == 'js':
        array = pg.surfarray.array2d(surface, True)
        for i in range(10):
            array[0,i] = 255
        assert array[0,0] == 255
        surface2 = pg.Surface((15,10), pg.SRCALPHA)
        array2 = pg.surfarray.array2d(surface2, True)
        for i in range(10):
            array2[0,i] = 255
        assert array2[0,0] == 255
        assert array2[1,0] == 0


def test_surfarray_array3d():
    if not implemented:
        raise NotImplementedError
    surface = pg.Surface((15,10))
    surface.fill((0,0,0))
    array = pg.surfarray.array3d(surface)
    if env['platform'] != 'js':
        assert array.shape == (15,10,3)
    else:
        assert array.shape == (10,15,4)
    for i in range(10):
        array[0,i] = (0,0,255)
    assert array[0,0,2] == 255
    assert array[1,0,2] == 0
    if env['platform'] == 'js':
        array = pg.surfarray.array3d(surface, True)
        assert array.shape == (15,10,3)
        for i in range(10):
            array[0,i] = (0,0,255)
        assert array[0,0,2] == 255
        assert array[1,0,2] == 0


def test_surfarray_array_alpha():
    if not implemented:
        raise NotImplementedError
    surface = pg.Surface((15,10))
    surface.fill((0,0,0))
    array = pg.surfarray.array_alpha(surface)
    if env['platform'] != 'js':
        assert array.shape == (15,10)
    else:
        assert array.shape == (10,15,4)
    assert array[1,1] & 0xff == 255
    surface2 = pg.Surface((15,10),pg.SRCALPHA)
    array2 = pg.surfarray.array_alpha(surface2)
    for i in range(10):
        array2[0,i] = 255
    assert array2[0,0] & 0xff == 255
    assert array2[1,0] & 0xff == 0
    if env['platform'] == 'js':
        array = pg.surfarray.array_alpha(surface)
        assert array[1,1] & 0xff == 255
        surface2 = pg.Surface((15,10),pg.SRCALPHA)
        array2 = pg.surfarray.array_alpha(surface2)
        for i in range(10):
            array2[0,i] = 255
        assert array2[0,0] & 0xff == 255
        assert array2[1,0] & 0xff == 0


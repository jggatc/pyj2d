env = None
pg = None
surface = None
width = None
height = None


def init(environ):
    global env, pg, surface, width, height
    env = environ
    pg = env['pg']
    surface = env['surface']
    width = env['width']
    height = env['height']
    tests = [test_surface_get_size,
             test_surface_get_rect,
             test_surface_copy,
             test_surface_blit,
             test_surface_fill,
             test_surface_set_colorkey,
             test_surface_get_colorkey,
             test_surface_set_at,
             test_surface_get_at]
    return tests


def test_surface_get_size():
    assert surface.get_size() == (width,height)    # __:opov
    assert surface.get_width() == width
    assert surface.get_height() == height


def test_surface_get_rect():
    rect = surface.get_rect()
    assert rect == (0,0,width,height)    # __:opov
    assert (rect.x,rect.y,rect.width,rect.height) == (0,0,width,height)    # __:opov
    rect = surface.get_rect(center=(15,15))
    assert (rect.x,rect.y,rect.width,rect.height) == (5,5,width,height)    # __:opov


def test_surface_copy():
    new_surface = surface.copy()
    assert surface == surface    # __:opov
    assert surface != new_surface    # __:opov
    assert surface.get_size() == new_surface.get_size()    # __:opov


def test_surface_blit():
    new_surface = pg.Surface((5,5))
    surface.fill((0,0,0))
    new_surface.fill((100,100,100))
    rect = surface.blit(new_surface, (1,0))
    assert surface.get_at((0,0)) == (0,0,0,255)    # __:opov
    assert surface.get_at((1,0)) == (100,100,100,255)    # __:opov
    assert surface.get_at((0,0)) == pg.Color(0,0,0,255)    # __:opov
    assert surface.get_at((1,0)) == pg.Color(100,100,100,255)    # __:opov
    assert (rect.x,rect.y,rect.width,rect.height) == (1,0,5,5)    # __:opov


def test_surface_fill():
    color = (255,0,0), (0,255,0,255)
    for c in color:
        surface.fill((0,0,0))
        surface.fill(pg.Color(c))
        assert surface.get_at((0,0)) == c    # __:opov


def test_surface_set_colorkey():
    color = (255,0,0), (0,255,0,255), None
    for c in color:
        surface.set_colorkey(c)
        if surface.get_colorkey():
            assert pg.Color(*surface.get_colorkey()) == pg.Color(*c)    # __:opov


def test_surface_get_colorkey():
    surface.fill((0,0,0))
    surface.set_colorkey((0,0,0))
    assert surface.get_colorkey() == (0,0,0,255)    # __:opov
    surface.set_colorkey(None)
    assert surface.get_colorkey() is None


def test_surface_set_at():
    color = (255,0,0), (0,255,0,255)
    for c in color:
        surface.fill((0,0,0))
        surface.set_at((0,0), c)
        assert surface.get_at((0,0)) == c    # __:opov


def test_surface_get_at():
    color = (0,0,255,255)
    surface.fill((0,0,0))
    surface.set_at((0,0), (0,0,255,255))
    assert surface.get_at((0,0)) == (0,0,255,255)    # __:opov
    assert surface.get_at((0,0)) == (0,0,255)    # __:opov


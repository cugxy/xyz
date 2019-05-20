#!coding=utf-8

import pyproj as pj
import numpy


_WGS84 = {
    'geocent': pj.Proj(proj='geocent', ellps='WGS84'),
    'longlat': pj.Proj(proj='latlong', ellps='WGS84'),
    # 'geocent-geoid':    pj.Proj(proj='latlong',ellps='WGS84', geoidgrids=_EGM96),
    # 'latlong-geoid':    pj.Proj(proj='latlong',ellps='WGS84', geoidgrids=_EGM96),
    # 'latlong-geoid2':   pj.Proj(proj='latlong',ellps='WGS84', geoidgrids=_EGM08),
}

# _10TM  = pj.Proj(proj='tmerc',lon_0=-115, k=0.9992, x_0=500000, ellps='GRS80', datum='NAD83', units='m')
_TM = {
    'longlat': pj.Proj(proj='latlong', ellps='WGS84'),
}


def wgs84_to(x, y, z, proj='geocent', tm='10tm'):
    '''
    wgs84转换到其他坐标系
    :param x:
    :param y:
    :param z:
    :param proj:
    :param tm:
    :return:
    '''
    proj, tm = proj.lower(), tm.lower()
    # from IPython import embed; embed()
    assert _WGS84.__contains__(proj)
    assert _TM.__contains__(tm)

    rs = pj.transform(_WGS84[proj], _TM[tm], x, y, z)
    return numpy.array(rs).T


def wgs84_from(e, n, z, proj='geocent', tm='10tm'):
    '''
    从其他转到wgs84
    :param e:
    :param n:
    :param z:
    :param proj:
    :param tm:
    :return:
    '''
    proj, tm = proj.lower(), tm.lower()
    assert _WGS84.__contains__(proj)
    # 如果找不到,默认采用epsg初始化的方式
    p = _TM.get(tm, None)
    if not p:
        p = pj.Proj(init=tm)
    rs = pj.transform(p, _WGS84[proj], e, n, z)
    return numpy.array(rs).T


# 从epsg转换
def wgs84_from_epsg(e, n, z, epsg, proj='geocent'):
    assert _WGS84.__contains__(proj)
    rs = pj.transform(pj.Proj(init=epsg), _WGS84[proj], e, n, z)
    return numpy.array(rs).T


def popM_from(x, y, z):
    '''
    prcs_xyz*M => wgs84_xyz
    xyz should be wgs84
    :param x:
    :param y:
    :param z:
    :return:
    '''
    arr = wgs84_to(x, y, z, tm='longlat')[:2]
    arr = numpy.radians(arr)  # long,lat
    sa, sb = numpy.sin(arr)
    ca, cb = numpy.cos(arr)
    return numpy.array([
        [-sa, -ca * sb, ca * cb, x],
        [ca, -sa * sb, sa * cb, y],
        [0, cb, sb, z],
        [0, 0, 0, 1]
    ]).T


def inv_popM(M):
    '''
    raw major, matrix: ecef->prcs
    '''
    inv_popM_R = M[:3, :3].T
    inv_popM_t = -M[3, :3].dot(inv_popM_R)
    invM = numpy.zeros_like(M)
    invM[:3, :3] = inv_popM_R
    invM[3, :3] = inv_popM_t
    invM[3, 3] = 1
    return invM


# --------------------------------------------
def prcs_from(arr, popM, tm='wgs84'):
    assert numpy.allclose(popM[:3, 3], 0), 'popM should be raw majar'
    if tm.lower() == 'prcs':
        return arr
    if arr.ndim == 1:
        if tm.lower() != 'wgs84':
            arr = wgs84_from(*arr, tm=tm)
        return numpy.dot((arr - popM[3, 0:3]), popM[0:3, 0:3].T)

    if tm.lower() != 'wgs84':
        arr = wgs84_from(arr[:, 0], arr[:, 1], arr[:, 2], tm=tm)
    # sR,sC =  popM.strides
    offset = popM[3, 0:3]  # as_strided( popM[3,0:3], shape=arr.shape,strides=(0,sC))
    return numpy.dot((arr - offset), popM[0:3, 0:3].T)


def prcs_to(arr, popM, tm='wgs84'):
    assert numpy.allclose(popM[:3, 3], 0), 'popM should be raw majar'
    if tm.lower() == 'prcs':  return arr

    if arr.ndim == 1:
        arr = numpy.dot(arr, popM[0:3, 0:3]) + popM[3, 0:3]
        if tm.lower() == 'wgs84': return arr
        return wgs84_to(*arr, tm=tm)
    # sR,sC =  popM.strides
    # offset = as_strided( popM[3,0:3], shape=arr.shape,strides=(0,sC))
    offset = popM[3, 0:3]
    arr = numpy.dot(arr, popM[0:3, 0:3]) + offset
    if tm.lower() == 'wgs84': return arr
    return wgs84_to(arr[:, 0], arr[:, 1], arr[:, 2], tm=tm)


def dd2dms(v):
    av = abs(v)
    d = int(av)
    m = int((av - d) * 60)
    s = ((av - d) * 60 - m) * 60.
    return (d if v > 0 else -d, m, s)


def dms2dd(d, m, s):  # -111°23'49.3794"
    v = (s / 60. + m) / 60. + abs(d)
    return v if d > 0 else -v




if __name__ == "__main__":
    if 0:
        # 将wkt 坐标转成proj4的格式
        from osgeo import osr

        wkt = 'PROJCS["WGS_1984_UTM_Zone_50N",GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],' \
              'PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],' \
              'PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",117.0],' \
              'PARAMETER["Scale_Factor",0.9996],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]'

        spatialRef = osr.SpatialReference()
        spatialRef.ImportFromWkt(wkt)
        pj4 = spatialRef.ExportToProj4()
        p = pj.Proj(pj4)

    if 1:#test calc angle

        arr0 = wgs84_to(2420682.7446169774, 4643724.861889638, 3628773.944194785, tm='longlat')[:3]
        import numpy as np
        xyz = np.array([[2420682.7446169774, 4643724.861889638, 3628773.944194785], [2420682.7446169774, 4643724.861889638, 3628773.944194785],
               [2420682.7446169774, 4643724.861889638, 3628773.944194785]])
        xyz = xyz.T
        rs = wgs84_to(xyz[0].T,xyz[1].T,xyz[2].T, tm='longlat')
        x = xyz[0]-xyz[1]
        y = xyz[2]-xyz[1]
        Lx = np.sqrt(x.dot(x))
        Ly = np.sqrt(y.dot(y))
        # 相当于勾股定理，求得斜线的长度
        cos_angle = x.dot(y) / (Lx * Ly)
        # 求得cos_sita的值再反过来计算，绝对长度乘以cos角度为矢量长度
        print(cos_angle)
        angle = np.arccos(cos_angle)
        xy_angle = angle * 360 / 2 / np.pi

        utm = pj.Proj(proj='utm', zone=50, ellps='WGS84')
        #x, y = utm(116.81449815, 30.87368477)
        geoxyz = []
        for e in xyz:
            rs = wgs84_from(e[0], e[1], e[2],proj='longlat', tm='EPSG:32647')
            rs_xyz = wgs84_from(*rs, tm='longlat')
            utm_xyz =utm(rs[0], rs[1])
            geoxyz.append([utm_xyz[0],utm_xyz[1],0])

        geoxyz = np.array(geoxyz)

        gx = geoxyz[0] - geoxyz[1]
        gy = geoxyz[2] - geoxyz[1]
        Lx = np.sqrt(gx.dot(gx))
        Ly = np.sqrt(gy.dot(gy))
        # 相当于勾股定理，求得斜线的长度
        cos_angle = gx.dot(gy) / (Lx * Ly)
        # 求得cos_sita的值再反过来计算，绝对长度乘以cos角度为矢量长度，初中知识。。
        print(cos_angle)
        angle = np.arccos(cos_angle)
        geo_angle = angle * 360 / 2 / np.pi

    lat, lng = [55.73837752, -120.87148552]
    lat, lng = [30.87368477, 116.81449815]
    utm = pj.Proj(proj='utm', zone=50, ellps='WGS84')
    x, y = utm(116.81449815, 30.87368477)
    # wgs84_to(*xyz, tm='longlat')


    _origin = wgs84_from(lng, lat, 0, proj='longlat', tm='50n')
    _origin = wgs84_from(lng, lat, 0, tm='longlat')
    print(wgs84_to(*_origin, tm='longlat'))
    pi = 3.141592653589793

    # -2186028.37642936,5182643.67968226,2996929.20455705  -2189441.407211436, 5181558.599819444, 2996318.0221550893
    # -2189441.407211436, 5181558.599819444, 2996318.0221550893
    # Marker created at (-2189370.825118118, 5179874.404784049, 2999260.3319733655)
    lat, lng = [28.20893149804916, 112.86991647789996]
    height = 16.21145287772694
    lat, lng = [26.845711, 106.720883]
    _origin = wgs84_from(lng, lat, 0, tm='longlat')

    arr0 = wgs84_to(2420682.7446169774, 4643724.861889638, 3628773.944194785, tm='longlat')[:3]

    #  -2189370.825118118, 5179874.404784049, 2999260.3319733655
    arr1 = wgs84_to(840579.1305296770296991, -5543881.8706182111054659, 3029485.9996336135081947, tm='longlat')[:3]
    arr0 = [106.720883, 26.845711]
    lat_offset = arr1[1] - arr0[1]
    lng_offset = arr1[0] - arr0[0]

    rs = wgs84_from(arr1[0], arr1[1], arr1[2], proj='geocent', tm='longlat')
    pm = popM_from(rs[0], rs[1], rs[2])

    lat, lng = [23.03508 - lat_offset, 113.77631 - lng_offset]
    lat, lng = [23.03508, 113.77631]
    height = 20  # 16.21145287772694
    rs = wgs84_from(lng, lat, height, proj='geocent', tm='longlat')
    pm1 = popM_from(rs[0], rs[1], rs[2])
    Y1 = (numpy.linalg.inv(pm)).dot(pm1)
    print(list(Y1.flatten()))
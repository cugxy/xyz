#!coding=utf-8

import os
if not os.environ.get('MPLCONFIGDIR',None):
    import getpass
    os.environ['MPLCONFIGDIR'] = '/home/%s/.matplotlib'%(getpass.getuser(),)
import numpy
from numpy.lib.stride_tricks import as_strided
import matplotlib

if os.name == 'posix':
    matplotlib.use('Agg')
else:
    try:
        from mayavi import mlab
    except (ImportError, ValueError) as e:
        pass


def show(): 
    mlab.show()

# -------------------------------------------------------------


def show_cloud(arr, idx=None, color=None, colormap=None):
    A = numpy.atleast_2d(arr)
    A = A.T if idx is None else (A[idx]).T
    
    if color is None:
        return mlab.points3d(A[0],A[1],A[2],mode='point')
    colormap = colormap or 'blue-red'
    return mlab.points3d(A[0],A[1],A[2], color=color, mode='point', colormap=colormap)


def _show_obj(arr, radius, scales, color, mode):
    B = numpy.atleast_2d(arr).T
    if scales is None:
        return mlab.points3d(B[0],B[1],B[2],scale_mode='none',
            scale_factor=radius*2,
            color= color if not color is None else (0.67, 0.77, 0.93),
            opacity=0.3,
            mode=mode
        )
    return mlab.points3d(B[0],B[1],B[2],scales, scale_mode='none',
        scale_factor=radius*2,
        opacity=0.3,
        mode=mode
    )


def show_balls(arr, radius, scales=None, color=None):
    return _show_obj(arr,radius, scales, color, mode='sphere')


def show_cubes(arr, length, scales=None, color=None):
    return _show_obj(arr,length, scales, color, mode='cube')


def show_ndarray(arr,radius, color=None):
    return mlab.points3d(arr[0],arr[1],arr[2],scale_mode='none',
        scale_factor=radius*2,
        color= color or (0.67, 0.77, 0.93),
        opacity=0.3,
        name='ball'
    )


def show_eigen(vals,vcts, m=None, scale=None):
    if scale is None:
        evals = numpy.array([1., 1., 1.])
    else:
        evals = numpy.sqrt(scale*numpy.abs(vals))
        evals /= evals.max() 
    
    evals = as_strided(evals, shape=vcts.shape, strides=(evals.strides[0],0))
    v = (vcts * evals).T
    if m is None:
        m = numpy.zeros((3,3))
    else:
        m = as_strided(m, shape=vcts.shape, strides=(0,m.strides[0])).T

    mlab.quiver3d( 
         m[0],m[1],m[2],
         v[0],v[1],v[2],
         line_width=1, scale_factor=1
    )


def show_quiver(arr, vct, scale=1., color=None):
    m, v = arr.T, vct.T
    mlab.quiver3d( 
         m[0], m[1], m[2],
         v[0], v[1], v[2],
         line_width=1, scale_factor=scale, color=color
    )


def show_tin(arr, idx, color=None, colormap=None, suface=False):
    A = numpy.atleast_2d(arr)
    A = A.T
    x = A[0]
    y = A[1]
    z = A[2]
    representation = 'wireframe'
    if suface:
        representation = 'surface'
    if color is None:
        return mlab.triangular_mesh(x, y, z, idx, representation=representation)
    return mlab.triangular_mesh(x, y, z, idx, color=color, colormap=colormap, representation=representation)


if __name__ == '__main__':
    # print('import ok')
    from IPython import embed
    if 0:
        from scipy.spatial import Delaunay
        n = numpy.random.random((100, 3))
        # pts = show_cloud(arr=n, color=(0.0, 0.0, 1.0))
        xy = n[:,0:2]
        tin = Delaunay(xy)
        idx = tin.simplices
        x = n.T[0]
        y = n.T[1]
        z = n.T[2]
        # mlab.triangular_mesh(x, y, z, idx, representation='wireframe')
        show_tin(n, idx, color=(1, 0, 0), colormap='')
    if 1:
        import numpy as np
        from scipy.spatial import Delaunay
        X = np.arange(-20, 20, 0.1)
        Y = np.arange(-20, 20, 0.1)
        X, Y = np.meshgrid(X,Y)
        X = X.reshape(-1)
        Y = Y.reshape(-1)
        R = np.sqrt(X**2 + Y**2)
        Z = np.cos(R)
        xy = np.c_[(X, Y)]
        tin = Delaunay(xy)
        idx = tin.simplices
        xyz = np.c_[(xy, Z)]
        show_tin(xyz, idx, color=(1, 0, 0), colormap='blue-red')
    show()
    pass


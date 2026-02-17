from numpy import ndarray
from scipy.interpolate import interp1d

def interext(x1: ndarray, x2: ndarray, v: ndarray) -> ndarray:
    inter = interp1d(x2, v, kind = 'quadratic', fill_value = 'extrapolate')
    return inter(x1)

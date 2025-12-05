
import numpy as np


def funcio_optimitzar(x):
    return np.exp(x) - 3 * x

def _punt_mig(a,b):
    return (a+b) / 2

presicio = 1e-9

# a < b
a_0 = np.log(3)
b_0 = 2

def bolzano_biseccio(func,a,b,presicio)->tuple[float,float,dict]:
    def get_error(a,b):
        return (a-b) / 2


    a_iter = a_0
    b_iter = b_0

    c = np.inf

    i = 0
    while i < 1_000_000:
        i+=1
        c = _punt_mig(a_iter,b_iter)
        func_c = funcio_optimitzar(c)
        if np.abs(func_c) < presicio:
            break
        elif func_c > 0:
            b_iter = c
        elif func_c < 0:
            a_iter = c

    return c,get_error(a_iter,b_iter),{"iter":i}

def newton_ralphson_simple(func,deriv,a,b,presicio)->tuple[float,float,dict]:
    raise NotImplementedError

def bolzano_regula_falsi(func,a,b,presicio)->tuple[float,float,dict]:
    i = 0
    raise NotImplementedError
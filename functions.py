import numpy as np

def pend(x, t, faks, f, xm):
    eps = 1e-4
    x_safe = np.clip(x, eps, 1.0)
    
    S = lambda: f3(t, faks[0])
    F = lambda: f3(t, faks[1])
    G = lambda: f3(t, faks[2])
    T = lambda: f3(t, faks[3])
    A = lambda: f3(t, faks[4])
    D = lambda: f3(t, faks[5])
    I = lambda: f3(t, faks[6])
    P = faks[7][3]
    C = faks[8][3]

    dkdt = [
        (1 / xm[0]) * f3(S(), f[0]) * f0x8(x_safe, f[1]) * (1 - x_safe[0]),
        (1 / xm[1]) * F() * G() * f3(S(), f[2]) * f0x8(x_safe, f[3]) * (1 - x_safe[1]) - f0x1(x_safe, f[4]) * f0x7(x_safe, f[5]),
        (1 / xm[2]) * f0x8(x_safe, f[6]) * f0x1(x_safe, f[7]) * (1 - x_safe[2]),
        (1 / xm[3]) * F() * G() * T() * f0x8(x_safe, f[8]) * f0x7(x_safe, f[9]) * f0x1(x_safe, f[10]) * (1 - x_safe[3]),
        (1 / xm[4]) * A() * f3(S(), f[11]) * (1 - x_safe[4]) - f0x1(x_safe, f[12]) * f0x7(x_safe, f[13]),
        (1 / xm[5]) * f3(S(), f[14]) * f0x8(x_safe, f[15]) * (1 - x_safe[5]),
        (1 / xm[6]) * f0x1(x_safe, f[16]) * (1 - x_safe[6]),
        (1 / xm[7]) * D() * f3(S(), f[17]) * (1 - x_safe[7]) - f0x4(x_safe, f[18]),
        (1 / xm[8]) * I() * f3(S(), f[19]) * (1 - x_safe[8]) - f0x1(x_safe, f[20]) * f0x7(x_safe, f[21]),
        (1 / xm[9]) * F() * G() * T() * f3(S(), f[22]) * f0x1(x_safe, f[23]) * f0x7(x_safe, f[24]) * (1 - x_safe[9]),
        (1 / xm[10]) * P * C * F() * G() * D() * f3(S(), f[25]) * f0x6(x_safe, f[26]) * (1 - x_safe[10]),
        (1 * xm[11]) * f0x11(x_safe, f[27]) * (1 - x_safe[11])
    ]
    
    for i in range(len(dkdt)):
        if x[i] <= eps and dkdt[i] < 0:
            dkdt[i] = 0.0
        if x[i] >= 0.999 and dkdt[i] > 0:
            dkdt[i] = 0.0

    return dkdt
def fx(x, params):
    return params[0] * x ** 4 + params[1] * x ** 3 + params[2] * x ** 2 + params[3] * x + params[4]


def f3(x, params):
    return params[0] * x ** 3 + params[1] * x ** 2 + params[2] * x + params[3]


def f0x8(t, p):
    x = x8(t)
    return fx(x, p)


def f0x1(t, p):
    x = x1(t)
    return fx(x, p)


def f0x7(t, p):
    x = x7(t)
    return fx(x, p)


def f0x4(t, p):
    x = x4(t)
    return fx(x, p)


def f0x6(t, p):
    x = x6(t)
    return fx(x, p)


def f0x11(t, p):
    x = x11(t)
    return fx(x, p)


def x1(t):
    return fx1(t[0])


def x2(t):
    return fx2(t[1])


def x3(t):
    return fx3(t[2])


def x4(t):
    return fx4(t[3])


def x5(t):
    return fx5(t[4])


def x6(t):
    return fx6(t[5])


def x7(t):
    return fx7(t[6])


def x8(t):
    return fx8(t[7])


def x9(t):
    return fx9(t[8])


def x10(t):
    return fx10(t[9])


def x11(t):
    return fx11(t[10])


def x12(t):
    return fx12(t[11])


def fx1(t):
    return np.clip(0.3 + 0.2 * t, 0.3, 0.8)

def fx2(t):
    return np.clip(0.4 - 0.1 * t, 0.3, 0.7)

def fx3(t):
    return np.clip(0.5 - 0.15 * t, 0.35, 0.8)

def fx4(t):
    return np.clip(0.2 + 0.3 * t, 0.2, 0.7)

def fx5(t):
    return np.clip(0.6 - 0.2 * t, 0.4, 0.8)

def fx6(t):
    return np.clip(0.4 + 0.25 * t, 0.4, 0.8)

def fx7(t):
    return np.clip(0.5 - 0.1 * t, 0.4, 0.8)

def fx8(t):
    return np.clip(0.3 + 0.3 * t, 0.3, 0.8)

def fx9(t):
    return np.clip(0.4 - 0.05 * t, 0.35, 0.7)

def fx10(t):
    return np.clip(0.2 + 0.4 * t, 0.2, 0.8)

def fx11(t):
    return np.clip(0.5 - 0.15 * t, 0.35, 0.8)

def fx12(t):
    return np.clip(0.3 + 0.35 * t, 0.3, 0.8)
def pend(x, t, faks, f, xm):
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
        # 0
        (
                (1 / xm[0]) * f3(S(), f[0]) * f0x8(x, f[1])
        ),

        # 1
        (
                (1 / xm[1]) * F() * G() * f3(S(), f[2]) * f0x8(x, f[3]) - f0x1(x, f[4]) * f0x7(x, f[5])
        ),

        # 2
        (
                (1 / xm[2]) * f0x8(x, f[6]) * f0x1(x, f[7])
        ),

        # 3
        (
                (1 / xm[3]) * F() * G() * T() * f0x8(x, f[8]) * f0x7(x, f[9]) * f0x1(x, f[10])
        ),

        # 4
        (
                (1 / xm[4]) * A() * f3(S(), f[11]) - f0x1(x, f[12]) * f0x7(x, f[13])
        ),

        # 5
        (
                (1 / xm[5]) * f3(S(), f[14]) * f0x8(x, f[15])
        ),

        # 6
        (
                (1 / xm[6]) * f0x1(x, f[16])
        ),

        # 7
        (
                (1 / xm[7]) * D() * f3(S(), f[17]) - f0x4(x, f[18])
        ),

        # 8
        (
                (1 / xm[8]) * I() * f3(S(), f[19]) - f0x1(x, f[20]) * f0x7(x, f[21])
        ),

        # 9
        (
                (1 / xm[9]) * F() * G() * T() * f3(S(), f[22]) * f0x1(x, f[23]) * f0x7(x, f[24])
        ),

        # 10
        (
                (1 / xm[10]) * P * C * F() * G() * D() * f3(S(), f[25]) * f0x6(x, f[26])
        ),

        # 11
        (
                (1 * xm[11]) * f0x11(x, f[27])
        )
    ]
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
    return 0.001 * t ** 3 + 0.0665 * t ** 2 - 0.0345 * t - 0.008


def fx2(t):
    return -0.0536 * t ** 3 + 0.4455 * t ** 2 - 0.786 * t + 0.447


def fx3(t):
    return -0.011 * t ** 3 + 0.151 * t ** 2 - 0.14 * t + 0.25


def fx4(t):
    return 0.0923 * t ** 3 - 0.859 * t ** 2 + 2.6156 * t - 1.849


def fx5(t):
    return -0.04 * t ** 3 + 0.288 * t ** 2 - 0.187 * t + 0.239


def fx6(t):
    return -0.0063 * t ** 3 + 0.104 * t ** 2 + 0.107 * t + 0.045


def fx7(t):
    return 0.03 * t ** 3 - 0.032 * t ** 2 + 0.01 * t + 0.023


def fx8(t):
    return 0.0132 * t ** 3 - 0.0245 * t ** 2 + 0.245 * t - 0.067


def fx9(t):
    return -0.009 * t ** 3 + 0.1115 * t ** 2 - 0.06 * t - 0.038


def fx10(t):
    return 0.16 * t ** 3 - 1.5 * t ** 2 + 4.57 * t - 3.23


def fx11(t):
    return 0.004 * t ** 3 + 0.01 * t ** 2 + 0.21 * t - 0.22


def fx12(t):
    return 0.034 * t ** 3 - 0.127 * t ** 2 + 0.24 * t

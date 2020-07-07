'''
@Author: Glimmer
@Date: 2020-05-25 13:17:39
@LastEditTime: 2020-07-04 12:02:25
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /code/element.py
'''

import numpy as np
from util import Gauss2D
from util import Gauss1D


class recElement:
    def __init__(self, number, node, side):
        self.number = number
        self.node = node
        self.side = side
        self.h1 = self.node[1].locationx - self.node[0].locationx
        self.h2 = self.node[2].locationy - self.node[1].locationy

        # 单元刚度矩阵, 6阶高斯积分
        BMatrix = lambda xi,eta,h1,h2 : np.array([[(eta-1)/h1, (1-eta)/h1, -eta/h1, eta/h1],[(xi-1)/h2, -xi/h2, (1-xi)/h2, xi/h2]])
        Ae = 0
        for i in Gauss2D:
            Ae += np.dot(
                BMatrix(i['lambda1'], i['lambda2'], self.h1, self.h2).T,
                BMatrix(i['lambda1'], i['lambda2'], self.h1,
                        self.h2)) * i['rho'] * self.h1 * self.h2
        self.Ae = Ae

        # 单元载荷向量，6阶高斯积分
        self.elementLoadVector = 0
        for i in Gauss2D:
            x_ = self.h1 * i['lambda1'] + self.node[0].locationx
            y_ = self.h2 * i['lambda2'] + self.node[0].locationy
            self.elementLoadVector += self.fx(x_, y_) * self.NVector(
                i['lambda1'], i['lambda2']) * i['rho'] * self.h1 * self.h2

        # 线元载荷向量, 3阶高斯积分
        self.lineLoadVector = 0
        for i in range(3):
            s = 0
            for para in Gauss1D:
                a = (para['lambda'] + 1) / 2
                x_ = self.h1 * a + self.node[0].locationx
                y_ = self.h2 * a + self.node[0].locationy
                s += self.NVector(a, a) * self.lx(
                    x_, y_, self.side[i]) * side[i].length * para['rho'] * 0.5
            self.lineLoadVector += s

    def NVector(self, xi, eta):
        N0 = (1 - xi) * (1 - eta)
        N1 = xi * (1 - eta)
        N2 = (1 - xi) * eta
        N3 = xi * eta
        return np.array([[N0, N1, N2, N3]]).T

    def fx(self, x, y):
        return 2 * (x + y)

    def lx(self, x, y, side):
        if side.marker == 2:
            return (-2 - 2 * y - y**2)
        elif side.marker == 3:
            return (-2 - x - x * x)
        else:
            return 0


class recSide:
    def __init__(self, number, node, marker):
        self.node = node
        self.number = number
        self.marker = marker
        self.length = ((node[0].locationx - node[1].locationx)**2 +
                       (node[0].locationy - node[1].locationy)**2)**0.5


class recNode:
    def __init__(self, number, locationx, locationy, marker):
        self.number = number
        self.locationx = locationx
        self.locationy = locationy
        self.marker = marker
        self.u = 0

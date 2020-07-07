'''
@Author: Glimmer
@Date: 2020-05-25 13:17:39
@LastEditTime: 2020-05-28 14:47:47
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /code/element.py
'''

import numpy as np
from util import Gauss2D
from util import Gauss1D


class Element:
    def __init__(self, number, node, side):
        self.number = number
        self.node = node
        self.side = side
        deltaMatrix = np.array(
            [[self.node[0].locationx, self.node[0].locationy, 1],
             [self.node[1].locationx, self.node[1].locationy, 1],
             [self.node[2].locationx, self.node[2].locationy, 1]])
        self.delta = 0.5 * np.linalg.det(deltaMatrix)
        
        # 单元刚度矩阵
        BMatrix = 1 / (2 * self.delta) * np.array(
            [[
                self.node[1].locationy - self.node[2].locationy,
                self.node[2].locationy - self.node[0].locationy,
                self.node[0].locationy - self.node[1].locationy
            ],
             [
                 self.node[2].locationx - self.node[1].locationx,
                 self.node[0].locationx - self.node[2].locationx,
                 self.node[1].locationx - self.node[0].locationx
             ]])
        self.Ae = np.dot(BMatrix.T, BMatrix) * self.delta

        x = np.array([[node.locationx for node in self.node]])
        y = np.array([[node.locationy for node in self.node]])
        
        # 单元载荷向量，6阶高斯积分
        self.elementLoadVector = 0
        for i in Gauss2D:
            a = np.array(
                [[i['lambda1'], i['lambda2'],
                  1 - i['lambda2'] - i['lambda1']]]).T
            x_ = np.dot(x, a)[0, 0]
            y_ = np.dot(y, a)[0, 0]
            self.elementLoadVector += self.fx(x_, y_) * self.NVector(
                x_, y_) * i['rho'] * self.delta

        # 线元载荷向量
        self.lineLoadVector = 0
        for i in range(3):
            s = 0
            for para in Gauss1D:
                a = [0, 0, 0]
                a[i - 2] = (para['lambda'] + 1) / 2
                a[i - 1] = 1 - a[i - 2]
                aVector = np.array([a]).T
                x_ = np.dot(x, aVector)[0, 0]
                y_ = np.dot(y, aVector)[0, 0]
                s += self.NVector(x_, y_) * self.lx(
                    x_, y_, self.side[i]) * side[i].length * para['rho'] * 0.5
            self.lineLoadVector += s

    def NVector(self, x, y):
        NiMatrix = np.array(
            [[x, y, 1], [self.node[1].locationx, self.node[1].locationy, 1],
             [self.node[2].locationx, self.node[2].locationy, 1]])
        Ni = 1 / (2 * self.delta) * np.linalg.det(NiMatrix)
        NjMatrix = np.array(
            [[x, y, 1], [self.node[2].locationx, self.node[2].locationy, 1],
             [self.node[0].locationx, self.node[0].locationy, 1]])
        Nj = 1 / (2 * self.delta) * np.linalg.det(NjMatrix)
        NkMatrix = np.array(
            [[x, y, 1], [self.node[0].locationx, self.node[0].locationy, 1],
             [self.node[1].locationx, self.node[1].locationy, 1]])
        Nk = 1 / (2 * self.delta) * np.linalg.det(NkMatrix)
        return np.array([[Ni, Nj, Nk]]).T

    def fx(self, x, y):
        return 2 * (x + y)

    def lx(self, x, y, side):
        if side.marker == 2:
            return (-2 - 2 * y - y**2)
        elif side.marker == 3:
            return (-2 - x - x * x)
        else:
            return 0


class Side:
    def __init__(self, number, node, marker):
        self.node = node
        self.number = number
        self.marker = marker
        self.length = ((node[0].locationx - node[1].locationx)**2 +
                       (node[0].locationy - node[1].locationy)**2)**0.5


class Node:
    def __init__(self, number, locationx, locationy, marker):
        self.number = number
        self.locationx = locationx
        self.locationy = locationy
        self.marker = marker
        self.u = 0

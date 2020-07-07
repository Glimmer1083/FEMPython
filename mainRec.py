'''
@Author: Glimmer
@Date: 2020-05-25 10:04:40
@LastEditTime: 2020-07-04 17:11:27
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /undefined/Users/Glimmer/Desktop/CIAE/基础课程/有限元方法/上机/code/main.py
'''
# -*- coding: UTF-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from scipy import linalg
from scipy.interpolate import griddata

from recElement import *

nodeFile = "./E.n"
sideFile = "./E.s"
elementFile = "./E.e"


def read_node(filename):
    with open(filename, 'r') as file_to_read:
        nodes = []
        lines = file_to_read.readline()
        item = [i for i in lines.split()]
        nodeNum = int(item[0])
        for index in range(nodeNum):
            lines = file_to_read.readline()
            item = [i for i in lines.split()]
            node = recNode(int(item[0]), float(item[1]), float(item[2]), int(item[3]))
            nodes.append(node)
    return nodes


def read_side(filename, nodes):
    with open(filename, 'r') as file_to_read:
        sides = []
        lines = file_to_read.readline()
        item = [i for i in lines.split()]
        sideNum = int(item[0])
        for index in range(sideNum):
            lines = file_to_read.readline()
            item = [i for i in lines.split()]
            side = recSide(int(item[0]), [nodes[int(item[1])], nodes[int(item[2])]], int(item[3]))
            sides.append(side)
    return sides


def create_elements(filename, nodes, sides):
    with open(filename, 'r') as file_to_read:
        elements = []
        lines = file_to_read.readline()
        item = [i for i in lines.split()]
        elementNum = int(item[0])
        for index in range(elementNum):
            lines = file_to_read.readline()
            item = [i for i in lines.split()]
            element = recElement(int(item[0]), [nodes[int(item[1])], nodes[int(item[2])], nodes[int(item[3])], nodes[int(item[4])]], [sides[int(item[5])], sides[int(item[6])], sides[int(item[7])], sides[int(item[8])]])
            elements.append(element)
    return elements


print("FEM: read nodes...")
nodes = read_node(nodeFile)
print("FEM: read sides...")
sides = read_side(sideFile, nodes)
print("FEM: create elements...")
elements = create_elements(elementFile, nodes, sides)
print("FEM: create the matrix...")

# 单元合成，构造有限元矩阵
Ae_ = np.zeros((len(nodes), len(nodes)))
fe_ = np.zeros((len(nodes), 1))
for element in elements:
    for i in range(4):
        for j in range(4):
            if Ae_[element.node[i].number, element.node[j].number] == 0:
                Ae_[element.node[i].number, element.node[j].number] = element.Ae[i, j]
            else:
                Ae_[element.node[i].number, element.node[j].number] += element.Ae[i, j]
    for i in range(4):
        if fe_[element.node[i].number, 0] == 0:
            fe_[element.node[i].number, 0] = element.elementLoadVector[i, 0] + element.lineLoadVector[i, 0]
        else:
            fe_[element.node[i].number, 0] += (element.elementLoadVector[i, 0] + element.lineLoadVector[i, 0])
    # pass

for node in nodes:
    if node.marker == 1 or node.marker == 4:
        Ae_[node.number, :] = 0
        Ae_[:, node.number] = 0
        Ae_[node.number, node.number] = 1
        fe_[node.number, 0] = 0
print("FEM: solve the problem...")

u = linalg.solve(Ae_, fe_)
x = []
y = []
z = []
index = 0
for node in nodes:
    node.u = u[index, 0]
    x.append(node.locationx)
    y.append(node.locationy)
    z.append(node.u + node.locationx**2 + node.locationy**2)
    index = index + 1

# 画网格，插值得到二维网格点的值，画云图
xi = np.linspace(min(x),max(x),300)
yi = np.linspace(min(y),max(y),300)
X, Y = np.meshgrid(xi,yi) #网格化
Z = griddata((x, y), z, (X, Y), method='cubic')
cset = plt.contourf(X, Y, Z, 20, cmap=plt.cm.hot)
contour = plt.contour(X, Y, Z, 20, colors='k')
plt.clabel(contour,fontsize=10,colors='k')
plt.colorbar(cset)
plt.show()
'''
@Author: Glimmer
@Date: 2020-05-25 23:05:40
@LastEditTime: 2020-06-25 21:27:36
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /code/util.py
'''

GaussFile = "./Gauss.dat"


def read_gauss(filename):
    with open(filename, 'r') as file_to_read:
        Gauss = []
        lines = file_to_read.readline()
        item = [i for i in lines.split()]
        n = int(item[0])
        for index in range(n):
            lines = file_to_read.readline()
            item = [i for i in lines.split()]
            i = {
                'lambda1': float(item[0]),
                'lambda2': float(item[1]),
                'rho': float(item[2])
            }
            Gauss.append(i)
    return Gauss


Gauss2D = read_gauss(GaussFile)

Gauss1D = [{
    'lambda': -0.7745966692,
    'rho': 0.555555556
}, {
    'lambda': 0,
    'rho': 0.888888889
}, {
    'lambda': 0.7745966692,
    'rho': 0.555555556
}]
'''
@Author: your name
@Date: 2020-07-04 12:54:21
@LastEditTime: 2020-07-04 17:31:57
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /code/meshRec.py
'''
def getNodes(h1, h2, Nx, Ny, filename):
  f = open(filename, "w")
  f.write("{0}\n".format(Nx*Ny))
  for i in range(Nx):
    for j in range(Ny):
      nodeNumber = i * Nx + j
      locationx = i * h1 / (Nx - 1)
      locationy = j * h2 / (Ny - 1)
      if j == 0 and i < Nx - 1:
        nodeMarker = 1
      elif j == Ny - 1 and i != 0:
        nodeMarker = 3
      elif i == 0 and j != 0:
        nodeMarker = 4
      elif i == Nx - 1 and j < Ny - 1:
        nodeMarker = 2
      else:
        nodeMarker = 0
      f.write("{0:5d}  {1:10.5f}  {2:10.5f}  {3:5d}\n".format(nodeNumber, locationx, locationy, nodeMarker))
  f.close()

def getSides(Nx, Ny, filename):
  f = open(filename, "w")
  f.write("{0}\n".format(Nx*(Ny-1)+Ny*(Nx-1)))
  for i in range(Nx):
    for j in range(Ny - 1):
      sideNumber = i * (Ny - 1) + j
      node1 = i * Ny + j + 1
      node2 = i * Ny + j
      if i == 0:
        sideMarker = 4
      elif i == Nx - 1:
        sideMarker = 2
      else:
        sideMarker = 0
      f.write("{0:5d}  {1:5d}  {2:5d}  {3:5d}\n".format(sideNumber, node1, node2, sideMarker))
  for i in range(Ny):
    for j in range(Nx - 1):
      sideNumber = i * (Nx - 1) + j + Nx * (Ny - 1)
      node1 = j * Ny + i
      node2 = j * Ny + i + Ny
      if i == 0:
        sideMarker = 1
      elif i == Ny - 1:
        sideMarker = 3
      else:
        sideMarker = 0
      f.write("{0:5d}  {1:5d}  {2:5d}  {3:5d}\n".format(sideNumber, node1, node2, sideMarker))
  f.close()

def getElements(Nx, Ny, filename):
  f = open(filename, "w")
  f.write("{0}\n".format((Nx-1)*(Ny-1)))
  for i in range(Nx - 1):
    for j in range(Ny - 1):
      elementNumber = i * (Ny - 1) + j
      node0 = i * Ny + j
      node1 = (i + 1) * Ny + j
      node2 = (i + 1) * Ny + j + 1
      node3 = i * Ny + j + 1
      # sides
      side0 = Nx * (Ny - 1) + j * (Nx - 1) + i
      side1 = (i + 1) * (Ny - 1) + j
      side2 = Nx * (Ny - 1) + j * (Nx - 1) + i + Nx - 1
      side3 = (i + 1) * (Ny - 1) + j - Ny + 1
      f.write("{0:5d}  {1:5d}  {2:5d}  {3:5d}  {4:5d}  {5:5d}  {6:5d}  {7:5d} {8:5d}\n".format(elementNumber, node0, node1, node2, node3, side0, side1, side2, side3))
  
  
if __name__ == "__main__":
    Nx = 51
    Ny = 51
    getNodes(2,2,Nx,Ny,'E.n')
    getSides(Nx,Ny,'E.s')
    getElements(Nx,Ny,'E.e')

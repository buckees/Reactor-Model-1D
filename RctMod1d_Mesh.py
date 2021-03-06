"""
Define Mesh.

Mesh --> 1d or 2d.
Mesh contains:
    x position
"""

from Geometry import Geom_1d

import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy

class Mesh_1d(Geom_1d):
    """Define 1d Mesh."""

    def __init__(self, label, width, nx=11, res=0.1):
        """Add option to choose nx or res for mesh."""
        super().__init__(label, width)
        self.nx = nx
        self.delx = self.width/(self.nx-1)
        self.x = np.linspace(0.0, self.width, self.nx)

    def __str__(self):
        """Print 1d mesh information."""
        res = 'Mesh_1d:'
        res += '\n ' + super().__str__()
        res += f'\nnx = {self.nx}'
        res += f'\ndelx = {self.delx} m'
        return res

    def add_bndy(self):
        """Add boundaries."""
        pass

    def add_mat(self):
        """Add materials."""
        pass

    def plot_mesh(self):
        """Plot 1d mesh in X."""
        fig, ax = plt.subplots(1, 1, figsize=(4, 4),
                               constrained_layout=True)
        y = np.zeros_like(self.x)
        ax.plot(self.x, y, 'o')
        plt.show(fig)

    def cnt_diff(self, y):
        """
        Caculate dy/dx using central differencing.
        
        input: y
        dy/dx = (y[i+1] - y[i-1])/(2.0*dx)
        dy[0] = dy[1]; dy[-1] = dy[-2]
        output: dy
        """
        dy = np.zeros_like(self.x)
        # Although dy[0] and dy[-1] are signed here,
        # they are eventually specified in boundary conditions
        # dy[0] = dy[1]; dy[-1] = dy[-2]
        for i in range(1, self.nx-1):
            dy[i] = (y[i+1] - y[i-1])/self.delx/2.0
        dy[0], dy[-1] = deepcopy(dy[1]), deepcopy(dy[-2])
        return dy
    
    def cnt_diff_2nd(self, y):
        """
        Caculate d2y/dx2 using 2nd order central differencing.

        input: y
        d2y/dx2 = (y[i+1] - 2 * y[i] + y[i-1])/dx^2
        d2y[0] = d2y[1]; d2y[-1] = d2y[-2]
        output: d2y/dx2
        """
        d2y = np.zeros_like(self.x)
        # Although dy[0] and dy[-1] are signed here,
        # they are eventually specified in boundary conditions
        # d2y[0] = d2y[1]; d2y[-1] = d2y[-2]
        for i in range(1, self.nx-1):
            d2y[i] = (y[i+1] - 2 * y[i] + y[i-1])/self.delx**2
        d2y[0], d2y[-1] = deepcopy(d2y[1]), deepcopy(d2y[-2])
        return d2y


if __name__ == '__main__':
    """Test Mesh."""
    geom1d = Geom_1d('A', 10e-2)
    mesh1d = Mesh_1d(geom1d.label, geom1d.width,
                     nx=101)
    # print(geom1d)
    print(mesh1d)
    mesh1d.plot_mesh()

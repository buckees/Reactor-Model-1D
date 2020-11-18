"""
Geometry module 1D, constructing the 1D geometry.

1D geometry is made of intervals.
Assign materials to the shapes, such as
'Metal', 'Quartz', etc.

1D geometry is defined separately from 2D geometry,
but they share the same strucuture.
"""

import matplotlib.pyplot as plt
import numpy as np

class Interval():
    """Init the Interval."""
    
    def __init__(self, label, lr):
        """
        Init the Interval.
        
        lr: unit in m, (2, ) tuple, defines the domain
        label: str, var, label of Interval.
        """
        self.lr = np.asarray(lr)
        self.label = label

    def __str__(self):
        """Print Shape info."""
        return f'label = {self.label}'
    
    def __contains__(self, posn):
        """
        Determind if a position is inside the Interval.
        
        posn: unit in m, (2, ) array, position as input
        boundaries are not consindered as "Inside"
        """
        return self.lr[0] <= posn and posn <= self.lr[1]

class Domain(Interval):
    """Define the Domain."""
    
    def __init__(self, lr=(0.0, 1.0)):
        """
        Init the Domain.
        
        lr: unit in m, (2, ) tuple, defines the domain
        label: Domain label is fixed to 'Plasma'
        """
        super().__init__(label='Plasma', lr=lr)
        self.type = 'Domain'

    def __str__(self):
        """Print Domain info."""
        res = 'Domain:'
        res += f'\nlabel = {self.label}'
        res += f'\nleft and right boundaries = {self.bndy} m'
        return res

class Segment(Interval):
    """Segment is a basic Interval."""
    
    def __init__(self, label, lr):
        """
        Init the Segment.
        
        lr: unit in m, (2, ) tuple, left and right boundaries of the segment
        label: str, var, label of Interval.
        type: str, var, type of Interval
        """
        super().__init__(label, lr)
        self.type = 'Segment'

    def __str__(self):
        """Print Rectangle info."""
        res = 'Rectangle:'
        res += f'\nleft and right bndy = {self.lr} m'
        return res



class Geom1d():
    """Constuct the 1D geometry."""
    
    def __init__(self, name='Geometry', is_cyl=False):
        """
        Init the 1D geometry.
        
        dim = 1, this class only supports 1D geometry
        is_cyl: bool, wether the geometry is cylidrical symmetric or not
        """
        self.name = name
        self.dim = 1
        self.is_cyl = is_cyl
        self.num_mat = 0
        self.label = None
        self.sequence = list()

    def __str__(self):
        """Print Geometry info."""
        res = f'Geometry dimension {self.dim}D'
        if self.is_cyl:
            res += ' cylindrical'
        res += '\nGeometry sequence:'
        for shape in self.sequence:
            res += '\n' + str(shape)
        return res

    def add_domain(self, domain):
        """
        Add domain to the geometry.
        
        domain: class
        lr: unit in m, (2, ) tuple, bndy of the domain
        label: dict, label <-> number
        """
        self.lr = domain.lr
        self.label ={domain.label:0}
        self.num_mat = 1

    def add_segment(self, segment):
        """
        Add segment to 1D geometry.
        
        segment: class
        """
        if self.num_mat:
            self.sequence.append(segment)
            if segment.label in self.label:
                pass
            else:
                self.num_mat += 1
                self.label[segment.label] = self.num_mat - 1
        else:
            res = 'Domian is not added yet.'
            res += '\nRun self.add_domain() before self.add_shape()'
            return res

    def get_label(self, posn):
        """
        Return the label of a position.
        
        posn: unit in m, var, position as input
        label: str, var, label of the segment
        """
        # what if return None
        label = 'Plasma'
        for segment in self.sequence:
            if posn in segment:
                label = segment.label
        return label, self.label[label]

    def label_check(self, posn, label):
        """
        Check if labelf of posn == label of input.
        
        posn: unit in m, var or (2, ) array, position as input
        label: str, var, label as input
        """
        # cannot determined if the posn is in domain
        res = False
        posn_label = self.get_label(posn)
        return res or (posn_label == label)
    
    def plot(self, figsize=(8, 8), dpi=300):
        """
        Plot the 1D geometry.
        
        figsize: unit in inch, (2, ) tuple, determine the fig/canvas size
        dpi: dimless, int, Dots Per Inch
        """
        color_dict = {0:'white', 1:'black', 2:'green', 3:'yellow', 
                      4:'blue', 5:'pink', 6:'grey'}
        
        fig, ax = plt.subplots(1, 1, figsize=figsize, dpi=dpi,
                               constrained_layout=True)
        
        ax.plot(self.lr, (0.0, 0.0), 'o-',
                linewidth=5, color='purple', markersize=16)
        for segment in self.sequence:
            temp_col = color_dict[self.label[segment.label]]
            ax.plot(segment.lr, (0.0, 0.0), 'o-',
                linewidth=5, color=temp_col, markersize=16)
        # for ax in axes:
        #     ax.set_xlim(self.bl[0], self.bl[0] + self.domain[0])
        #     ax.set_ylim(self.bl[1], self.bl[1] + self.domain[1])
        fig.savefig(self.name, dpi=dpi)
        plt.close()
if __name__ == '__main__':
    """Test 1D Geometry."""
    geom1d = Geom1d(name='1D_Test', is_cyl=False)
    domain1d = Domain(lr=(-10.0, 10.0))
    geom1d.add_domain(domain1d)
    seg1 = Segment('M', (-10.0, -8.0))
    geom1d.add_segment(seg1)
    seg2 = Segment('M', (5.0, 10.0))
    geom1d.add_segment(seg2)
    seg3 = Segment('D', (-6.0, 0.0))
    geom1d.add_segment(seg3)
    geom1d.plot()
    print(geom1d)

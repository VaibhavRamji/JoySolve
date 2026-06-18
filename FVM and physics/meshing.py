class Mesh:
    def __init__(self,length,width,height,nx,ny,nz):
        self.length = length # Length of domain
        self.width = width # width of domain
        self.height = height # height of domain
        self.nx = nx  # number of cells in x direction
        self.ny = ny # number of cells in y direction
        self.nz = nz # number of cells in z direction
        self.calculate_cell_sizes

    def calculate_cell_sizes(self):
        dx = self.length / self.nx # Length of individual cell in x axis
        dy = self.width / self.ny # Length of individual cell in y axis
        dz = self.height / self.nz # Length of individual cell in z axis

        self.dx = dx
        self.dy = dy 
        self.dz = dz

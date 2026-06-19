class Mesh:
    def __init__(self,length,width,height,nx,ny,nz):
        self.length = length # Length of domain
        self.width = width # width of domain
        self.height = height # height of domain
        self.nx = nx  # number of cells in x direction
        self.ny = ny # number of cells in y direction
        self.nz = nz # number of cells in z direction
        self.calculate_cell_sizes()
        self.calculate_cell_volume()
        self.calculate_cell_area()

    def calculate_cell_sizes(self):
        self.dx = self.length / self.nx # Length of individual cell in x axis
        self.dy = self.width / self.ny # Length of individual cell in y axis
        self.dz = self.height / self.nz # Length of individual cell in z axis
    
    def calculate_cell_volume(self):
        self.cell_volume = self.dx * self.dy * self.dz # cell volume for a uniform structured mesh
    
    def calculate_cell_area(self):
        self.Ax = self.dy * self.dz # Cell area
        self.Ay = self.dx * self.dz # Cell area
        self.Az = self.dx * self.dy # Cell area



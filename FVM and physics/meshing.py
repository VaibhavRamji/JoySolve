class Mesh:
    def __init__(self,length,width,height,nx,ny,nz):
        self.length = length # Length of domain
        self.width = width # width of domain
        self.height = height # width of domain
        self.nx = nx  # number of cells in x direction
        self.ny = ny # number of cells in y direction
        self.nz = nz # number of cells in z direction

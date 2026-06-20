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
        self.generate_cell_data()

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

    def generate_cell_data(self):
        self.boundary_cells = []
        self.neighbouring_cells = []
        self.cell_centers = []
        self.face_centers = []
        self.cell_indices = []
        for i in range(self.nx): # Loop over x cells
            for j in range(self.ny): # Loop over y cells
                for k in range(self.nz): # Loop over z cells
                    #Find cell centers
                    x = (i + 0.5) * self.dx
                    y = (j + 0.5) * self.dy
                    z = (k + 0.5) * self.dz

                    #Find neighbouring cells:
                    Xp = (i+1,j,k) if i+1 < self.nx else None
                    Xm = (i-1,j,k) if i-1 >= 0 else None
                    Yp = (i,j+1,k) if j+1 < self.ny else None
                    Ym = (i,j-1,k) if j-1 >= 0 else None
                    Zp = (i,j,k+1) if k+1 < self.nz else None
                    Zm = (i,j,k-1) if k-1 >= 0 else None

                    # Find Boundary cells
                    if i in (0, self.nx-1) or j in (0, self.ny-1) or k in (0, self.nz-1):
                        self.boundary_cells.append((i, j, k))

                    #Find face centers:
                    x_plus = (x + self.dx/2,y,z)
                    x_minus = (x - self.dx/2,y,z)

                    y_plus = (x,y + self.dy/2,z)
                    y_minus = (x,y - self.dy/2,z)

                    z_plus = (x,y,z + self.dz/2)
                    z_minus = (x,y,z - self.dz/2)

                    self.cell_indices.append((i,j,k)) # Appends each cell indice to list: cell_indices
                    self.face_centers.append((x_plus,x_minus,y_plus,y_minus,z_plus,z_minus)) # Append face center value to list: face_centers
                    self.neighbouring_cells.append((Xp,Xm,Yp,Ym,Zp,Zm)) # Append neighbouring cells to list: neighbouring_cells
                    self.cell_centers.append((x,y,z)) # Append cell center values to list: cell_centers

   


                    
                    



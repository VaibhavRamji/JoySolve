from meshing import Mesh
import numpy as np

class FVM:

    # test commit 
    @staticmethod
    def face_and_cell_centered_velocities(u, v, w, cell_id, mesh):

        neighbours = mesh.neighbouring_cells[cell_id]

        Xp = neighbours["Xp"]
        Xm = neighbours["Xm"]
        Yp = neighbours["Yp"]
        Ym = neighbours["Ym"]
        Zp = neighbours["Zp"]
        Zm = neighbours["Zm"]

        i, j, k = mesh.cell_indices[cell_id]

        u_p = u[i,j,k]
        v_p = v[i,j,k]
        w_p = w[i,j,k]

        u_x_plus  = u[Xp] if Xp is not None else u_p
        u_x_minus = u[Xm] if Xm is not None else u_p
        u_y_plus  = u[Yp] if Yp is not None else u_p
        u_y_minus = u[Ym] if Ym is not None else u_p
        u_z_plus  = u[Zp] if Zp is not None else u_p
        u_z_minus = u[Zm] if Zm is not None else u_p

        v_x_plus  = v[Xp] if Xp is not None else v_p
        v_x_minus = v[Xm] if Xm is not None else v_p
        v_y_plus  = v[Yp] if Yp is not None else v_p
        v_y_minus = v[Ym] if Ym is not None else v_p
        v_z_plus  = v[Zp] if Zp is not None else v_p
        v_z_minus = v[Zm] if Zm is not None else v_p

        w_x_plus  = w[Xp] if Xp is not None else w_p
        w_x_minus = w[Xm] if Xm is not None else w_p
        w_y_plus  = w[Yp] if Yp is not None else w_p
        w_y_minus = w[Ym] if Ym is not None else w_p
        w_z_plus  = w[Zp] if Zp is not None else w_p
        w_z_minus = w[Zm] if Zm is not None else w_p

        u_face = {
            "x_plus": 0.5*(u_p + u_x_plus),
            "x_minus": 0.5*(u_p + u_x_minus),
            "y_plus": 0.5*(u_p + u_y_plus),
            "y_minus": 0.5*(u_p + u_y_minus),
            "z_plus": 0.5*(u_p + u_z_plus),
            "z_minus": 0.5*(u_p + u_z_minus),
        }

        v_face = {
            "x_plus": 0.5*(v_p + v_x_plus),
            "x_minus": 0.5*(v_p + v_x_minus),
            "y_plus": 0.5*(v_p + v_y_plus),
            "y_minus": 0.5*(v_p + v_y_minus),
            "z_plus": 0.5*(v_p + v_z_plus),
            "z_minus": 0.5*(v_p + v_z_minus),
        }

        w_face = {
            "x_plus": 0.5*(w_p + w_x_plus),
            "x_minus": 0.5*(w_p + w_x_minus),
            "y_plus": 0.5*(w_p + w_y_plus),
            "y_minus": 0.5*(w_p + w_y_minus),
            "z_plus": 0.5*(w_p + w_z_plus),
            "z_minus": 0.5*(w_p + w_z_minus),
        }

        return {
            "u": {"center": u_p, "faces": u_face},
            "v": {"center": v_p, "faces": v_face},
            "w": {"center": w_p, "faces": w_face},
        }

    @staticmethod
    def fluxes(rho, u_face, v_face, w_face,mesh):

        Ax = mesh.Ax
        Ay = mesh.Ay
        Az = mesh.Az

        # X-direction flux
        Fx_plus = rho * u_face["x_plus"] * Ax
        Fx_minus = rho * u_face["x_minus"] * Ax

        # Y-direction flux
        Fy_plus = rho * v_face["y_plus"] * Ay
        Fy_minus = rho * v_face["y_minus"] * Ay

        # Z-direction flux
        Fz_plus = rho * w_face["z_plus"] * Az
        Fz_minus = rho * w_face["z_minus"] * Az

        return {
            "Fx+": Fx_plus,
            "Fx-": Fx_minus,
            "Fy+": Fy_plus,
            "Fy-": Fy_minus,
            "Fz+": Fz_plus,
            "Fz-": Fz_minus,
        }

    @staticmethod
    def advection_term(
        Fx_plus,
        Fx_minus,
        Fy_plus,
        Fy_minus,
        Fz_plus,
        Fz_minus,
        u_face,
        v_face,
        w_face,
        mesh
    ):

        V = mesh.cell_volume

        ADVu = (
            (Fx_minus * u_face["x_minus"] - Fx_plus * u_face["x_plus"])
            + (Fy_minus * u_face["y_minus"] - Fy_plus * u_face["y_plus"])
            + (Fz_minus * u_face["z_minus"] - Fz_plus * u_face["z_plus"])
        ) / V

        ADVv = (
            (Fx_minus * v_face["x_minus"] - Fx_plus * v_face["x_plus"])
            + (Fy_minus * v_face["y_minus"] - Fy_plus * v_face["y_plus"])
            + (Fz_minus * v_face["z_minus"] - Fz_plus * v_face["z_plus"])
        ) / V

        ADVw = (
            (Fx_minus * w_face["x_minus"] - Fx_plus * w_face["x_plus"])
            + (Fy_minus * w_face["y_minus"] - Fy_plus * w_face["y_plus"])
            + (Fz_minus * w_face["z_minus"] - Fz_plus * w_face["z_plus"])
        ) / V

        return ADVu, ADVv, ADVw, V

    @staticmethod
    def diffusion(
        nu,
        u_x_plus,
        u_x_minus,
        u_y_plus,
        u_y_minus,
        u_z_plus,
        u_z_minus,
        u_p,
        v_x_plus,
        v_y_plus,
        v_z_plus,
        v_p,
        v_x_minus,
        v_y_minus,
        v_z_minus,
        w_z_plus,
        w_y_plus,
        w_x_plus,
        w_p,
        w_x_minus,
        w_y_minus,
        w_z_minus,
        mesh
    ):

        Diffu = nu * (
            (u_x_plus - 2 * u_p + u_x_minus) / mesh.dx**2
            + (u_y_plus - 2 * u_p + u_y_minus) / mesh.dy**2
            + (u_z_plus - 2 * u_p + u_z_minus) / mesh.dz**2
        )

        Diffv = nu * (
            (v_x_plus - 2 * v_p + v_x_minus) / mesh.dx**2
            + (v_y_plus - 2 * v_p + v_y_minus) / mesh.dy**2
            + (v_z_plus - 2 * v_p + v_z_minus) / mesh.dz**2
        )

        Diffw = nu * (
            (w_x_plus - 2 * w_p + w_x_minus) / mesh.dx**2
            + (w_y_plus - 2 * w_p + w_y_minus) / mesh.dy**2
            + (w_z_plus - 2 * w_p + w_z_minus) / mesh.dz**2
        )

        return Diffu, Diffv, Diffw

    @staticmethod
    def velocity_update(
        u_p,
        v_p,
        w_p,
        ADVu,
        ADVv,
        ADVw,
        Diffu,
        Diffv,
        Diffw,
        dt,
    ):

        u_new = u_p + dt * (-ADVu + Diffu)
        v_new = v_p + dt * (-ADVv + Diffv)
        w_new = w_p + dt * (-ADVw + Diffw)

        return u_new, v_new, w_new
    
    def pressure_poisson(u_x_plus,u_x_minus,v_y_plus,v_y_minus,w_z_plus,w_z_minus,mesh,p):
        RHS = [
            (u_x_plus - u_x_minus) / (2*mesh.dx) + (v_y_plus - v_y_minus) / (2*mesh.dy) + (w_z_plus - w_z_minus) / (2*mesh.dz)
        ]
        LHS = (
            (np.roll(p, -1, axis=0) - 2*p + np.roll(p, 1, axis=0)) / mesh.dx**2 +
            (np.roll(p, -1, axis=1) - 2*p + np.roll(p, 1, axis=1)) / mesh.dy**2 +
            (np.roll(p, -1, axis=2) - 2*p + np.roll(p, 1, axis=2)) / mesh.dz**2
            ) 
        return RHS,LHS


    

    
        
    


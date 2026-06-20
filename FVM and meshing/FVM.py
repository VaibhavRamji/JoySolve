from meshing import Mesh

class FVM:

    @staticmethod
    def face_and_cell_centered_velocites(u, v, w, i, j, k):

        # --- U component ---
        u_p = u[i, j, k]

        u_x_plus = u[i + 1, j, k]
        u_x_minus = u[i - 1, j, k]
        u_y_plus = u[i, j + 1, k]
        u_y_minus = u[i, j - 1, k]
        u_z_plus = u[i, j, k + 1]
        u_z_minus = u[i, j, k - 1]

        u_face = {
            "x_plus": 0.5 * (u_p + u_x_plus),
            "x_minus": 0.5 * (u_p + u_x_minus),
            "y_plus": 0.5 * (u_p + u_y_plus),
            "y_minus": 0.5 * (u_p + u_y_minus),
            "z_plus": 0.5 * (u_p + u_z_plus),
            "z_minus": 0.5 * (u_p + u_z_minus),
        }

        # --- V component ---
        v_p = v[i, j, k]

        v_x_plus = v[i + 1, j, k]
        v_x_minus = v[i - 1, j, k]
        v_y_plus = v[i, j + 1, k]
        v_y_minus = v[i, j - 1, k]
        v_z_plus = v[i, j, k + 1]
        v_z_minus = v[i, j, k - 1]

        v_face = {
            "x_plus": 0.5 * (v_p + v_x_plus),
            "x_minus": 0.5 * (v_p + v_x_minus),
            "y_plus": 0.5 * (v_p + v_y_plus),
            "y_minus": 0.5 * (v_p + v_y_minus),
            "z_plus": 0.5 * (v_p + v_z_plus),
            "z_minus": 0.5 * (v_p + v_z_minus),
        }

        # --- W component ---
        w_p = w[i, j, k]

        w_x_plus = w[i + 1, j, k]
        w_x_minus = w[i - 1, j, k]
        w_y_plus = w[i, j + 1, k]
        w_y_minus = w[i, j - 1, k]
        w_z_plus = w[i, j, k + 1]
        w_z_minus = w[i, j, k - 1]

        w_face = {
            "x_plus": 0.5 * (w_p + w_x_plus),
            "x_minus": 0.5 * (w_p + w_x_minus),
            "y_plus": 0.5 * (w_p + w_y_plus),
            "y_minus": 0.5 * (w_p + w_y_minus),
            "z_plus": 0.5 * (w_p + w_z_plus),
            "z_minus": 0.5 * (w_p + w_z_minus),
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


    

    
        
    


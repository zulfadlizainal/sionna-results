import sionna.rt

# Other imports
import matplotlib.pyplot as plt
import numpy as np
import drjit as dr
import mitsuba as mi

no_preview = True # Toggle to False to use the preview widget

import matplotlib.pyplot as plt
import numpy as np

from sionna.rt import load_scene, PlanarArray, Transmitter, Receiver, ITURadioMaterial,\
    Camera, PathSolver, InteractionType, RadioMapSolver
from sionna.rt.utils import r_hat

scene = load_scene(sionna.rt.scene.simple_wedge, merge_shapes=False)

if no_preview:
    # Render scene
    my_cam = Camera(position=[10,-100,100], look_at=[10,0,0])
    scene.render(camera=my_cam);
    
if not no_preview:
    scene.preview();
    
scene.frequency = 1e9 # 1GHz
scene.objects["wedge"].radio_material = ITURadioMaterial("metal", itu_type="metal", thickness=100)

# Configure the antenna arrays used by the transmitters and receivers
scene.tx_array = PlanarArray(num_rows=1,
                             num_cols=1,
                             vertical_spacing=0.5,
                             horizontal_spacing=0.5,
                             pattern="iso",
                             polarization="V")

scene.rx_array = scene.tx_array

# Transmitter
tx_angle = 30/180*dr.pi # Angle phi from the 0-face
tx_dist = 50 # Distance from the edge
tx_pos = 50*r_hat(dr.pi/2, tx_angle)
ref_boundary = (dr.pi - tx_angle)/dr.pi*180
los_boundary = (dr.pi + tx_angle)/dr.pi*180
scene.add(Transmitter(name="tx",
                      position=tx_pos,
                      orientation=[0,0,0]))

# Receivers
# We place num_rx receivers uniformly spaced on the segment of a circle around the wedge
num_rx = 1000 # Number of receivers
rx_dist = 5 # Distance from the edge
phi = dr.linspace(mi.Float, 1e-2, 3/2*dr.pi-1e-2, num=num_rx)
theta = dr.pi/2*dr.ones(mi.Float, num_rx)
rx_pos = rx_dist*r_hat(theta, phi)

for i in range(num_rx):
    scene.add(Receiver(name=f"rx-{i}",
                       position=[rx_pos.x[i], rx_pos.y[i], rx_pos.z[i]],
                       orientation=[0,0,0]))
    
# Render scene
my_cam.position = [-30,100,100]
my_cam.look_at([10,0,0])
if no_preview:
    scene.render(camera=my_cam);
    
if not no_preview:
    scene.preview()
    
# Compute paths between the transmitter and all receivers
paths = PathSolver()(scene,
                     max_depth=1,
                     los=True,
                     specular_reflection=True,
                     diffraction=True,
                     edge_diffraction=False,
                     refraction=False,
                     diffuse_reflection=False)

# Obtain channel impulse responses
# We squeeze irrelevant dimensions
# [num_rx, max_num_paths]
a, tau = [np.squeeze(t) for t in paths.cir(out_type="numpy")]

n = 400
plt.figure()
plt.stem(tau[n]/1e-9, 10*np.log10(np.abs(a[n])**2))
plt.title(fr"Angle of receiver $\phi: {int(phi[n]/dr.pi*180)}^\circ$");
plt.xlabel("Delay (ns)");
plt.ylabel("$|a|^2$ (dB)");

h_f_tot = np.sum(a, axis=-1)

fig = plt.figure()
plt.plot(phi.numpy()/dr.pi*180, 20*np.log10(np.abs(h_f_tot)))
plt.xlabel(r"Diffraction angle $\phi$ (deg)");
plt.ylabel(r"Path gain $|H(f)|^2$ (dB)");
plt.ylim([-100, -59]);
plt.xlim([0, phi[-1]/dr.pi*180]);

def plot(frequency, material):
    """Plots the path gain $|H(f)|^2 versus $phi$ for a given
       frequency and RadioMaterial of the wedge.
    """
    # Set carrier frequency and material of the wedge
    # You can see a list of available materials by executing
    # scene.radio_materials
    scene.frequency = frequency
    used_material = scene.get(material)
    if used_material is None:
        scene.objects["wedge"].radio_material = ITURadioMaterial(material, itu_type=material, thickness=100)
    else:
        scene.objects["wedge"].radio_material = used_material

    # Recompute paths with the updated material and frequency
    paths = PathSolver()(scene,
                         max_depth=1,
                         los=True,
                         specular_reflection=True,
                         diffraction=True,
                         edge_diffraction=False,
                         refraction=False,
                         diffuse_reflection=False)
    a, _ = paths.cir(out_type="numpy")
    a = np.squeeze(a)

    # Separate LoS, reflected, and diffracted paths
    interactions = np.squeeze(paths.interactions.numpy())
    valid = np.squeeze(paths.valid.numpy())
    a_los = []
    a_reflected = []
    a_diffracted = []
    for i in range(num_rx):
        # LoS
        los_index = np.where(np.logical_and(valid[i], interactions[i] == InteractionType.NONE))[0]
        if los_index.shape[0] == 0:
            a_los.append(0.)
        else:
            a_los.append(a[i][los_index][0])
        # Reflection
        ref_index = np.where(np.logical_and(valid[i], interactions[i] == InteractionType.SPECULAR))[0]
        if ref_index.shape[0] == 0:
            a_reflected.append(0.)
        else:
            a_reflected.append(a[i][ref_index][0])
        # Diffraction
        dif_index = np.where(np.logical_and(valid[i], interactions[i] == InteractionType.DIFFRACTION))[0]
        if dif_index.shape[0] == 0:
            a_diffracted.append(0.)
        else:
            a_diffracted.append(a[i][dif_index][0])
    a_los = np.array(a_los)
    a_reflected = np.array(a_reflected)
    a_diffracted = np.array(a_diffracted)

    def compute_gain(a):
        """Compute $|H(f)|^2 are f = 0 where H(f) is the baseband channel frequency response"""
        if len(a.shape) == 2:
                h_f_2 = np.abs(np.sum(a, axis=-1))**2

        else:
                h_f_2 = np.abs(a)**2
        h_f_2 = np.where(h_f_2==0, 1e-24, h_f_2)
        g_db = 10*np.log10(h_f_2)
        return np.squeeze(g_db)

    # Compute gain for all path types
    g_tot_db = compute_gain(a)
    g_los_db = compute_gain(a_los)
    g_ref_db = compute_gain(a_reflected)
    g_dif_db = compute_gain(a_diffracted)

    # Make a nice plot
    fig = plt.figure()
    phi_deg = phi.numpy()/np.pi*180
    ymax = np.max(g_tot_db)+5
    ymin = ymax - 45
    plt.plot(phi_deg, g_tot_db)
    plt.plot(phi_deg, g_los_db)
    plt.plot(phi_deg, g_ref_db)
    plt.plot(phi_deg, g_dif_db)
    plt.ylim([ymin, ymax])
    plt.xlim([phi_deg[0], phi_deg[-1]]);
    plt.legend(["Total", "LoS", "Reflected", "Diffracted"], loc="lower left")
    plt.xlabel(r"Diffraction angle $\phi$ (deg)")
    plt.ylabel(r"Path gain $|H(f)|^2$ (dB)")
    ax = fig.axes[0]
    ax.axvline(x=ref_boundary, ymin=0, ymax=1, color="black", linestyle="--")
    ax.axvline(x=los_boundary, ymin=0, ymax=1, color="black", linestyle="--")
    ax.text(ref_boundary-10,ymin+5,'RSB',rotation=90,va='top')
    ax.text(los_boundary-10,ymin+5,'ISB',rotation=90,va='top')
    ax.text(ref_boundary/2,ymax-2.5,'Region I', ha='center', va='center',
            bbox=dict(facecolor='none', edgecolor='black', pad=4.0))
    ax.text(los_boundary-(los_boundary-ref_boundary)/2,ymax-2.5,'Region II', ha='center', va='center',
            bbox=dict(facecolor='none', edgecolor='black', pad=4.0))
    ax.text(phi_deg[-1]-(phi_deg[-1]-los_boundary)/2,ymax-2.5,'Region III', ha='center', va='center',
            bbox=dict(facecolor='none', edgecolor='black', pad=4.0))
    plt.title('$f={}$ GHz ("{}")'.format(frequency/1e9, material))
    plt.tight_layout()
    return fig

plot(1e9, "metal");

plot(10e9, "metal");

plot(100e9, "metal");

plot(1e9, "wood");

# Coverage Maps

scene = load_scene(sionna.rt.scene.simple_street_canyon, merge_shapes=True)

# Set the carrier frequency to 1GHz
scene.frequency = 1e9

scene.tx_array = PlanarArray(num_rows=1,
                             num_cols=1,
                             vertical_spacing=0.5,
                             horizontal_spacing=0.5,
                             pattern="iso",
                             polarization="V")

scene.rx_array = scene.tx_array

scene.add(Transmitter(name="tx",
                      position=[-33,11,32],
                      orientation=[0,0,0]))

# Render scene
my_cam = Camera([-1.5,-137,115])
my_cam.look_at([0,0,10])
if no_preview:
    scene.render(camera=my_cam);
    
if not no_preview:
    scene.preview();
    
radio_map_solver = RadioMapSolver()
cm = radio_map_solver(scene, cell_size=(1, 1), samples_per_tx=10**7,
                      refraction=False) # Deactivate refraction

# Add a camera looking at the scene from the top
my_cam = Camera(position=[10,0,300], look_at=[0,0,0])
my_cam.look_at([0,0,0])

# Render scene with the new camera and overlay the coverage map
scene.render(camera=my_cam, radio_map=cm, rm_show_color_bar=True);

cm = radio_map_solver(scene, cell_size=(1, 1), samples_per_tx=10**7,
                      los=True,
                      specular_reflection=True,
                      refraction=False, # Deactivate refraction
                      diffraction=True) # Activate diffraction
scene.render(camera=my_cam, radio_map=cm, rm_show_color_bar=True);

scene = load_scene(sionna.rt.scene.simple_street_canyon)
scene.frequency = 30e9
scene.tx_array = PlanarArray(num_rows=1,
                             num_cols=1,
                             vertical_spacing=0.5,
                             horizontal_spacing=0.5,
                             pattern="iso",
                             polarization="V")

scene.rx_array = scene.tx_array
scene.add(Transmitter(name="tx",
                      position=[-33,11,32],
                      orientation=[0,0,0]))

cm = radio_map_solver(scene, cell_size=(1, 1), samples_per_tx=10**7,
                      los=True,
                      specular_reflection=True,
                      refraction=False, # Deactivate refraction
                      diffraction=False) # Deactivate diffraction
cm_diff = radio_map_solver(scene, cell_size=(1, 1), samples_per_tx=10**7,
                          los=True,
                          specular_reflection=True,
                          refraction=False, # Deactivate refraction
                          diffraction=True) # Activate diffraction
scene.render(camera=my_cam, radio_map=cm, rm_show_color_bar=True);
scene.render(camera=my_cam, radio_map=cm_diff, rm_show_color_bar=True);


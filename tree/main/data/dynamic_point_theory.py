"""
dynamic_point_theory.py
Generate figures and datasets for:
"The Nature and Interior of the Mathematical Point,
 and the Transition from Point to Consciousness"
Author: Xiaohui Li
"""

import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

# --------------------------------------------------------------------------- #
# Physical constants
# --------------------------------------------------------------------------- #
hbar = 1.054571817e-34  # J*s
G = 6.67430e-11          # m^3 kg^-1 s^-2
c = 2.99792458e8         # m/s
l_P = np.sqrt(hbar * G / c**3)  # Planck length ~ 1.616e-35 m
print(f"Planck length l_P = {l_P:.3e} m")

OUT_DIR = "output"
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(os.path.join(OUT_DIR, "data"), exist_ok=True)

np.random.seed(42)

# --------------------------------------------------------------------------- #
# Figure 1: Internal Hilbert-space dimension vs. spatial extension
# --------------------------------------------------------------------------- #
delta = np.logspace(-2, 2, 1000) * l_P  # from 0.01 l_P to 100 l_P
D0 = 1.0
alpha = 2.0

D_uncut = D0 * (l_P / delta)**alpha
D_cut = np.where(delta >= l_P, D0 * (l_P / delta)**alpha, D0)

fig, ax = plt.subplots(figsize=(6, 4))
ax.loglog(delta / l_P, D_uncut, label="Uncutoff model", color="#1f77b4")
ax.loglog(delta / l_P, D_cut, label="Planck-cutoff model", color="#ff7f0e")
ax.axvline(1.0, color="gray", linestyle="--", alpha=0.7)
ax.set_xlabel(r"$\delta / l_P$", fontsize=12)
ax.set_ylabel(r"$D(\delta)$", fontsize=12)
ax.set_title("Internal Hilbert-space dimension of a dynamic point", fontsize=13)
ax.legend()
ax.grid(True, which="both", ls=":", alpha=0.5)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "figure1_dimension_scaling.pdf"))
plt.savefig(os.path.join(OUT_DIR, "figure1_dimension_scaling.png"), dpi=300)
plt.close()

df1 = pd.DataFrame({"delta_over_lP": delta / l_P,
                    "D_uncut": D_uncut,
                    "D_cut": D_cut})
df1.to_csv(os.path.join(OUT_DIR, "data", "S1_dimension_scaling.csv"), index=False)

# --------------------------------------------------------------------------- #
# Figure 2: Concept network of a point
# --------------------------------------------------------------------------- #
G_net = nx.Graph()
nodes = ["Language", "Cosmology", "Consciousness", "Physics", "Life", "Intelligence"]
G_net.add_nodes_from(nodes)

edges = [
    ("Language", "Consciousness", 0.85),
    ("Consciousness", "Physics", 0.75),
    ("Physics", "Cosmology", 0.90),
    ("Cosmology", "Life", 0.60),
    ("Life", "Intelligence", 0.80),
    ("Intelligence", "Language", 0.70),
    ("Consciousness", "Life", 0.65),
    ("Physics", "Intelligence", 0.55),
]
G_net.add_weighted_edges_from(edges)

pos = nx.spring_layout(G_net, seed=42, k=1.2)
weights = [d["weight"] for (_, _, d) in G_net.edges(data=True)]

fig, ax = plt.subplots(figsize=(6, 6))
nx.draw_networkx_nodes(G_net, pos, node_color="#66c2a5", node_size=2500, ax=ax)
nx.draw_networkx_labels(G_net, pos, font_size=9, ax=ax)
nx.draw_networkx_edges(G_net, pos, width=[8*w for w in weights],
                       edge_color="#fc8d62", alpha=0.7, ax=ax)
ax.set_title("Concept network stabilizing the mathematical point", fontsize=13)
ax.axis("off")
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "figure2_concept_network.pdf"))
plt.savefig(os.path.join(OUT_DIR, "figure2_concept_network.png"), dpi=300)
plt.close()

adj = nx.to_pandas_adjacency(G_net)
adj_dict = {n: dict(G_net[n]) for n in G_net.nodes()}
with open(os.path.join(OUT_DIR, "data", "S3_concept_network.json"), "w") as f:
    json.dump(adj_dict, f, indent=2)

# --------------------------------------------------------------------------- #
# Figure 3: Simulated gravitational waveform with DPT echoes
# --------------------------------------------------------------------------- #
fs = 4096
t = np.linspace(0, 2.0, 2 * fs)

# Inspiral-merger-ringdown approximation
def waveform(t, f0=35, f1=250, t_merge=1.0, gamma=8.0):
    chirp = np.sin(2*np.pi*(f0 + (f1-f0)*np.exp((t - t_merge)*gamma) /
                             (1 + np.exp((t - t_merge)*gamma))) * t)
    envelope = np.exp(-((t - t_merge)**2) / 0.005)
    return chirp * envelope

signal = waveform(t)
# Echoes after merger
echo_times = [1.05, 1.15, 1.28, 1.44]
echo_amp = 0.12
for et in echo_times:
    echo = echo_amp * np.sin(2*np.pi*180*(t - et)) * \
           np.exp(-((t - et)**2)/0.003) * (t > et)
    signal += echo

signal += 0.02 * np.random.randn(len(t))

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(t, signal, color="#2c3e50", lw=0.8)
for et in echo_times:
    ax.axvline(et, color="#e74c3c", linestyle="--", alpha=0.6, lw=1)
ax.set_xlabel("Time [s]", fontsize=12)
ax.set_ylabel("Strain $h(t)$", fontsize=12)
ax.set_title("Simulated BBH waveform with DPT-predicted echoes", fontsize=13)
ax.set_xlim(0.5, 1.8)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "figure3_gravitational_echoes.pdf"))
plt.savefig(os.path.join(OUT_DIR, "figure3_gravitational_echoes.png"), dpi=300)
plt.close()

df2 = pd.DataFrame({"time_s": t, "strain": signal})
df2.to_csv(os.path.join(OUT_DIR, "data", "S2_echo_template.csv"), index=False)

print("All figures and datasets generated in:", OUT_DIR)

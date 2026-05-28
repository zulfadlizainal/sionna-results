# About

This repository is made for the purpose of <mark>testing</mark> [Sionna](https://nvlabs.github.io/sionna/) by [NVIDIA Labs](https://research.nvidia.com/research-labs).

This repository contains a <mark>list of results generated from the Sionna simulation toolkit</mark> based on controlled test case and experiments, made in order to verify the effects of electromagnetic wave propagation in wireless communication through simulations. It <mark>provides direct, easy-to-grasp results, along with the code</mark> used to generate them, so users can:

1. Easily grasp the concept of electromagnetic wave propagation behavior in practice  
2. Easily deploy a propagation simulation with minimal coding and understanding of complex API documentation
3. Easily confirm research and practical observations with the simulation results

For more detailed information, go to Sionna’s primary [resources](https://nvlabs.github.io/sionna/).

## Experiments

List of experiments published in the repository so far:

| Test ID | Test Name | Status | Date Published | Sionna Version | Result |
|----|----|----|----|----|----|
| Blockage-001 | Effect of Signal Attenuation Across Different Blocking Materials | ✅ Done | 2026-05-28 | v2.0.1 | [View](https://github.com/zulfadlizainal/sionna-results/blob/main/docs/docs/Blockage/Blockage-001.md) |

## Requirement

To regenerate the results from experiments in this repository, users need to configure at least the packages below as requirements:

| No | Tools | Download | Purpose |
|----|----|----|----|
| 1 | Sionna 2.0+ | [Get](https://github.com/NVlabs/sionna) | Core simulation toolkit for modeling and evaluating wireless communication systems |
| 2 | Python 3.12+ | [Get](https://www.python.org/) | Primary programming language required to run simulations and scripts |
| 3 | PyTorch 2.9+ | [Get](https://pytorch.org/get-started/locally/) | Backend framework for tensor computation and machine learning support |
| 4 | Blender LTS | [Get](https://www.blender.org/download/lts/) | 3D environment for scene creation and visualization of propagation models |
| 5 | Blender OSM Add On | [Get](https://github.com/solido3d/blender-osm) | Imports real-world OpenStreetMap data into Blender for realistic city modeling |
| 6 | Blender Mitsuba Add On | [Get](https://github.com/mitsuba-renderer/mitsuba-blender) | Enables physically-based rendering for accurate electromagnetic wave visualization |
| 7 | Optional: Jupyter Notebook | [Get](https://jupyter.org/install) | Interactive environment for running experiments and analyzing results |
| 8 | Optional: 3D Model of Tokyo | [Get](https://info.tokyo-digitaltwin.metro.tokyo.lg.jp/3dmodel/) | Provides realistic urban 3D data for high-fidelity simulation scenarios |

## Citation

If you use the results from this repository, please cite it as:

```bibtex
@misc{sionna_results,
  title        = {Sionna Results: Simulation Outputs Generated Using the Sionna Toolkit},
  author       = {Zulfadli Zainal},
  year         = {2026},
  howpublished = {\url{https://github.com/zulfadlizainal/sionna-results}},
  note         = {A curated collection of simulation results generated using the NVIDIA Sionna open source library}
}
```

If you use the software in any way, please cite the author of the software:

```bibtex
@software{sionna,
 title = {Sionna},
 author = {Hoydis, Jakob and Cammerer, Sebastian and {Ait Aoudia}, Fayçal and
 Nimier-David, Merlin and Maggi, Lorenzo and Marcus, Guillermo and Vem, Avinash and Keller,
 Alexander},
 note = {https://nvlabs.github.io/sionna/},
 year = {2022},
 version = {2.0.1}
}
```

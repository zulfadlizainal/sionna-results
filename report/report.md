<!-- repo: github.com/zulfadlizainal/sionna-results -->

<div class="paper-title">Title of Your Technical Paper</div>

<div class="paper-authors">Zulfadli Zainal<sup>1</sup>, Collaborator Name<sup>2</sup></div>
<div class="paper-affiliation"><sup>1</sup>Your Institution &nbsp;·&nbsp; <sup>2</sup>Collaborator Institution</div>
<div class="paper-date">May 2026 &nbsp;·&nbsp; Preprint v1.0</div>

<hr class="title-rule">

<div class="abstract-box">
<div class="abstract-label">Abstract</div>

Write your abstract here. Summarize the problem statement, experimental methodology,
key findings, and significance of results in 150–250 words. Avoid unexplained acronyms
and citations in the abstract.

</div>

<div class="keywords"><strong>Keywords —</strong> Sionna, ray tracing, diffraction, wireless channel, 5G simulation</div>

<hr class="section-rule">

## Introduction

Provide the background and motivation for this work. Explain the problem domain and
what gap this study addresses [1].

### Background

Accurate propagation modeling is a cornerstone of modern wireless network design.

### Objectives

The specific objectives of this study are:

- Quantify diffraction loss as a function of propagation distance.
- Characterize the influence of edge geometry on received signal level.
- Validate simulation results against published empirical measurements.

## Methodology

All experiments were conducted using Sionna's ray tracing module.

### Simulation Environment

| Parameter | Value | Notes |
|-----------|-------|-------|
| Carrier frequency | 3.5 GHz | n78 band |
| Bandwidth | 20 MHz | — |
| Scenario | Urban macro | 3GPP UMa |
| Tx height | 25 m | Rooftop |
| Rx height | 1.5 m | Pedestrian |
| Simulation runs | 50 | Per configuration |

### Diffraction Model

The diffraction model follows the Uniform Theory of Diffraction (UTD).

<div class="callout">
<div class="callout-label">Note</div>
All results were averaged over 50 independent runs at 95% confidence level.
</div>

## Results

### EXP-001 — Diffraction Loss vs Distance

![Figure 1 — Path loss vs distance plot](assets/exp001_plot.png)
*Figure 1 — Path loss increases monotonically with distance from the transmitter.*

| Distance (m) | Mean Path Loss (dB) | Std Dev (dB) |
|--------------|---------------------|--------------|
| 100 | 82.4 | 1.2 |
| 200 | 91.7 | 1.8 |
| 500 | 103.2 | 2.4 |
| 1000 | 114.5 | 3.1 |

### EXP-002 — Effect of Edge Geometry

![Figure 2 — Edge geometry comparison](assets/exp002_plot.png)
*Figure 2 — Rounded edges consistently produce lower path loss than knife-edge models.*

| Edge Type | Path Loss (dB) | Delta (dB) |
|-----------|----------------|------------|
| Knife edge | 103.2 | — |
| Rounded (r = 0.5 m) | 98.7 | −4.5 |
| Rounded (r = 1.0 m) | 97.3 | −5.9 |

<div class="callout tip">
<div class="callout-label">Observation</div>
Rounded edges reduce path loss by up to 6 dB vs knife-edge models.
</div>

## Discussion

The observed path loss exponent of 3.8 is consistent with 3GPP UMa reference measurements,
validating the fidelity of the simulation model.

<div class="callout warning">
<div class="callout-label">Limitation</div>
Results are specific to 3.5 GHz. Extrapolation to mmWave should be done with caution.
</div>

## Conclusion

Key findings from this study:

- Diffraction loss increases at approximately 3.2 dB per decade beyond the edge.
- Rounded edges reduce path loss by up to 6 dB vs knife-edge models.
- Results are consistent with 3GPP UMa reference measurements.

<div class="references">

## References

<ol class="ref-list">
<li>3GPP TR 38.901, "Study on channel model for frequencies from 0.5 to 100 GHz," 2017.</li>
<li>J. Hoydis et al., "Sionna: An open-source library for next-generation physical layer research," arXiv:2203.11854, 2022.</li>
<li>C. A. Balanis, <em>Advanced Engineering Electromagnetics</em>, 2nd ed. Wiley, 2012.</li>
</ol>

</div>
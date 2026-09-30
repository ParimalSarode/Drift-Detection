import numpy as np


def calculate_psi(reference, production, bins=10):

    reference = np.asarray(reference)
    production = np.asarray(production)

    breakpoints = np.percentile(
        reference,
        np.linspace(0, 100, bins + 1)
    )

    breakpoints = np.unique(breakpoints)

    if len(breakpoints) < 3:
        return 0.0

    reference_counts, _ = np.histogram(
        reference,
        bins=breakpoints
    )

    production_counts, _ = np.histogram(
        production,
        bins=breakpoints
    )

    reference_percent = reference_counts / len(reference)
    production_percent = production_counts / len(production)

    reference_percent = np.maximum(
        reference_percent,
        0.0001
    )

    production_percent = np.maximum(
        production_percent,
        0.0001
    )

    psi = np.sum(
        (production_percent - reference_percent)
        * np.log(production_percent / reference_percent)
    )

    return float(psi)
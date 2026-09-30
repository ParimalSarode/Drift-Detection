from scipy.stats import ks_2samp


def run_ks_test(reference, production, threshold=0.05):
    statistic, p_value = ks_2samp(reference, production)

    return {
        "statistic": statistic,
        "p_value": p_value,
        "drift": p_value < threshold
    }
from .ks_test import run_ks_test
from .psi import calculate_psi


def check_feature_drift(reference, production, feature):

    ks_result = run_ks_test(
        reference,
        production
    )

    psi_score = calculate_psi(
        reference,
        production
    )

    return {
        "feature": feature,
        "ks_statistic": round(
            ks_result["statistic"], 4
        ),
        "p_value": round(
            ks_result["p_value"], 6
        ),
        "ks_drift": ks_result["drift"],
        "psi": round(psi_score, 4)
    }


def check_all_features(
    reference_df,
    production_df,
    features
):

    results = []

    for feature in features:

        result = check_feature_drift(
            reference_df[feature],
            production_df[feature],
            feature
        )

        results.append(result)

    return results
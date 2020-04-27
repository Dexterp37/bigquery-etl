#!/usr/bin/env python3
import os


APP_CHANNEL_TUPLES = [
    ("org_mozilla_fenix",           "Firefox Preview",  "beta"),
    ("org_mozilla_fenix_nightly",   "Firefox Preview",  "nightly"),
    ("org_mozilla_fennec_aurora",   "Fenix",            "nightly"),
    ("org_mozilla_firefox_beta",    "Fenix",            "beta"),
    ("org_mozilla_firefox",         "Fenix",            "release"),
]


def create_cte(name, query, first=False, last=False):
    return f"""{"WITH " if first else ""}{name} AS (
    {query}
){"," if not last else ""}"""


def main():
    base_dir = os.path.dirname(__file__)

    # baseline is only required because older clients don't send locale in metrics
    # this is only a problem for firefox preview for <10% of clients
    with open(os.path.join(base_dir, "fenix_baseline.template.sql")) as f:
        baseline_query_template = f.read()

    baseline_queries = [
        baseline_query_template.format(
            namespace=app_channel[0]
        ) for app_channel in APP_CHANNEL_TUPLES
    ]
    print(create_cte("fenix_client_locale", "\nUNION ALL\n".join(baseline_queries), first=True))

    with open(os.path.join(base_dir, "fenix_metrics.template.sql")) as f:
        metrics_query_template = f.read()

    metrics_queries = [
        metrics_query_template.format(
            namespace=app_channel[0], app_name=app_channel[1], channel=app_channel[2]
        ) for app_channel in APP_CHANNEL_TUPLES
    ]
    print(create_cte("fenix_metrics", "\nUNION ALL\n".join(metrics_queries), last=True))


if __name__ == "__main__":
    main()

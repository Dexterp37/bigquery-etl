#!/usr/bin/env python3
import os


APP_CHANNEL_TUPLES = [
    ('org_mozilla_fenix_stable',           'Firefox Preview',  'beta'),
    ('org_mozilla_fenix_nightly_stable',   'Firefox Preview',  'nightly'),
    ('org_mozilla_fennec_aurora_stable',   'Fenix',            'nightly'),
    ('org_mozilla_firefox_beta_stable',    'Fenix',            'beta'),
    ('org_mozilla_firefox_stable',         'Fenix',            'release'),
]


def main():
    base_dir = os.path.dirname(__file__)

    with open(os.path.join(base_dir, 'fenix_metrics.template.sql')) as f:
        metrics_query_template = f.read()

    metrics_queries = [
        metrics_query_template.format(
            namespace=app_channel[0], app_name=app_channel[1], channel=app_channel[2]
        ) for app_channel in APP_CHANNEL_TUPLES
    ]

    print('\nUNION ALL\n'.join(metrics_queries))


if __name__ == '__main__':
    main()

import os
import meerkat.probe

config = {
    # paths relative from this config file
    "pidfile": os.path.realpath(os.path.join(os.path.dirname(__file__),
                                '..', 'var', 'meerkat.pid')),
    "logfile": os.path.realpath(os.path.join(os.path.dirname(__file__),
                                '..', 'log', 'meerkat.log')),
    "datafile": os.path.realpath(os.path.join(os.path.dirname(__file__),
                                 '..', 'data', 'meerkat.db')),
    "probe_path": os.path.realpath(os.path.join(os.path.dirname(__file__),
                                 '..', 'meerkat', 'probes')),

    "probes": [
        "meerkat.probe.bluetooth": {
            "command": ["bluetooth"],
            "type": meerkat.probe.PROBE_DURATION,
            "duration": 30,
            "delay": 60,
            "data_type": meerkat.probe.TYPE_JSON,
            "filters": [
                "meerkat.filter.drop_unchanged"
            ]
        },
        "meerkat.probe.wifi_scan": {
            "type": meerkat.probe.PROBE_PERIODIC,
            "delay": 30,
            "data_type": meerkat.probe.TYPE_JSON,
            "filters": [
                "meerkat.filter.drop_unchanged"
            ]
        },
        "meerkat.probe.wifi_fake_ap": {
            "type": meerkat.probe.PROBE_CONTINUOUS,
            "data_type": meerkat.probe.TYPE_JSON
        },
        "meerkat.probe.wifi_packet_sniff": {
            "type": meerkat.probe.PROBE_DURATION,
            "duration": 30,
            "delay": 30,
            "data_type": meerkat.probe.TYPE_JSON,
            "filters": [
                "meerkat.filter.packet_filter"
            ]
        },
        "meerkat.probe.photo": {
            "type": meerkat.probe.PROBE_PERIODIC,
            "delay": 30,
            "data_type": meerkat.probe.TYPE_JSON, # this matches the output of all filters
            "filters": [
                "meerkat.filter.opencv_pedestrian_count"
            ]
        }
    ]
}


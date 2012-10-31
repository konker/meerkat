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
                                 '..', 'meerkat', 'probe')),

    "probes": {
        "meerkat.probe.dummy_data": {
            "command": ["dummy_data.sh", "128"],
            "type": meerkat.probe.TYPE_PERIODIC,
            "delay": 10,
            "data_type": meerkat.probe.DATA_TYPE_DATA
        },
        "meerkat.probe.bluetooth": {
            "command": ["bluetooth_scan.py"],
            "type": meerkat.probe.TYPE_DURATION,
            "duration": 30,
            "delay": 60,
            "data_type": meerkat.probe.DATA_TYPE_JSON,
            "filters": [
                "meerkat.filters.dummy.Uppercase"
            ]
        }
    }
}

'''
        "meerkat.probe.wifi_scan": {
            "type": meerkat.probe.TYPE_PERIODIC,
            "delay": 30,
            "data_type": meerkat.probe.DATA_TYPE_JSON,
            "filters": [
                "meerkat.filters.drop_unchanged"
            ]
        },
        "meerkat.probe.wifi_fake_ap": {
            "type": meerkat.probe.TYPE_CONTINUOUS,
            "data_type": meerkat.probe.DATA_TYPE_JSON
        },
        "meerkat.probe.wifi_packet_sniff": {
            "type": meerkat.probe.TYPE_DURATION,
            "duration": 30,
            "delay": 30,
            "data_type": meerkat.probe.DATA_TYPE_JSON,
            "filters": [
                "meerkat.filters.packet_filter"
            ]
        },
        "meerkat.probe.photo": {
            "type": meerkat.probe.TYPE_PERIODIC,
            "delay": 30,
            "data_type": meerkat.probe.DATA_TYPE_JSON, # this matches the output of all filters
            "filters": [
                "meerkat.filters.opencv_pedestrian_count"
            ]
        }
'''


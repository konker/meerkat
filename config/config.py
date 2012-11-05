import os
import meerkat.probe.probe as probe

config = {
    # paths relative from this config file
    "pidfile": os.path.realpath(os.path.join(os.path.dirname(__file__),
                                '..', 'var', 'meerkat.pid')),
    "logfile": os.path.realpath(os.path.join(os.path.dirname(__file__),
                                '..', 'log', 'meerkat.log')),
    "datafile": os.path.realpath(os.path.join(os.path.dirname(__file__),
                                 '..', 'data', 'meerkat.db')),
    "probe_path": os.path.realpath(os.path.join(os.path.dirname(__file__),
                                 '..', 'meerkat', 'probe', 'bin')),

    "http_host": "0.0.0.0",
    "http_port": 80,
    "ssl_cert": None,
    "ssl_key": None,

    "probes": {
        "meerkat.probe.tick_sleeper": {
            "command": ["tick_sleeper.sh", "20"],
            "type": probe.TYPE_DURATION,
            "duration": 6,
            "interval": 14,
            "data_type": probe.DATA_TYPE_DATA
        },
        "meerkat.probe.camera_photo": {
            "command": ["camera_photo.py", "meerkat.probe.camera_photo"],
            "type": probe.TYPE_PERIODIC,
            "interval": 20,
            "data_type": probe.DATA_TYPE_DATA,
            "filters": [
                "meerkat.filters.cv_filters.CreateLatestLink"
            ],
            "error_filters": [
                "meerkat.filters.cv_filters.RemoveErrors"
            ]
        },
        "meerkat.probe.dummy_data": {
            "command": ["dummy_data.sh", "128"],
            "type": probe.TYPE_PERIODIC,
            "interval": 10,
            "data_type": probe.DATA_TYPE_DATA
        },
        "meerkat.probe.bluetooth": {
            "command": ["bluetooth_scan.py"],
            "type": probe.TYPE_DURATION,
            "duration": 60,
            "interval": 30,
            "data_type": probe.DATA_TYPE_JSON,
            "filters": [
                "meerkat.filters.dummy.Uppercase"
            ]
        }
    }
}

'''
        "meerkat.probe.wifi_scan": {
            "type": probe.TYPE_PERIODIC,
            "interval": 30,
            "data_type": probe.DATA_TYPE_JSON,
            "filters": [
                "meerkat.filters.drop_unchanged"
            ]
        },
        "meerkat.probe.wifi_fake_ap": {
            "type": probe.TYPE_CONTINUOUS,
            "data_type": meerkat.probe.DATA_TYPE_JSON
        },
        "meerkat.probe.wifi_packet_sniff": {
            "type": probe.TYPE_DURATION,
            "duration": 30,
            "interval": 30,
            "data_type": probe.DATA_TYPE_JSON,
            "filters": [
                "meerkat.filters.packet_filter"
            ]
        },
        "meerkat.probe.photo": {
            "type": probe.TYPE_PERIODIC,
            "interval": 30,
            "data_type": probe.DATA_TYPE_JSON, # this matches the output of all filters
            "filters": [
                "meerkat.filters.opencv_pedestrian_count"
            ]
        }
'''


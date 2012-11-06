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
    "imagepath": os.path.realpath(os.path.join(os.path.dirname(__file__),
                                 '..', 'meerkat', 'http', 'static','img')),
    "probepath": os.path.realpath(os.path.join(os.path.dirname(__file__),
                                 '..', 'meerkat', 'probe', 'bin')),

    "http_host": "0.0.0.0",
    "http_port": 80,

    #[TODO]
    "ssl_cert": None,
    "ssl_key": None,

    "has_camera": True,

    "probes": [
        {
            "id": "meerkat.probe.bluetooth",
            "command": ["bluetooth_scan.py"],
            "type": probe.TYPE_PERIODIC,
            "interval": 10,
            "duration": -1,
            "data_type": probe.DATA_TYPE_JSON,
            "auto_start": False,
            "filters": [
                "meerkat.filters.dummy.Uppercase"
            ]
        },
        {
            "id": "meerkat.probe.camera_photo",
            "command": ["camera_photo.py", "meerkat.probe.camera_photo"],
            "type": probe.TYPE_PERIODIC,
            "interval": 20,
            "data_type": probe.DATA_TYPE_JSON,
            "auto_start": False,
            "filters": [
                "meerkat.filters.cv_filters.CreateLatestLink"
            ],
            "error_filters": [
                "meerkat.filters.cv_filters.RemoveErrors"
            ]
        },
        {
            "id": "meerkat.probe.wifi_client_scan",
            "command": ["wifi_client_scan.py"],
            "type": probe.TYPE_DURATION,
            "interval": 10,
            "duration": 30,
            "data_type": probe.DATA_TYPE_TEXT,
            "auto_start": False,
            "filters": [
            ],
            "error_filters": [
                "meerkat.filters.wifi_filters.RemoveWarnings"
            ]
        },
        {
            "id": "meerkat.probe.json_tick_sleeper",
            "command": ["json_tick_sleeper.sh", "20"],
            "type": probe.TYPE_DURATION,
            "duration": 8,
            "interval": 4,
            "data_type": probe.DATA_TYPE_JSON,
            "auto_start": False
        },
        {
            "id": "meerkat.probe.text_tick_sleeper",
            "command": ["text_tick_sleeper.sh", "20"],
            "type": probe.TYPE_DURATION,
            "duration": 8,
            "interval": 5,
            "data_type": probe.DATA_TYPE_TEXT,
            "auto_start": False
        },
        {
            "id": "meerkat.probe.dummy_data",
            "command": ["dummy_data.sh", "128"],
            "type": probe.TYPE_PERIODIC,
            "interval": 10,
            "data_type": probe.DATA_TYPE_TEXT,
            "auto_start": False
        }
    ]
}


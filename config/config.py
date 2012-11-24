import os
import meerkat.probes.probe as probe

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
    "probespath": os.path.realpath(os.path.join(os.path.dirname(__file__),
                                 '..', 'meerkat', 'probes', 'bin')),

    "debug": True,

    "http_host": "0.0.0.0",
    "http_port": 8080,

    "mission_control": {
        "url": "http://meerkat.0-9.fi/meerkat/",
        "register_url": "http://meerkat.0-9.fi/meerkat/register.json"
    },
    "heartbeat": {
        "interval": 20,
        "url": "https://localhost/meerkat/heartbeat.json"
    },

    "has_camera": True,

    "probes": []
}
config["probes"].append({
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
})

config["probes"].append({
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
})
'''
config["probes"].append({
    "id": "meerkat.probe.camera_photo_detect_people",
    "command": ["camera_photo_detect_people.py", "meerkat.probe.camera_photo_detect_people"],
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
})
'''
config["probes"].append({
    "id": "meerkat.probe.wifi_client_scan",
    "command": ["wifi_client_scan.py"],
    "type": probe.TYPE_DURATION,
    "interval": 10,
    "duration": 60,
    "data_type": probe.DATA_TYPE_JSON,
    "auto_start": False,
    "filters": [
    ],
    "error_filters": [
        "meerkat.filters.wifi_filters.RemoveWarnings"
    ]
})
config["probes"].append({
    "id": "meerkat.probe.heartbeat",
    "command": ["heartbeat.py", config["heartbeat"]["url"]],
    "type": probe.TYPE_PERIODIC,
    "interval": config["heartbeat"]["interval"],
    "duration": -1,
    "data_type": probe.DATA_TYPE_JSON,
    "auto_start": True
})
config["probes"].append({
    "id": "meerkat.probe.json_tick_sleeper",
    "command": ["json_tick_sleeper.sh", "20"],
    "type": probe.TYPE_DURATION,
    "duration": 8,
    "interval": 4,
    "data_type": probe.DATA_TYPE_JSON,
    "dummy": True,
    "auto_start": False
})
config["probes"].append({
    "id": "meerkat.probe.text_tick_sleeper",
    "command": ["text_tick_sleeper.sh", "20"],
    "type": probe.TYPE_DURATION,
    "duration": 8,
    "interval": 5,
    "data_type": probe.DATA_TYPE_TEXT,
    "dummy": True,
    "auto_start": False
})
config["probes"].append({
    "id": "meerkat.probe.dummy_data",
    "command": ["dummy_data.sh", "128"],
    "type": probe.TYPE_PERIODIC,
    "interval": 5,
    "data_type": probe.DATA_TYPE_TEXT,
    "dummy": True,
    "auto_start": False
})


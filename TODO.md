TODO
==============================================================================

- meerkat.probes package holds small stand-alone probe programs
    - each probe writes JSON/binary data(?) to it's stdout
    - can be called from command line
    - each probe can take some standard arguments:
        --duration-secs=n
        - is it the probe's responsibility to manage duration?
            - or should the master program terminate a probe after n secs?
                - what about data in inconsisitent state?


    - do we need a Probe base class?

- probes are configured by config.config
    "global_filters": [
        # or just repeat this in each filters array?
        # XXX: does this imply that all probes have BINARY data_type?
        "meerkat.filter.ecrypt"
    ],
    - "probes": [
        "meerkat.probe.bluetooth": {
            "type": "PROBE_DURATION",
            "duration": 30,
            "delay": 60,
            "data_type": "JSON",
            "filters": [
                "meerkat.filter.drop_unchanged"
            ]
        },
        "meerkat.probe.wifi_scan": {
            "type": "PROBE_PERIODIC",
            "delay": 30,
            "data_type": "JSON",
            "filters": [
                "meerkat.filter.drop_unchanged"
            ]
        },
        "meerkat.probe.wifi_fake_ap": {
            "type": "PROBE_CONTINUOUS",
            "data_type": "JSON"
        },
        "meerkat.probe.wifi_packet_sniff": {
            "type": "PROBE_DURATION",
            "duration": 30,
            "delay": 30,
            "data_type": "JSON",
            "filters": [
                "meerkat.filter.packet_filter"
            ]
        },
        "meerkat.probe.photo": {
            "type": "PROBE_PERIODIC",
            "delay": 30,
            "data_type": "JSON", # this matches the output of all filters
            "filters": [
                "meerkat.filter.opencv_pedestrian_count"
            ]
        }
    ]

- main program loads and manages each probe
    - responsible for scheduling probe calls:
        - DURATION: run for a duration of y secs with a delay for x secs
        - PERIODIC: run every x secs
            - this the same as DURATION, but with a duration of -1 => until exit
        - CONTINUOUS: run and continuously read data
            - e.g. video stream,
            - e.g. fake wifi ap
    - probes are called using multiprocessing with pipes for probe stdout
    - event loop for reading on file descriptors?
        - pyev

- main program provides storage
    - sqlite
    - pos. encrypt

- main program manages filters
    - plugins loaded from meerkat.filters
    - filters provide a filter(data) method
    - config.config configures which filters are applied to which probes
    - could be multiple filters pipelined for one probe
    - e.g. photo try and detect faces, send that meta-data,
      drop actual photo
    - maybe encryption could be a fitler?
        - a way to configure 'global' filters that automatically apply
          to all probes?
    - do we need a Filter base class?

- proposed probes:
    - wifi ap scan
    - wifi packet scan
    - fake wifi ap
    - bluetooth device scan
    - periodic photo
        - video stream => very small delay (?)

- proposed filters:
    - encrytion
    - packet sniff grep filter, e.g. tcp port 80, get host
    - opencv based "pedestrian detect" filter
    - drop if unchanged filter (?)

- http ui:
    - bottle
        - or is this better done in nodejs?
            - can we have the access that we need across py/nodejs?
    - websockets possibly?
        - https://github.com/zeekay/bottle-websocket
        - socket.io in nodejs
    - show the latest data
        - latest picture captured
    - timeline ui of some kind?
    - show status
        - probes configured
        - probes currently running
        - filters?
    - start/stop system?

- what about:
    - Motion?

- potential problems:
    - wifi dongle no moitor mode: cannot do packet sniffing
        - pos. re-compile kernel?
    - when wifi dongle is in monitor mode for sniffing
        - cannot do wifi scan?
            - sniffing => wifi scan?
        - cannot do fake AP?
    - usb storage drive draws too much power?
        - use bigger sdhc card?
    - general performance problems
        - use netbook?
    - opencv on arm?
        - seems python-opencv package is available



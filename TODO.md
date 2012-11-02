TODO
==============================================================================

- add pause / unpause
    - stop probes, but not destroy

- move code out of __init__.py modules

- command-line args for daemon
    - logfile
    - debug
    - http host?
    - http port?

- change to tornado?
    - websockets?

- duration timeout -> kill -> doesn't read output?
- continuous -> will io watcher work?

- meerkat.probes package holds small stand-alone probe programs
    - each probe writes JSON/binary data(?) to it's stdout
    - can be called from command line
    - each probe can take some standard arguments:
        --duration-secs=n
        - is it the probe's responsibility to manage duration?
            - or should the master program terminate a probe after n secs?
                - what about data in inconsisitent state?

    - do we need a Probe base class?


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

- potential problems:
    - usb storage drive draws too much power?
        - use bigger sdhc card?
    - general performance problems
        - use netbook?



TODO
==============================================================================

- further tests of opencv on images
    - set up over night?

- have js UI  draw 'detected' rects on to images?
    - how? canvas?
    - raphael?
    - bonsaijs?
    - d3?

- data 'tab' in UI for inspecting the db
- link to download database
    - pos. zipped?

- security:
    - ssl?
        - cherrypy
    - auth
    - encryption

- --no-debug flag in command line?
    - overrides config['debug']

- opencv pedestrian detect filter blocks event loop
    - for ~20s
    - what can we do?
        - "threaded filter"?
            - bit of a mess with getting the data back into the filter chain?
        - add the detect code into the actual probe process?
        - have some kind of file watcher process? 
            -  watches for new files and runs detect?
        - some kind of dependent probe?


- wifi_client_scan blocks/fucks event loop
    - why?
        - because stderr was blocking. see next issue.

- stderr_cb:
    - if blocking, wifi_scan blocks the event loop,
      but others will only get the first line of stack trace?
      Pos. have err_buf like stdout buf and collect stderr before processing?]

- change to cherrypy?
    - bjoern did not work.

- Leave websockets for later
    - !!

- test out opencv
- test out network sniffing
- create wifi client sniffer
- find out more about clock/gps/ntp

- "sessions"
    - another db table:
        id: id
        start: datetime
        end: datetime
        user: user.id (?)
        data_size_start: number
        data_size_end: number

- auto_start flag for probes

- "latest image"
    - have a function to grab a frame from the camera and save as latest.jpg
        - can be called via web

- change to tornado?
    - class based route handlers
    - better ajax support?
    - better auth support
    - websockets?
        - later

- add some kind of auth
    - can be manually controlled

- add warning prompts for toggle buttons
    - LATER
- add error indicators when ajax errors occur
    - LATER

- remove scroll from log?

- add pause / unpause
    - stop probes, but not destroy

- move code out of __init__.py modules

- command-line args for daemon
    - logfile
    - debug
    - http host?
    - http port?

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

SOLVED:
------------------------------------------------------------------------------
- Delay before probes start:
    - something to do with http-thread -> MainThread?
        - try with auto_start to see if the same effect
        - if so, pos. implement queues?
        - or: why can't http server be in main thread?
    - didn't notice this happening before..?

- Master toggle doesn't work at first load:
    - click masterRefresh -> masterToggle works
    - some artefact of moving masterToggle into probes?


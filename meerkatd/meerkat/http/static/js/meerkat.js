
var meerkat = (function($) {
    var URL_PREFX                = '/meerkat',
        PROBES_JSON_URL          = URL_PREFX + '/probes.json',
        MASTER_JSON_URL          = URL_PREFX + '/master.json',
        REGISTER_JSON_URL        = URL_PREFX + '/register.json',
        KICKSTART_JSON_URL       = URL_PREFX + '/kickstart_gps.json',
        CLEANUP_JSON_URL         = URL_PREFX + '/cleanup_gps.json',
        GPS_PROCS_JSON_URL       = URL_PREFX + '/gps_procs.json',
        JOIN_CLICK_WIFI_JSON_URL = URL_PREFX + '/join_click_wifi.json',
        JOIN_CITY_WIFI_JSON_URL  = URL_PREFX + '/join_city_wifi.json',
        CAPTURE_JSON_URL         = URL_PREFX + '/capture.json',
        LOG_JSON_URL             = URL_PREFX + '/log.json';

    return {
        init: function() {
            meerkat.util.init();
            meerkat.master.init();
            meerkat.probes.init();
            meerkat.log.init();
        },

        master: {
            master: null,
            capture_counter: 0,

            init: function() {
                meerkat.master.refresh();
            },
            capture: function() {
                meerkat.util.loading.on();

                $.ajax({
                    url: CAPTURE_JSON_URL,
                    type: 'POST',
                    dataType: 'json',
                    timeout: 20000,
                    error: function(jqXHR, textStatus, errorThrown) {
                        /*[TODO: error handling ]*/
                        meerkat.util.alert.show("Could not execute operation.", errorThrown);
                        meerkat.util.loading.off();
                    },
                    success: function(data, textStatus, jqXHR) {
                        var img = $('#latest-img img');
                        var src = img.attr('src');
                        if (src.indexOf('?') != -1) {
                            src = src.substr(0, src.indexOf('?'));
                        }
                        src = src + '?' + meerkat.master.capture_counter++;
                        img.attr('src', src)
                        meerkat.util.loading.off();
                    }
                });
                return false;
            },
            toggle: function() {
                meerkat.util.loading.on();

                var command = 'ON';
                if (meerkat.master.master.all_on) {
                    command = 'OFF';
                }

                $.ajax({
                    url: MASTER_JSON_URL,
                    type: 'POST',
                    data: {'command': command},
                    dataType: 'json',
                    timeout: 20000,
                    error: function(jqXHR, textStatus, errorThrown) {
                        /*[TODO: error handling ]*/
                        meerkat.util.alert.show("Could not execute operation.", errorThrown);
                        meerkat.util.loading.off();
                    },
                    success: function(data, textStatus, jqXHR) {
                        meerkat.master.master = data.body;
                        meerkat.master.renderMaster();

                        meerkat.probes.refresh();
                        meerkat.util.loading.off();
                    }
                });
                return false;
            },
            cleanupGPS: function() {
                meerkat.util.loading.on();
                $.ajax({
                    url: CLEANUP_JSON_URL,
                    type: 'POST',
                    dataType: 'json',
                    timeout: 20000,
                    error: function(jqXHR, textStatus, errorThrown) {
                        /*[TODO: error handling ]*/
                        meerkat.util.alert.show("Could not execute operation.", errorThrown);
                        meerkat.util.loading.off();
                    },
                    success: function(data, textStatus, jqXHR) {
                        if (data.status == "ERROR") {
                            meerkat.util.alert.show("Could not execute operation.", data.body);
                        }
                        meerkat.util.alert.showSuccess(data.status, data.body);
                        meerkat.util.loading.off();
                    }
                });
            },
            getGPSProcs: function() {
                meerkat.util.loading.on();
                $.ajax({
                    url: GPS_PROCS_JSON_URL,
                    type: 'GET',
                    dataType: 'json',
                    timeout: 20000,
                    error: function(jqXHR, textStatus, errorThrown) {
                        /*[TODO: error handling ]*/
                        meerkat.util.alert.show("Could not execute operation.", errorThrown);
                        meerkat.util.loading.off();
                    },
                    success: function(data, textStatus, jqXHR) {
                        if (data.status == "ERROR") {
                            meerkat.util.alert.show("Could not execute operation.", data.body);
                        }
                        meerkat.util.alert.showSuccess(data.status, data.body);
                        meerkat.util.loading.off();
                    }
                });
            },
            joinClickWifi: function() {
                meerkat.util.loading.on();
                $.ajax({
                    url: JOIN_CLICK_WIFI_JSON_URL,
                    type: 'GET',
                    dataType: 'json',
                    timeout: 20000,
                    error: function(jqXHR, textStatus, errorThrown) {
                        /*[TODO: error handling ]*/
                        meerkat.util.alert.show("Could not execute operation.", errorThrown);
                        meerkat.util.loading.off();
                    },
                    success: function(data, textStatus, jqXHR) {
                        if (data.status == "ERROR") {
                            meerkat.util.alert.show("Could not execute operation.", data.body);
                        }
                        meerkat.util.alert.showSuccess(data.status, data.body);
                        meerkat.util.loading.off();
                    }
                });
            },
            joinCityWifi: function() {
                meerkat.util.loading.on();
                $.ajax({
                    url: JOIN_CITY_WIFI_JSON_URL,
                    type: 'GET',
                    dataType: 'json',
                    timeout: 20000,
                    error: function(jqXHR, textStatus, errorThrown) {
                        /*[TODO: error handling ]*/
                        meerkat.util.alert.show("Could not execute operation.", errorThrown);
                        meerkat.util.loading.off();
                    },
                    success: function(data, textStatus, jqXHR) {
                        if (data.status == "ERROR") {
                            meerkat.util.alert.show("Could not execute operation.", data.body);
                        }
                        meerkat.util.alert.showSuccess(data.status, data.body);
                        meerkat.util.loading.off();
                    }
                });
            },
            kickstartGPS: function() {
                meerkat.util.loading.on();
                $.ajax({
                    url: KICKSTART_JSON_URL,
                    type: 'POST',
                    dataType: 'json',
                    timeout: 40000,
                    error: function(jqXHR, textStatus, errorThrown) {
                        /*[TODO: error handling ]*/
                        meerkat.util.alert.show("Could not execute operation.", errorThrown);
                        meerkat.util.loading.off();
                    },
                    success: function(data, textStatus, jqXHR) {
                        if (data.status == "ERROR") {
                            meerkat.util.alert.show("Could not execute operation.", data.body);
                        }
                        meerkat.util.alert.showSuccess(data.status, data.body);
                        meerkat.util.loading.off();
                    }
                });
            },
            missionControlRegister: function() {
                meerkat.util.loading.on();
                $.ajax({
                    url: REGISTER_JSON_URL,
                    type: 'POST',
                    dataType: 'json',
                    timeout: 20000,
                    error: function(jqXHR, textStatus, errorThrown) {
                        /*[TODO: error handling ]*/
                        meerkat.util.alert.show("Could not execute operation.", errorThrown);
                        meerkat.util.loading.off();
                    },
                    success: function(data, textStatus, jqXHR) {
                        if (data.status == "ERROR") {
                            meerkat.util.alert.show("Could not execute operation.", data.body);
                        }
                        console.log(data);
                        meerkat.util.alert.showSuccess(data.status, data.body);
                        meerkat.util.loading.off();
                    }
                });
            },
            refresh: function() {
                meerkat.util.loading.on();

                /* fetch JSON data from the server */
                $.ajax({
                    url: MASTER_JSON_URL,
                    dataType: 'json',
                    timeout: 20000,
                    error: function(jqXHR, textStatus, errorThrown) {
                        /*[TODO: error handling ]*/
                        meerkat.util.alert.show("Could not load master information.", errorThrown);
                        meerkat.util.loading.off();
                    },
                    success: function(data, textStatus, jqXHR) {
                        meerkat.master.master = data.body;
                        meerkat.master.renderMaster();
                        meerkat.util.loading.off();
                    }
                });
                return false;
            },
            renderMaster: function() {
                /* extra formatting */
                meerkat.master.master.uptime_secs =
                    meerkat.util.format_secs(meerkat.master.master.uptime_secs);
                meerkat.master.master.sys_temperature =
                    meerkat.util.format_temp(meerkat.master.master.sys_temperature);
                meerkat.master.master.gpu_temperature =
                    meerkat.util.format_temp(meerkat.master.master.gpu_temperature);
                meerkat.master.master.data_size_kb =
                    meerkat.util.format_kb(meerkat.master.master.data_size_kb);
                meerkat.master.master.image_data_size_kb =
                    meerkat.util.format_kb(meerkat.master.master.image_data_size_kb);
                meerkat.master.master.free_space_b =
                    meerkat.util.format_b(meerkat.master.master.free_space_b);
                meerkat.master.master.available_memory_kb =
                    meerkat.util.format_kb(meerkat.master.master.available_memory_kb);
                meerkat.master.master.free_memory_kb =
                    meerkat.util.format_kb(meerkat.master.master.free_memory_kb);
                meerkat.master.master.location =
                    meerkat.util.format_location(meerkat.master.master.location);

                /* render the data */
                $('#master').render(meerkat.master.master, meerkat.master.directives.main);

                /* event handlers */
                $('#missionControlRegister')
                    .unbind('click')
                    .bind('click', meerkat.master.missionControlRegister);

                $('#kickstartGPS')
                    .unbind('click')
                    .bind('click', meerkat.master.kickstartGPS);

                $('#getGPSProcs')
                    .unbind('click')
                    .bind('click', meerkat.master.getGPSProcs);

                $('#joinClickWifi')
                    .unbind('click')
                    .bind('click', meerkat.master.joinClickWifi);

                $('#joinCityWifi')
                    .unbind('click')
                    .bind('click', meerkat.master.joinCityWifi);

                $('#cleanupGPS')
                    .unbind('click')
                    .bind('click', meerkat.master.cleanupGPS);

                $('#masterRefresh')
                    .unbind('click')
                    .bind('click', meerkat.master.refresh);

                if (meerkat.master.master.has_camera) {
                    $('#masterCapture')
                        .unbind('click')
                        .bind('click', meerkat.master.capture)
                        .show();
                    $('#img-holder').show();
                }
                else {
                    $('#masterCapture').hide();
                    $('#img-holder').hide();
                }

                /* visual aids */
                if (meerkat.master.master.all_on) {
                    $('#masterToggle')
                        .removeClass('btn-success')
                        .addClass('btn-danger')
                        .find('.lbl')
                        .text('Master OFF');
                    $('#master dl')
                        .find('dd.status')
                        .removeClass('text-success')
                        .addClass('text-error');
                }
                else {
                    $('#masterToggle')
                        .removeClass('btn-danger')
                        .addClass('btn-success')
                        .find('.lbl')
                        .text('Master ON');
                    $('#master dl')
                        .find('dd.status')
                        .removeClass('text-error')
                        .addClass('text-success');
                }

                /* show it */
                $('#master .section-body').show();
            },
            directives: {
                main: {
                    'dd.status': 'status',
                    'dd.ip_address': 'ip_address',
                    'dd.net_interfaces': 'net_interfaces',
                    'dd.host': 'host',
                    'dd.uptime': 'uptime_secs',
                    'dd.load_average': 'load_average',
                    'dd.sys_temperature': 'sys_temperature',
                    'dd.gpu_temperature': 'gpu_temperature',
                    'dd.data_size': 'data_size_kb',
                    'dd.image_data_size': 'image_data_size_kb',
                    'dd.free_space': 'free_space_b',
                    'dd.available_memory': 'available_memory_kb',
                    'dd.free_memory': 'free_memory_kb',
                    'dd.location': 'location',
                    'dd.mission_control a': 'mission_control_url',
                    'dd.mission_control a@href': 'mission_control_url'
                }
            }
        },
        probes: {
            probes: null,
            image_width: 400,
            image_height: 225,

            init: function() {
                meerkat.probes.loadProbes();
            },
            loadProbes: function() {
                meerkat.util.loading.on();

                $.ajax({
                    url: PROBES_JSON_URL,
                    dataType: 'json',
                    timeout: 20000,
                    error: function(jqXHR, textStatus, errorThrown) {
                        /*[TODO: error handling ]*/
                        meerkat.util.alert.show("Could not load probes data.", errorThrown);
                        meerkat.util.loading.off();
                    },
                    success: function(data, textStatus, jqXHR) {
                        meerkat.probes.probes = data.body.probes;

                        /* render the data */
                        $('#probes').render(data.body, meerkat.probes.directives.main);

                        for (var p in data.body.probes) {
                            meerkat.probes.renderProbe(p);
                        }

                        /* master probe toggle event handler */
                        $('#masterToggle')
                            .unbind('click')
                            .bind('click', meerkat.master.toggle)
                            .show();

                        /* show it */
                        $('#probes .section-body').show();

                        meerkat.util.loading.off();
                    }
                });
                return false;
            },
            toggle: function(e) {
                meerkat.util.loading.on();
                var probe = meerkat.probes.probes[e.data.p];
                var command = 'ON';
                if (probe.status == 'ON') {
                    command = 'OFF';
                }

                $.ajax({
                    url: URL_PREFX + '/' + probe.id + '.json',
                    type: 'POST',
                    data: {'command': command},
                    dataType: 'json',
                    timeout: 20000,
                    error: function(jqXHR, textStatus, errorThrown) {
                        /*[TODO: error handling ]*/
                        meerkat.util.alert.show("Could not execute operation.", errorThrown);
                        meerkat.util.loading.off();
                    },
                    success: function(data, textStatus, jqXHR) {
                        meerkat.probes.probes[e.data.p] = data.body;

                        /* render the data */
                        meerkat.probes.renderProbe(e.data.p);

                        /* show it */
                        $('#probes .section-body').show();

                        /* make sure master is up to date */
                        meerkat.master.refresh();

                        meerkat.util.loading.off();
                    }
                });
                return false;
            },
            refresh: function() {
                for (var p in meerkat.probes.probes) {
                    meerkat.probes.refreshOne(p);
                }
            },
            probeRefreshCB: function(e) {
                meerkat.probes.refreshOne(e.data.p);
                return false;
            },
            refreshOne: function(p) {
                meerkat.util.loading.on();

                $.ajax({
                    url: URL_PREFX + '/' + meerkat.probes.probes[p].id + '.json',
                    dataType: 'json',
                    timeout: 20000,
                    error: function(jqXHR, textStatus, errorThrown) {
                        /*[TODO: error handling ]*/
                        meerkat.util.alert.show("Could not load probe data.", errorThrown);
                        meerkat.util.loading.off();
                    },
                    success: function(data, textStatus, jqXHR) {
                        meerkat.probes.probes[p] = data.body;

                        /* render the data */
                        meerkat.probes.renderProbe(p);

                        /* show it */
                        $('#probes .section-body').show();

                        meerkat.util.loading.off();
                    }
                });
            },
            toggleOpenProbe: function(e) {
                var p = $('#' + e.data.id);
                if (p.hasClass('open')) {
                    p.removeClass('open').addClass('closed');
                    p.find('h3 i')
                        .first()
                        .removeClass('icon-chevron-down')
                        .addClass('icon-chevron-right');
                }
                else {
                    p.removeClass('closed').addClass('open');
                    p.find('h3 i')
                        .first()
                        .removeClass('icon-chevron-right')
                        .addClass('icon-chevron-down');
                }
                return false;
            },
            renderProbe: function(p) {
                var probeHtml = $('#' + meerkat.probes.probes[p].id);

                /* render dummy */
                if (meerkat.probes.probes[p].dummy) {
                    probeHtml.
                        addClass('dummy');
                }

                /* render status */
                probeHtml
                    .find('.probe-body')
                    .render(meerkat.probes.probes[p], meerkat.probes.directives.single);

                /* render data */
                var data = meerkat.probes.probes[p].data;
                for (var r in data) {
                    if (data[r].metadata.timestamp) {
                        data[r].metadata.timestamp =
                            meerkat.util.format_timestamp(data[r].metadata.timestamp);
                    }
                    probeHtml
                        .find('.dbody')
                        .empty()
                        .append(ConvertJsonToTable([data[r].metadata], null,
                                    'table table-bordered', null));

                    if (typeof(data[r].data) == 'object') {
                        /*[FIXME: this should be in some kind of plugin or something?]*/
                        for (var rr in data[r].data) {
                            if (data[r].data[rr] && data[r].data[rr].image_path) {
                                data[r].data[rr].image_path = data[r].data[rr].image_path.substr(data[r].data[rr].image_path.lastIndexOf('/') + 1);
                                data[r].data[rr].image = '<canvas id="holder' + rr + '" width="'+ meerkat.probes.image_width +'" height="'+ meerkat.probes.image_height+'"></canvas>';
                            }
                            if (data[r].data[rr].id) {
                                delete data[r].data[rr].id;
                            }
                            if (data[r].data[rr].detected) {
                                data[r].data[rr].num_detected = data[r].data[rr].detected.length;
                            }
                        }
                        probeHtml
                            .find('.dbody')
                            .append(ConvertJsonToTable(data[r].data, null,
                                            'table table-bordered', null));

                        for (var rr in data[r].data) {
                            if (data[r].data[rr].image_path) {
                                var ctx = $('#holder' + rr).get(0).getContext('2d');
                                var dataimage = new Image();
                                dataimage.onload = function() {
                                    ctx.drawImage(dataimage, 0, 0, meerkat.probes.image_width, meerkat.probes.image_height);
                                    if (data[r].data[rr].num_detected > 0) {
                                        var x_fact = (meerkat.probes.image_width / data[r].data[rr].image_width);
                                        var y_fact = (meerkat.probes.image_height / data[r].data[rr].image_height);

                                        for (var d in data[r].data[rr].detected) {
                                            console.log(data[r].data[rr].detected[d]);
                                            ctx.strokeStyle = 'rgb(255, 0, 0)';
                                            ctx.strokeRect(
                                                data[r].data[rr].detected[d][0][0] * x_fact,
                                                data[r].data[rr].detected[d][0][1] * y_fact,
                                                data[r].data[rr].detected[d][1][0] * x_fact,
                                                data[r].data[rr].detected[d][1][1] * y_fact
                                            );
                                        }
                                    }
                                }
                                dataimage.src = '/static/img/capture/' + data[r].data[rr].image_path;
                            }
                        }
                    }
                    else {
                        probeHtml
                            .find('.dbody')
                            .append('<pre class="scalar">' + data[r].data + '</pre>');
                    }
                }

                /* render filters */
                probeHtml
                    .find('.filters ol')
                    .html('<li></li>')
                    .render(meerkat.probes.probes[p], meerkat.probes.directives.filters);

                /* render error filters */
                probeHtml
                    .find('.error-filters ol')
                    .html('<li></li>')
                    .render(meerkat.probes.probes[p], meerkat.probes.directives.error_filters);

                /* event handlers */
                probeHtml
                    .find('h3')
                    .unbind('click')
                    .bind('click', {id: meerkat.probes.probes[p].id}, meerkat.probes.toggleOpenProbe);

                probeHtml
                    .find('.probeToggle')
                    .unbind('click')
                    .bind('click', {p: p, id: meerkat.probes.probes[p].id}, meerkat.probes.toggle);

                probeHtml
                    .find('.probeRefresh')
                    .unbind('click')
                    .bind('click', {p: p}, meerkat.probes.probeRefreshCB);

                /* visual aids */
                if (meerkat.probes.probes[p].status == 'ON') {
                    probeHtml
                        .find('.probeToggle')
                        .removeClass('btn-danger')
                        .addClass('btn-success')
                        .find('.lbl')
                        .text('Probe ON');

                    probeHtml
                        .find('dd.status')
                        .removeClass('text-error')
                        .addClass('text-success');
                }
                else {
                    probeHtml
                        .find('.probeToggle')
                        .removeClass('btn-success')
                        .addClass('btn-danger')
                        .find('.lbl')
                        .text('Probe OFF');

                    probeHtml
                        .find('dd.status')
                        .removeClass('text-success')
                        .addClass('text-error');
                }

                if (!probeHtml.hasClass('open') && !probeHtml.hasClass('closed')) {
                    probeHtml.addClass('closed');
                }
                /* show it */
                $('#probes .section-body').show();
            },
            directives: {
                main: {
                    '.probe': {
                        'probe<-probes': {
                            '@id': 'probe.id',
                            'h3 span.probe-label': 'probe.label',
                        }
                    }
                },
                single: {
                    'dd.status': 'status',
                    'dd.interval': 'interval',
                    'dd.duration': 'duration',
                    'dd.command': 'command',
                    'dd.last_error pre': 'last_error'
                },
                filters: {
                    'li': {
                        'filter<-filters': {
                            '.': 'filter'
                        }
                    }
                },
                error_filters: {
                    'li': {
                        'filter<-error_filters': {
                            '.': 'filter'
                        }
                    }
                }
            }
        },
        log: {
            init: function() {
                meerkat.log.refresh();
            },
            refresh: function() {
                meerkat.util.loading.on();
                $.ajax({
                    url: LOG_JSON_URL,
                    dataType: 'json',
                    timeout: 20000,
                    error: function(jqXHR, textStatus, errorThrown) {
                        /*[TODO: error handling ]*/
                        meerkat.util.alert.show("Could not load log data.", errorThrown);
                        meerkat.util.loading.off();
                    },
                    success: function(data, textStatus, jqXHR) {
                        data.body.log = data.body.log.join("");
                        $('#log').render(data.body, meerkat.log.directives.main);
                        $('#logRefresh')
                            .unbind('click')
                            .bind('click', meerkat.log.refresh)
                            .show();

                        /* show it */
                        $('#log .section-body').show();

                        meerkat.util.loading.off();
                    }
                });
            },
            directives: {
                main: {
                    'pre': 'log'
                }
            }
        },
        util: {
            NL_RE: /\n/,

            init: function() {
                meerkat.util.alert.init();
            },
            nl2br: function(s) {
                return s.replace(meerkat.util.NL_RE, '<br/>');
            },
            alert: {
                init: function() {
                    //$('#alert').alert();
                    $('#alert .close').bind('click', meerkat.util.alert.hide);
                    $('#alert').hide();
                },
                show: function(body, title) {
                    meerkat.util.alert._set(body, title);
                    $('#alert')
                        .addClass('alert-error');
                    meerkat.util.alert._show();
                },
                showSuccess: function(body, title) {
                    meerkat.util.alert._set(body, title);
                    $('#alert')
                        .addClass('alert-success');
                    meerkat.util.alert._show();
                },
                showInfo: function(body, title) {
                    meerkat.util.alert._set(body, title);
                    $('#alert')
                        .addClass('alert-info');
                    meerkat.util.alert._show();
                },
                _set: function(body, title) {
                    $('#alert')
                        .removeClass('alert-error')
                        .removeClass('alert-success')
                        .removeClass('alert-info')
                    $('#alert')
                        .find('.body').text(title);
                    $('#alert')
                        .find('.title').text(body);
                },
                _show: function() {
                    $('#alert').show();
                },
                hide: function() {
                    //$('#alert').alert('close');
                    $('#alert').hide();
                }
            },
            loading: {
                _stack: 0,
                on: function() {
                    meerkat.util.loading._stack++;
                    meerkat.util.loading._setLoading(true);
                    meerkat.util.alert.hide();
                },
                off: function() {
                    meerkat.util.loading._stack--;
                    if (meerkat.util.loading._stack <= 0) {
                        meerkat.util.loading._setLoading(false);
                    }
                },
                _setLoading: function(on) {
                    if (on) {
                        //$('h1').addClass('loading');
                        $('#loading').show();
                    }
                    else {
                        //$('h1').removeClass('loading');
                        $('#loading').hide();
                        meerkat.util.loading._stack = 0;
                    }
                }
            },
            format_timestamp: function(ts) {
                return meerkat.util.ReadableDateString(new Date(ts)) + "<br/><small>" + ts + "</small>";
            },
            format_location: function(location) {
                console.log(location);
                if (location.latitude == '?' || location.longitude == '?') {
                    return '?, ?';
                }
                return '<a href="http://www.openstreetmap.org/index.html?mlat=' + location.latitude + '&mlon=' + location.longitude + '&zoom=17">' + location.latitude + ', ' + location.longitude + '</a>';
            },
            ReadableDateString: function(d) {
                function pad(n){return n<10 ? '0'+n : n}
                    return d.getFullYear()+'-'
                        + pad(d.getMonth()+1)+'-'
                        + pad(d.getDate())+' '
                        + pad(d.getHours())+':'
                        + pad(d.getMinutes())+':'
                        + pad(d.getSeconds())
            },
            ISODateString: function(d) {
                function pad(n){return n<10 ? '0'+n : n}
                    return d.getUTCFullYear()+'-'
                        + pad(d.getUTCMonth()+1)+'-'
                        + pad(d.getUTCDate())+'T'
                        + pad(d.getUTCHours())+':'
                        + pad(d.getUTCMinutes())+':'
                        + pad(d.getUTCSeconds())+'Z'
            },
            format_secs: function(secs) {
                if (secs > 60) {
                    if (secs > 3600) {
                        return Math.round(secs/3600) + " hrs";
                    }
                    return Math.round(secs/60) + " mins";
                }
                return secs + " secs";
            },
            format_b: function(b) {
                if (b > 1024) {
                    return meerkat.util.format_kb(b/1024);
                }
                return b.toFixed(2) + " B";
            },
            format_kb: function(kb) {
                if (kb > 1024) {
                    return meerkat.util.format_mb(kb/1024);
                }
                return kb.toFixed(2) + " KB";
            },
            format_mb: function(mb) {
                if (mb > 1024) {
                    return (mb/1024).toFixed(2) + " GB";
                }
                return mb.toFixed(2) + " MB";
            },
            format_temp: function(temp) {
                return temp + "&deg;C";
            }
        }
    }
})(jQuery);

$(meerkat.init);

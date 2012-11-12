
var meerkat = (function($) {
    var PROBES_JSON_URL  = '/probes.json',
        MASTER_JSON_URL  = '/master.json',
        CAPTURE_JSON_URL = '/capture.json',
        LOG_JSON_URL     = '/log.json';

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
                if (meerkat.master.master.status == 'ON') {
                    command = 'OFF';
                }

                $.ajax({
                    url: MASTER_JSON_URL,
                    type: 'POST',
                    data: {'command': command},
                    dataType: 'json',
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
            refresh: function() {
                meerkat.util.loading.on();

                /* fetch JSON data from the server */
                $.ajax({
                    url: MASTER_JSON_URL,
                    dataType: 'json',
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
                meerkat.master.master.data_size_kb =
                    meerkat.util.format_kb(meerkat.master.master.data_size_kb);
                meerkat.master.master.free_space_b =
                    meerkat.util.format_b(meerkat.master.master.free_space_b);
                meerkat.master.master.available_memory_kb =
                    meerkat.util.format_kb(meerkat.master.master.available_memory_kb);
                meerkat.master.master.free_memory_kb =
                    meerkat.util.format_kb(meerkat.master.master.free_memory_kb);

                /* render the data */
                $('#master').render(meerkat.master.master, meerkat.master.directives.main);

                /* event handlers */
                $('#masterRefresh')
                    .unbind('click')
                    .bind('click', meerkat.master.refresh);

                if (meerkat.master.master.has_camera) {
                    $('#masterCapture')
                        .unbind('click')
                        .bind('click', meerkat.master.capture)
                        .show();
                    $('#latest-img').show();
                }
                else {
                    $('#masterCapture').hide();
                    $('#latest-img').hide();
                }

                /* visual aids */
                if (meerkat.master.master.status == 'ON') {
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
                else {
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

                /* show it */
                $('#master .section-body').show();
            },
            directives: {
                main: {
                    'dd.status': 'status',
                    'dd.ip_address': 'ip_address',
                    'dd.host': 'host',
                    'dd.uptime': 'uptime_secs',
                    'dd.data_size': 'data_size_kb',
                    'dd.free_space': 'free_space_b',
                    'dd.available_memory': 'available_memory_kb',
                    'dd.free_memory': 'free_memory_kb'
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
                    url: '/' + probe.id + '.json',
                    type: 'POST',
                    data: {'command': command},
                    dataType: 'json',
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
                    url: '/' + meerkat.probes.probes[p].id + '.json',
                    dataType: 'json',
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
                                dataimage.src = 'static/img/' + data[r].data[rr].image_path;
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
            init: function() {
                meerkat.util.alert.init();
            },
            alert: {
                init: function() {
                    //$('#alert').alert();
                    $('#alert .close').bind('click', meerkat.util.alert.hide);
                    $('#alert').hide();
                },
                show: function(body, title) {
                    $('#alert')
                        .find('.body').html(body);
                    $('#alert')
                        .find('.title').html(title);

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
                },
                off: function() {
                    meerkat.util.loading._stack--;
                    if (meerkat.util.loading._stack <= 0) {
                        meerkat.util.loading._setLoading(false);
                    }
                },
                _setLoading: function(on) {
                    if (on) {
                        $('h1').addClass('loading');
                    }
                    else {
                        $('h1').removeClass('loading');
                        meerkat.util.loading._stack = 0;
                    }
                }
            },
            format_timestamp: function(ts) {
                return meerkat.util.ReadableDateString(new Date(ts)) + "<br/><small>" + ts + "</small>";
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
                return kb + " KB";
            },
            format_kb: function(kb) {
                if (kb > 1024) {
                    return meerkat.util.format_mb(kb/1024);
                }
                return kb + " KB";
            },
            format_mb: function(mb) {
                if (mb > 1024) {
                    return mb/1024 + " GB";
                }
                return mb + " MB";
            }
        }
    }
})(jQuery);

$(meerkat.init);

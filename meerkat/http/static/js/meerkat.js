
var meerkat = (function($) {
    var PROBES_JSON_URL = '/probes.json';
    var MASTER_JSON_URL = '/master.json';
    var LOG_JSON_URL = '/log.json';

    return {
        init: function() {
            meerkat.master.init();
            meerkat.probes.init();
            meerkat.log.init();
        },
        master: {
            master: null,

            init: function() {
                meerkat.master.refresh();
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
                        alert(errorThrown);
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
                    error: function(data, textStatus, jqXHR) {
                        /*[TODO: error handling ]*/
                        alert(errorThrown);
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
                meerkat.master.master.data_size_mb =
                    meerkat.util.format_mb(meerkat.master.master.data_size_mb);
                meerkat.master.master.free_space_mb =
                    meerkat.util.format_mb(meerkat.master.master.free_space_mb);

                /* render the data */
                $('#master').render(meerkat.master.master, meerkat.master.directives.main);

                /* event handlers */
                $('#masterToggle')
                    .unbind('click')
                    .bind('click', meerkat.master.toggle);

                $('#masterRefresh')
                    .unbind('click')
                    .bind('click', meerkat.master.refresh);

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
                    'dd.data_size': 'data_size_mb',
                    'dd.free_space': 'free_space_mb',
                }
            }
        },
        probes: {
            probes: null,

            init: function() {
                meerkat.probes.loadProbes();
            },
            loadProbes: function() {
                meerkat.util.loading.on();

                $.ajax({
                    url: PROBES_JSON_URL,
                    dataType: 'json',
                    error: function(data, textStatus, jqXHR) {
                        /*[TODO: error handling ]*/
                        alert(errorThrown);
                        meerkat.util.loading.off();
                    },
                    success: function(data, textStatus, jqXHR) {
                        /*[TODO: error handling ]*/

                        meerkat.probes.probes = data.body.probes;

                        /* render the data */
                        $('#probes').render(data.body, meerkat.probes.directives.main);

                        for (var p in data.body.probes) {
                            meerkat.probes.renderProbe(p);
                        }

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
                        alert(errorThrown);
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
                        alert(errorThrown);
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
                var data = meerkat.probes.probes[p].data.data;
                for (var r in data) {
                    data[r].image_path = '<a href="' + data[r].image_path + '">' + data[r].image_path + '</a>';
                }
                probeHtml
                    .find('.dbody')
                    .html(ConvertJsonToTable(data, null, 'table table-bordered', null));

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
                    'dd.duration': 'duration'
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
                    error: function(data, textStatus, jqXHR) {
                        /*[TODO: error handling ]*/
                        alert(errorThrown);
                        meerkat.util.loading.off();
                    },
                    success: function(data, textStatus, jqXHR) {
                        data.body.log = data.body.log.join("");
                        $('#log').render(data.body, meerkat.log.directives.main);
                        $('#log')
                            .find('.logRefresh')
                            .unbind('click')
                            .bind('click', meerkat.log.refresh);
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
            format_secs: function(secs) {
                /*[TODO]*/
                return secs + " secs";
            },
            format_mb: function(mb) {
                /*[TODO]*/
                return mb + " MB";
            }
        }
    }
})(jQuery);

$(meerkat.init);

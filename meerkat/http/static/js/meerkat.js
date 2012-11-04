
var meerkat = (function($) {
    var PROBES_JSON_URL = 'probes.json';
    var MASTER_JSON_URL = 'master.json';
    var LOG_JSON_URL = 'log.json';

    return {
        init: function() {
            meerkat.master.init();
            meerkat.probes.init();
            meerkat.log.init();
        },
        loading: {
            _stack: 0,
            on: function() {
                meerkat.loading._stack++;
                meerkat.loading._setLoading(true);
            },
            off: function() {
                meerkat.loading._stack--;
                if (meerkat.loading._stack <= 0) {
                    meerkat.loading._setLoading(false);
                }
            },
            _setLoading: function(on) {
                if (on) {
                    $('h1').addClass('loading');
                }
                else {
                    $('h1').removeClass('loading');
                    meerkat.loading._stack = 0;
                }
            }
        },
        master: {
            init: function() {
                meerkat.loading.on();
                meerkat.master.refresh();
            },
            masterToggle: function() {
                /* TODO */
                meerkat.loading.on();
                meerkat.master.refresh();
                return false;
            },
            masterRefresh: function() {
                meerkat.loading.on();
                meerkat.master.refresh();
                return false;
            },
            refresh: function() {
                /* fetch JSON data from the server */
                $.ajax({
                    url: 'master.json',
                    dataType: 'json',
                    error: function(data, textStatus, jqXHR) {
                        /*[TODO: error handling ]*/
                        alert(errorThrown);
                        meerkat.loading.off();
                    },
                    success: function(data, textStatus, jqXHR) {
                        /*[TODO: error handling ]*/
                        /* extra formatting */
                        data.body.uptime_ms =
                            meerkat.util.format_ms(data.body.uptime_ms);
                        data.body.data_size_mb =
                            meerkat.util.format_mb(data.body.data_size_mb);
                        data.body.free_space_mb =
                            meerkat.util.format_mb(data.body.free_space_mb);

                        /* render the data */
                        $('#master').render(data.body, meerkat.master.directives.main);

                        /* event handlers */
                        $('#masterToggle')
                            .unbind('click')
                            .bind('click', meerkat.master.masterToggle);

                        $('#masterRefresh')
                            .unbind('click')
                            .bind('click', meerkat.master.masterRefresh);

                        /* visual aids */
                        if (data.body.status == 'ON') {
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

                        meerkat.loading.off();
                    }
                });
            },
            directives: {
                main: {
                    'dd.status': 'status',
                    'dd.ip_address': 'ip_address',
                    'dd.host': 'host',
                    'dd.uptime': 'uptime_ms',
                    'dd.data_size': 'data_size_mb',
                    'dd.free_space': 'free_space_mb',
                }
            }
        },
        probes: {
            probes: null,

            init: function() {
                meerkat.loading.on();
                meerkat.probes.refresh();
            },
            probeToggle: function(e) {
                /* TODO */
                meerkat.loading.on();
                meerkat.probes.refreshProbe(e.data.p);
                return false;
            },
            probeRefresh: function(e) {
                meerkat.loading.on();
                meerkat.probes.refreshProbe(e.data.p);
                return false;
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
            refresh: function() {
                $.ajax({
                    url: 'probes.json',
                    dataType: 'json',
                    error: function(data, textStatus, jqXHR) {
                        /*[TODO: error handling ]*/
                        alert(errorThrown);
                        meerkat.loading.off();
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

                        meerkat.loading.off();
                    }
                });
            },
            refreshProbe: function(p) {
                $.ajax({
                    url: meerkat.probes.probes[p].id + '.json',
                    dataType: 'json',
                    error: function(jqXHR, textStatus, errorThrown) {
                        /*[TODO: error handling ]*/
                        alert(errorThrown);
                        meerkat.loading.off();
                    },
                    success: function(data, textStatus, jqXHR) {
                        meerkat.probes.probes[p] = data.body;

                        /* render the data */
                        meerkat.probes.renderProbe(p);

                        /* show it */
                        $('#probes .section-body').show();

                        meerkat.loading.off();
                    }
                });
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
                    .html(ConvertJsonToTable(data, null, 'table', null));

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
                    .bind('click', {p: p, id: meerkat.probes.probes[p].id}, meerkat.probes.probeToggle);

                probeHtml
                    .find('.probeRefresh')
                    .unbind('click')
                    .bind('click', {p: p, id: meerkat.probes.probes[p].id}, meerkat.probes.probeRefresh);

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
                    'dd.status': 'status'
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
                meerkat.loading.on();
                $.ajax({
                    url: 'log.json',
                    dataType: 'json',
                    error: function(data, textStatus, jqXHR) {
                        /*[TODO: error handling ]*/
                        alert(errorThrown);
                        meerkat.loading.off();
                    },
                    success: function(data, textStatus, jqXHR) {
                        /*[TODO: error handling ]*/
                        data.body.log = data.body.log.join("\n");
                        $('#log').render(data.body, meerkat.log.directives.main);

                        /* show it */
                        $('#log .section-body').show();

                        meerkat.loading.off();
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
            format_ms: function(ms) {
                return (ms / 1000) + " secs";
            },
            format_mb: function(mb) {
                return mb + " MB";
            }
        }
    }
})(jQuery);

$(meerkat.init);

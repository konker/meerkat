
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
        master: {
            init: function() {
                meerkat.master.refresh();
            },
            masterToggle: function() {
                meerkat.master.refresh();
                return false;
            },
            refresh: function() {
                /* fetch JSON data from the server */
                $.getJSON('master.json', function(data, textStatus, jqXHR) {
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

                    /* visual aids */
                    if (data.body.status == 'ON') {
                        $('#masterToggle')
                            .removeClass('btn-danger')
                            .addClass('btn-success')
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
                            .text('Master OFF');
                        $('#master dl')
                            .find('dd.status')
                            .removeClass('text-success')
                            .addClass('text-error');
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
                meerkat.probes.refresh();
            },
            probeToggle: function(e) {
                meerkat.probes.refreshProbe(e.data.p);
                return false;
            },
            toggleOpenProbe: function(e) {
                var p = $('#' + e.data.id);
                if (p.hasClass('open')) {
                    p.removeClass('open').addClass('closed');
                    p.find('i')
                        .removeClass('icon-chevron-down')
                        .addClass('icon-chevron-right');
                }
                else {
                    p.removeClass('closed').addClass('open');
                    p.find('i')
                        .removeClass('icon-chevron-right')
                        .addClass('icon-chevron-down');
                }
                return false;
            },
            refresh: function() {
                $.getJSON('probes.json', function(data, textStatus, jqXHR) {
                    /*[TODO: error handling ]*/

                    meerkat.probes.probes = data.body.probes;

                    /* render the data */
                    $('#probes').render(data.body, meerkat.probes.directives.main);

                    for (var p in data.body.probes) {
                        meerkat.probes.renderProbe(p);
                    }
                });
            },
            refreshProbe: function(p) {
                $.getJSON(meerkat.probes.probes[p].id + '.json', function(data, textStatus, jqXHR) {
                    /*[TODO: error handling ]*/

                    meerkat.probes.probes[p] = data.body;

                    /* render the data */
                    meerkat.probes.renderProbe(p);
                });
            },
            renderProbe: function(p) {
                var probeHtml = $('#' + meerkat.probes.probes[p].id);

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

                /* visual aids */
                if (meerkat.probes.probes[p].status == 'ON') {
                    probeHtml
                        .find('.probeToggle')
                        .removeClass('btn-danger')
                        .addClass('btn-success')
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
                        .text('Probe OFF');

                    probeHtml
                        .find('dd.status')
                        .removeClass('text-success')
                        .addClass('text-error');
                }

                /* show it */
                if (!probeHtml.hasClass('open') && !probeHtml.hasClass('closed')) {
                    probeHtml.addClass('closed');
                }
            },
            directives: {
                main: {
                    '.probe': {
                        'probe<-probes': {
                            '@id': 'probe.id',
                            'h3 span.id': 'probe.label',
                            'dd.status': 'probe.status'
                        }
                    }
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
                $.getJSON('log.json', function(data, textStatus, jqXHR) {
                    /*[TODO: error handling ]*/
                    data.body.log = data.body.log.join("\n");
                    $('#log').render(data.body, meerkat.log.directives.main);
                });
            },
            directives: {
                main: {
                    "pre": "log"
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

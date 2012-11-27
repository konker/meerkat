
var meerkat = (function($) {
    var NODES_JSON_URL  = '/nodes.json',
        MASTER_JSON_URL = '/master.json',
        LOG_JSON_URL    = '/log.json';

    return {
        init: function() {
            meerkat.util.init();
            meerkat.nodes.init();
            meerkat.log.init();
        },
        nodes: {
            nodes: null,
            image_width: 400,
            image_height: 225,

            init: function() {
                meerkat.nodes.loadNodes();
            },
            loadNodes: function() {
                meerkat.util.loading.on();

                $.ajax({
                    url: NODES_JSON_URL,
                    dataType: 'json',
                    error: function(jqXHR, textStatus, errorThrown) {
                        /*[TODO: error handling ]*/
                        meerkat.util.alert.show("Could not load nodes data.", errorThrown);
                        meerkat.util.loading.off();
                    },
                    success: function(data, textStatus, jqXHR) {
                        meerkat.nodes.nodes = data.body.nodes;

                        /* render the data */
                        meerkat.nodes.reset();
                        $('#nodes').render(data.body, meerkat.nodes.directives.main);

                        for (var p in data.body.nodes) {
                            meerkat.nodes.renderNode(p);
                        }

                        /* nodes refresh event handler */
                        $('#nodesRefresh')
                            .unbind('click')
                            .bind('click', meerkat.nodes.loadNodes)
                            .show();

                        /* show it */
                        $('#nodes .section-body').show();

                        meerkat.util.loading.off();
                    }
                });
                return false;
            },
            reset: function() {
              $('#nodes .section-body')
                .empty();
              $('#templates .node').clone().appendTo('#nodes .section-body');
            },
            refresh: function() {
              //TODO
            },
            nodeRefreshCB: function(e) {
                meerkat.nodes.refreshOne(e.data.p);
                return false;
            },
            refreshOne: function(p) {
                meerkat.util.loading.on();

                $.ajax({
                    url: '/' + meerkat.nodes.nodes[p].id + '.json',
                    dataType: 'json',
                    error: function(jqXHR, textStatus, errorThrown) {
                        /*[TODO: error handling ]*/
                        meerkat.util.alert.show("Could not load node data.", errorThrown);
                        meerkat.util.loading.off();
                    },
                    success: function(data, textStatus, jqXHR) {
                        meerkat.nodes.nodes[p] = data.body;

                        /* render the data */
                        meerkat.nodes.renderNode(p);

                        /* show it */
                        $('#nodes .section-body').show();

                        meerkat.util.loading.off();
                    }
                });
            },
            toggleOpenNode: function(e) {
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
            renderNode: function(p) {
                var nodeHtml = $('#' + meerkat.nodes.nodes[p].info.ip_address);

                /* render status */
                console.log(meerkat.nodes.nodes[p])
                console.log(nodeHtml)
                /*
                nodeHtml
                    .find('.node-body')
                    .render(meerkat.nodes.nodes[p], meerkat.nodes.directives.single);
                */
                /* render data */
                /*
                var data = meerkat.nodes.nodes[p].data;
                for (var r in data) {
                    if (data[r].metadata.timestamp) {
                        data[r].metadata.timestamp =
                            meerkat.util.format_timestamp(data[r].metadata.timestamp);
                    }
                    nodeHtml
                        .find('.dbody')
                        .empty()
                        .append(ConvertJsonToTable([data[r].metadata], null,
                                    'table table-bordered', null));

                    if (typeof(data[r].data) == 'object') {
                        for (var rr in data[r].data) {
                            if (data[r].data[rr] && data[r].data[rr].image_path) {
                                data[r].data[rr].image_path = data[r].data[rr].image_path.substr(data[r].data[rr].image_path.lastIndexOf('/') + 1);
                                data[r].data[rr].image = '<canvas id="holder' + rr + '" width="'+ meerkat.nodes.image_width +'" height="'+ meerkat.nodes.image_height+'"></canvas>';
                            }
                            if (data[r].data[rr].id) {
                                delete data[r].data[rr].id;
                            }
                            if (data[r].data[rr].detected) {
                                data[r].data[rr].num_detected = data[r].data[rr].detected.length;
                            }
                        }
                        nodeHtml
                            .find('.dbody')
                            .append(ConvertJsonToTable(data[r].data, null,
                                            'table table-bordered', null));

                        for (var rr in data[r].data) {
                            if (data[r].data[rr].image_path) {
                                var ctx = $('#holder' + rr).get(0).getContext('2d');
                                var dataimage = new Image();
                                dataimage.onload = function() {
                                    ctx.drawImage(dataimage, 0, 0, meerkat.nodes.image_width, meerkat.nodes.image_height);
                                    if (data[r].data[rr].num_detected > 0) {
                                        var x_fact = (meerkat.nodes.image_width / data[r].data[rr].image_width);
                                        var y_fact = (meerkat.nodes.image_height / data[r].data[rr].image_height);

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
                        nodeHtml
                            .find('.dbody')
                            .append('<pre class="scalar">' + data[r].data + '</pre>');
                    }
                }
                */

                /* event handlers */
                nodeHtml
                    .find('h3')
                    .unbind('click')
                    .bind('click', {id: meerkat.nodes.nodes[p].id}, meerkat.nodes.toggleOpenNode);

                nodeHtml
                    .find('.nodeRefresh')
                    .unbind('click')
                    .bind('click', {p: p}, meerkat.nodes.nodeRefreshCB);

                /* visual aids */
                if (meerkat.nodes.nodes[p].status == 'ON') {
                    nodeHtml
                        .find('.nodeToggle')
                        .removeClass('btn-danger')
                        .addClass('btn-success')
                        .find('.lbl')
                        .text('node ON');

                    nodeHtml
                        .find('dd.status')
                        .removeClass('text-error')
                        .addClass('text-success');
                }
                else {
                    nodeHtml
                        .find('.nodeToggle')
                        .removeClass('btn-success')
                        .addClass('btn-danger')
                        .find('.lbl')
                        .text('node OFF');

                    nodeHtml
                        .find('dd.status')
                        .removeClass('text-success')
                        .addClass('text-error');
                }

                if (!nodeHtml.hasClass('open') && !nodeHtml.hasClass('closed')) {
                    nodeHtml.addClass('closed');
                }

                /* show it */
                $('#nodes .section-body').show();
            },
            directives: {
                main: {
                    '.node': {
                        'node<-nodes': {
                            '@id': 'node.info.ip_address',
                            'h3 span.node-label': 'node.info.host',
                        }
                    }
                },
                single: {
                    'dd.status': 'info.status',
                    'dd.ip_address': 'info.ip_address'
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

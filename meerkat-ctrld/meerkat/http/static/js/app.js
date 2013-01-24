App = Ember.Application.create({
    VERSION: "0.1",
    NODES_JSON_URL: '/meerkat/nodes.json',
    NODE_JSON_URL: '/meerkat/node.json',
    LOG_JSON_URL: '/meerkat/log.json',

    ready: function() {
        App.util.init();
        App.MainView.create().appendTo('#container');
        App.nodeListController.set('content', App.Node.all());
        App.logController.set('content', App.Log.all());
    },
    nodeListController: Ember.ArrayController.create({
        content: null
    }),
    logController: Ember.ArrayController.create({
        content: null,
    }),
    MainView: Ember.View.extend({
        templateName: 'main'
    }),
    NodeListView: Ember.View.extend({
        templateName: 'node-list',
        refresh: function(evt) {
            App.Node.all();
        }
    }),
    NodeView: Ember.View.extend({
        templateName: 'node',

        toggleOpen: function(evt) {
            $(evt.target).closest('.node').toggleClass('closed');
        },
        refresh: function(evt) {
            var id = $(evt.target).closest('.node').attr('id');
            console.log(id);
            App.Node.find(id);
        }
    }),
    LogView: Ember.View.extend({
        templateName: 'log',

        refresh: function() {
            App.Log.all();
        }
    })
});

App.Log = Ember.Object.extend();
App.Log.reopenClass({
    log: Ember.A(),
    all: function() {
        App.util.loading.on();

        var _log = this.log;
        $.ajax({
            url: App.LOG_JSON_URL,
            type: 'GET',
            dataType: 'json',
            error: function(jqXHR, textStatus, errorThrown) {
                /*[TODO: error handling ]*/
                App.util.alert.show("Could not execute operation.", errorThrown);
                App.util.loading.off();
            },
            success: function(data, textStatus, jqXHR) {
                _log.clear();
                _log.pushObjects(data.body.log);
                App.util.loading.off();
            }
        });
        return _log;
    }
});

App.Node = Ember.Object.extend();
App.Node.reopenClass({
    nodes: Ember.A(),
    all: function() {
        App.util.loading.on();

        var _nodes = this.nodes;
        $.ajax({
            url: App.NODES_JSON_URL,
            type: 'GET',
            dataType: 'json',
            error: function(jqXHR, textStatus, errorThrown) {
                /*[TODO: error handling ]*/
                App.util.alert.show("Could not execute operation.", errorThrown);
                App.util.loading.off();
            },
            success: function(data, textStatus, jqXHR) {
                _nodes.clear();
                console.log(data.body.nodes);
                for (var n in data.body.nodes) {
                    if (data.body.nodes.hasOwnProperty(n)) {
                        console.log(data.body.nodes[n]);
                        _nodes.pushObject(App.Node.create(data.body.nodes[n]));
                    }
                }
                App.util.loading.off();
            }
        });
        return _nodes;
    },
    find: function(id) {
        App.util.loading.on();

        var _nodes = this.nodes;
        $.ajax({
            url: App.NODE_JSON_URL,
            data: { id: id },
            type: 'GET',
            dataType: 'json',
            error: function(jqXHR, textStatus, errorThrown) {
                /*[TODO: error handling ]*/
                App.util.alert.show("Could not execute operation.", errorThrown);
                App.util.loading.off();
            },
            success: function(data, textStatus, jqXHR) {
                console.log(data.body);
                _nodes[_nodes.indexOf(_nodes.findProperty('id', id))] = App.Node.create(data.body);
                App.util.loading.off();
            }
        });
        return _nodes.findProperty('id', id);
    }
});

App.reopen({
    util: {
        init: function() {
            App.util.alert.init();
            Handlebars.registerHelper('format_timestamp', App.util.format_timestamp_helper);
            Handlebars.registerHelper('format_secs', App.util.format_secs_helper);
            Handlebars.registerHelper('format_b', App.util.format_b_helper);
            Handlebars.registerHelper('format_kb', App.util.format_kb_helper);
            Handlebars.registerHelper('format_mb', App.util.format_mb_helper);
        },
        alert: {
            init: function() {
                //$('#alert').alert();
                $('#alert .close').bind('click', App.util.alert.hide);
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
                App.util.loading._stack++;
                App.util.loading._setLoading(true);
            },
            off: function() {
                App.util.loading._stack--;
                if (App.util.loading._stack <= 0) {
                    App.util.loading._setLoading(false);
                }
            },
            _setLoading: function(on) {
                if (on) {
                    $('h1').addClass('loading');
                }
                else {
                    $('h1').removeClass('loading');
                    App.util.loading._stack = 0;
                }
            }
        },
        format_timestamp_helper: function(property, options) {
            var ts = Ember.Handlebars.get(this, property, options);
            return new Handlebars.SafeString(App.util.format_timestamp(ts));
        },
        format_timestamp: function(ts) {
            var d = new Date(ts);
            return jQuery.timeago(d) + "<br/><small>" + App.util.ReadableDateString(d) + "</small><br/><small>" + ts + "</small>";
        },
        /*
        format_timestamp: function(ts) {
            return App.util.ReadableDateString(new Date(ts)) + "<br/><small>" + ts + "</small>";
        },
        */
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
        format_secs_helper: function(property, options) {
            var secs = Ember.Handlebars.get(this, property, options);
            return App.util.format_secs(secs);
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
        format_b_helper: function(property, options) {
            var b = Ember.Handlebars.get(this, property, options);
            return App.util.format_b(b);
        },
        format_b: function(b) {
            if (b > 1024) {
                return App.util.format_kb(b/1024);
            }
            return b.toFixed(2) + " KB";
        },
        format_kb_helper: function(property, options) {
            var kb = Ember.Handlebars.get(this, property, options);
            return App.util.format_kb(kb);
        },
        format_kb: function(kb) {
            if (kb > 1024) {
                return App.util.format_mb(kb/1024);
            }
            return kb.toFixed(2) + " KB";
        },
        format_mb_helper: function(property, options) {
            var kb = Ember.Handlebars.get(this, property, options);
            return App.util.format_mb(mb);
        },
        format_mb: function(mb) {
            if (mb > 1024) {
                return (mb/1024).toFixed(2) + " GB";
            }
            return mb.toFixed(2) + " MB";
        }
    }
});

/*
App = Ember.Application.create({
    ready: function() {
        console.log('App.ready');
        App.nodeListController = App.NodeListController.create();
        App.nodeListController.kinit();
        App.nodeListView = App.NodeListView.create({
            controller: App.nodeListController
        }).appendTo('#container');

    },

    NodeController: Ember.ObjectController.extend({
    }),
    NodeView: Ember.View.extend({
        templateName: 'node'
    }),

    NodeListController: Ember.ArrayController.extend({
        content: Ember.A(),
        kinit: function() {
            console.log('NodeListController.init');
            this.content.push(Ember.Object.create({
                label: 'klonk0',
                status: 'OFF'
            }));
            this.content.push(Ember.Object.create({
                label: 'klonk1',
                status: 'OFF'
            }));
        }
    }),
    NodeListView: Ember.View.extend({
        templateName: 'node-list'
    }),

    LogController: Ember.Controller.extend({
        log: 'konk'
    }),
    LogView: Ember.View.extend({
        templateName: 'log'
    }),

    ApplicationController: Ember.Controller.extend({
    }),
    ApplicationView: Ember.View.extend({
        templateName: 'application'
    }),
    Router: Ember.Router.extend({
        root: Ember.Route.extend({
            index: Ember.Route.extend({
                route: '/'
            })
        }),
        enableLogging: true
    })
});
App.NodeListView.reopenClass({
    controller: App.NodeListController.create()
});

App.initialize();
*/
/*
App = Ember.Application.create();
App.ApplicationController = Ember.Controller.extend();

App.ApplicationView = Ember.View.extend({
  templateName: 'application'
});
App.LogView = Ember.View.extend({
  templateName: 'log'
});
alert(App.LogView);

App.Router = Ember.Router.extend({
  root: Ember.Route.extend({
    index: Ember.Route.extend({
      route: '/'
    })
  })
})

App.initialize();
$('#container').append(App.LogView);
*/


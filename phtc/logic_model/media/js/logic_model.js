(function (jQuery) {
    Backbone.sync = function (method, model, success, error) {
    };

    var Column = Backbone.Model.extend({
        defaults: {
        },
        aboutMe: function() {
        },
    });
    var ColumnCollection = Backbone.Collection.extend({
        model: Column
    });

    var ColumnView = Backbone.View.extend({
        tagName: "span",
        className: "column_span",
        events: {
        },
        initialize: function (options, render) {
            var self = this;
            _.bindAll(this, "render", "unrender");
            this.model.bind("destroy", this.unrender);
            this.model.bind("change:minimized", this.render);
            this.template = _.template(jQuery("#logic-model-column").html());
            this.render();
        },
        render: function () {
            var ctx = this.model.toJSON();
            this.el.innerHTML = this.template(ctx);
        },
        unrender: function () {
            jQuery(this.el).fadeOut('fast', function() {
                jQuery(this.el).remove();
            });            
        }
    });

    ///////


    window.LogicModelView = Backbone.View.extend({
        events: {
            /*
            "click .reset-state": "onResetState",
            "click .decision-point-button": "onDecisionPoint",
            "click .choose-again": "onChooseAgain",
            "click i.icon-question-sign": "onHelp",
            "click .choose-cirrhosis-again": "onResetState",
            "click .run_test": "onRunTest"            
            */
            // new ones for changing the phase:

            // new ones for changing the scenario:

        },
        initialize: function(options) {
            _.bindAll(this ,
                "render" ,
                "onAddColumn",
                "onRemoveColumn"
            );
            this.getSettings();
            // Paint the columns:
            this.columns = new ColumnCollection();
            //this.activityState.bind("change", this.render);
            this.columns.bind("add", this.onAddColumn);
            this.columns.bind("remove", this.onRemoveColumn);
            this.render();
        },

        render: function() {
            var self = this;
            jQuery("li.next, h1.section-label-header, li.previous").hide();
        },

        getSettings: function() {
            // Fetch the list of columns and scenarios from the back end.
            var self = this;
            jQuery.ajax({
                type: 'POST',
                url: '/_logic_model/settings/',
                data: {
                },
                dataType: 'json',
                error: function () {
                    alert('There was an error.');
                },
                success: function (json, textStatus, xhr) {
                    self.columns.add(json.columns);
                }
            });
        }
        ,onAddColumn: function(column) {
            var view = new ColumnView({
                model: column,
                parentView: this
            });
            jQuery("div.logic-model-columns").append(view.el);
        },
        onRemoveColumn: function(column) {
            console.log ("removingcolumn");
        },
    });


}(jQuery));    
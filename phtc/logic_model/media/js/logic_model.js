(function (jQuery) {










    Backbone.sync = function (method, model, success, error) {
    };

    var DEBUG_PHASE = 4;

    var Box = Backbone.Model.extend({
        defaults: {
        },
        aboutMe: function() {
        },
    });
    var BoxCollection = Backbone.Collection.extend({
        model: Box
    });

    var BoxView = Backbone.View.extend({
        className: "backbone_box_div",
        events: {
        },
        initialize: function (options, render) {
            var self = this;
            _.bindAll(this, "render", "unrender", "onDrop", "setUpDroppable", "setUpDraggable");
            this.model.bind("destroy", this.unrender);
            this.model.bind("change:minimized", this.render);
            this.template = _.template(jQuery("#logic-model-box").html());
            this.render();
        },

        onDrop: function (event, ui) {
            console.log ('on drop');
            the_draggable = ui.draggable;
            var origin_text = the_draggable.find('.text_box').val();
            the_draggable.css({top: '0px', left: '0px'});

            jQuery (event.target).find('.text_box').val(origin_text);
        },

        setUpDroppable: function (){
            var self = this;
            droppable_options = {
                accept: ".box_draggable" ,
                /* activeClass: "active_droppable", */
                hoverClass: "hover_droppable",
                drop: self.onDrop
            }
            jQuery (this.el).find ('.box_droppable').droppable(droppable_options);

        },

        setUpDraggable: function () {
            var self = this;
            draggable_options = {
                handle : '.box_handle',
            }

            jQuery (this.el).find ('.box_draggable').draggable(draggable_options);
        },
        render: function () {
            var self = this;
            var ctx = this.model.toJSON();
            this.el.innerHTML = this.template(ctx);

            self.setUpDraggable();
            self.setUpDroppable();
            return this;
        },

        unrender: function () {
            jQuery(this.el).fadeOut('fast', function() {
                jQuery(this.el).remove();
            });            
        },



    });


    //////////////////


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
        className: "backbone_column_span",
        events: {
        },
        initialize: function (options, render) {
            var self = this;
            _.bindAll(self, "render", "unrender",  "addBox");
            self.model.bind("destroy", self.unrender);
            self.model.bind("change:minimized", self.render);
            
            self.boxes = new BoxCollection();
            self.boxes.add ([
                    { name: '1'  },
                    { name: '2' },
                    { name: '3' },
                    { name: '4' },
                    { name: '5' },
                    { name: '6' }
            ]);
            
            self.template = _.template(jQuery("#logic-model-column").html());
            self.render();
        },

        addBoxes: function() {
            var self = this;
            self.boxes.each(self.addBox);
        },


        addBox: function(box) {
            var self = this;
            view = new BoxView({
                model: box,
                parentView : self
            });
            jQuery(self.el).find('.boxes').append(view.el);
        },

        render: function () {
            var self = this;
            var ctx = this.model.toJSON();
            this.el.innerHTML = this.template(ctx);
            self.addBoxes();
            return this;
        },
        unrender: function () {
            jQuery(this.el).fadeOut('fast', function() {
                jQuery(this.el).remove();
            });            
        },
    });

    ///////


    window.LogicModelView = Backbone.View.extend({
        events: {
            
            "click .next_phase": "goToNextPhase",
            "click .previous_phase": "goToPreviousPhase"
            /*
            "click .choose-again": "onChooseAgain",
            "click i.icon-question-sign": "onHelp",
            "click .choose-cirrhosis-again": "onResetState",
            "click .run_test": "onRunTest"            
            */
            // new ones for changing the phase:

            // new ones for changing the scenario:

        },
        phases: null,
        current_phase : null,

        initialize: function(options) {
            var self = this;
            _.bindAll(this ,
                "render" ,
                "onAddColumn",
                "onRemoveColumn",
                "goToNextPhase",
                "goToPreviousPhase"

            );
            self.getSettings();
            // Paint the columns:
            self.columns = new ColumnCollection();
            //this.activityState.bind("change", this.render);
            self.columns.bind("add", this.onAddColumn);
            self.columns.bind("remove", this.onRemoveColumn);

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
                    self.phases = json.game_phases;
                    self.setUpPhases();
                    self.render();
                }
            });
        },
        setUpPhases : function() {
            var self = this;
            if (DEBUG_PHASE != undefined) {
                self.current_phase = DEBUG_PHASE;
            } else {
                self.current_phase = 0;
            }
        },

        paintPhase: function() {
            var self = this;
            var phase_info = self.phases[self.current_phase];
            

            jQuery("#phase_container").attr("class", phase_info.css_classes);

            jQuery('.logic-model-game-phase-instructions').html(phase_info.instructions);
            if (self.current_phase == 0) {
                jQuery ('.previous_phase').hide();
            } else {
                jQuery ('.previous_phase').show();
            }
            if (self.current_phase == self.phases.length - 1) {
                jQuery ('.next_phase').hide();
            } else {
                jQuery ('.next_phase').show();
            }

        },



        goToNextPhase: function() {
            var self = this;
            self.current_phase = self.current_phase  + 1;
            self.paintPhase();
        },


        goToPreviousPhase: function() {
            var self = this;
            jQuery("li.next, h1.section-label-header, li.previous").hide();
            self.current_phase = self.current_phase - 1;
            self.paintPhase();
        },

        render: function() {
            var self = this;
            jQuery("li.next, h1.section-label-header, li.previous").hide();
            //
            self.paintPhase();
        },

        onAddColumn: function(column) {
            var self = this;
            var view = new ColumnView({
                model: column,
                parentView: this
            });
            jQuery("div.logic-model-columns").append(view.el);
        },
        onRemoveColumn: function(column) {
            var self = this;
            console.log ("removingcolumn");
        },
    });


}(jQuery));    
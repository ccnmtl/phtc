(function (jQuery) {


    Backbone.sync = function (method, model, success, error) {
    };

    var DEBUG_PHASE = 1;

    var Box = Backbone.Model.extend({
        defaults: {
            "contents":  "",
            'active': true
        },
        aboutMe: function() {
        },
    });


    var BoxCollection = Backbone.Collection.extend({
        model: Box
    });


    function turnOffBoth(element) {
        jQuery (element).find ('.box_droppable').droppable( "disable" );
        jQuery (element).find ('.box_draggable').draggable( "disable" );
    }

    function turnOnDraggable(element) {
        jQuery (element).find ('.box_droppable').droppable( "disable" );
        jQuery (element).find ('.box_draggable').draggable( "enable" );
    }

    function turnOffDraggable(element) {
        the_droppable = jQuery (element).find ('.box_droppable');
        the_droppable.droppable( "enable" );
        jQuery (element).find ('.box_draggable').draggable( "disable");
    }

    var BoxView = Backbone.View.extend({
        className: "backbone_box_div",
        events: {
            'change textarea' : 'render'
        },
        initialize: function (options, render) {
            var self = this;
            _.bindAll(self,
                "render",
                "unrender",
                "setUpDroppable",
                "setUpDraggable",
                "hasText",
                "make_active", 
                "make_inactive"
            );

            self.model.bind("destroy", self.unrender);
            //self.model.bind("testForDraggable", self.testForDraggable);

            self.model.bind("make_active", self.make_active);
            self.model.bind("make_inactive", self.make_inactive);


            self.model.bind("render", self.render);
            
            self.template = _.template(jQuery("#logic-model-box").html());
            var ctx = self.model.toJSON();
            self.el.innerHTML = self.template(ctx);
            
            self.setUpDraggable();
            self.setUpDroppable();

            self.render();
        },

        onDrop: function (event, ui) {
            var source = ui.draggable.context;
            var origin_text = jQuery(source).find('.text_box').val();
            var destination = event.target;
            //move the source back to its original spot:
            jQuery(source).css({top: '0px', left: '0px'});
            //remove the distracting placeholder:
            jQuery( destination).find( ".placeholder" ).remove();
            // set the text in the destination:
            jQuery (destination).find('.text_box').val(origin_text);
            // remove the text in the source:
            jQuery(source).find('.text_box').val('');
            // since the destination now has text in it, make it draggable.
            turnOnDraggable(destination);
            jQuery (destination).find ('.box_handle').show();
            // since the source is now empty, make it undraggable.
            var the_actual_box = source.parentElement.parentElement;
            turnOffDraggable (the_actual_box);
            jQuery (the_actual_box).find ('.box_handle').hide();

        },

        setUpDroppable: function (){
            //console.log ("in setupdroppable")
            var self = this;
            droppable_options = {
                accept: ".box_draggable" ,
                /* activeClass: "active_droppable", */
                hoverClass: "hover_droppable",
                drop: self.onDrop,
                activate: self.render
            }
            jQuery (this.el).find ('.box_droppable').droppable(droppable_options);

        },

        hasText: function() {
            var self = this;

            if (jQuery (this.el).find('.text_box').val().length > 0) {
                // this has content in it, so return true.
                return true;
            }
            return false;
        },


        setUpDraggable: function () {
            var self = this;
            draggable_options = {
                handle : '.box_handle',
                revert : 'invalid'
            }
            jQuery (this.el).find ('.box_draggable').draggable(draggable_options);
        },

        render: function () {
            var self = this;

            if (self.model.get('active') == false ) {
                jQuery (this.el).addClass ('inactive_box');
                jQuery (this.el).find('.text_box').attr({'disabled':true})
                turnOffBoth(this.el);
                jQuery (this.el).find ('.box_handle').hide();
            }
            else {

                jQuery (this.el).removeClass ('inactive_box');
                jQuery (this.el).find('.text_box').attr({'disabled':false})
                    if (self.hasText()) {
                        turnOnDraggable(this.el);
                        jQuery (this.el).find ('.box_handle').show();
                    } else { // empty
                        turnOffDraggable(this.el);
                        jQuery (this.el).find ('.box_handle').hide();
                    }

            }


            //self.activateDraggable();
            return this;
        },

        make_active: function () {
            var self = this;
            self.model.set ({active: true});

        },
        make_inactive: function () {
            var self = this;
            self.model.set ({active: false});
        },


        unrender: function () {
            jQuery(this.el).fadeOut('fast', function() {
                jQuery(this.el).remove();
            });            
        },



    });


    //////////////////


    var Column = Backbone.Model.extend({
        what : 'model',
        defaults: {
            active : true
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
            _.bindAll(self, "render", "unrender",  "addBox", "check_the_boxes");
            //self.model.bind("destroy", self.unrender);
            //self.model.bind("change:minimized", self.render);
            self.model.bind("check_the_boxes", self.check_the_boxes);
            //console.log (self.model.title);
            self.boxes = new BoxCollection();
            self.boxes.add ([
                { name: '1' },
                { name: '2' },
                { name: '3' },
                { name: '4' },
                { name: '5' },
                { name: '6' }
            ]);
            
            self.template = _.template(jQuery("#logic-model-column").html());
            self.render();
        },



        check_the_boxes: function() {
            var self = this;
            if (self.model.get ('active')) {
                self.boxes.each (function (a) { a.trigger ('make_active'); });
            } else {
                self.boxes.each (function (a) { a.trigger ('make_inactive'); });
            } 
            // test all boxes for draggableness.
            self.boxes.each (function (a) { a.trigger ('render'); });

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
                    self.columns_in_each_phase = json.columns_in_each_phase;
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
            //console.log ('phase id is ' + phase_info.id);
            var active_columns_for_this_phase = self.columns_in_each_phase[phase_info.id];
            //console.log (active_columns_for_this_phase);
            self.columns.each (function (col) {
                //console.log (col.id)
                var active = (active_columns_for_this_phase.indexOf (col.id) != -1 )
                // console.log (active);
                col.set ({active: active});
            });

            self.columns.each (function (a) { a.trigger ('check_the_boxes'); });
            

            // set the #phase_container span so that
            // the CSS can properly paint this phase of the game.
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
            /*
            console.log ('id is :')
            console.log (column.get ('id'));
            console.log ('name is :')
            console.log (column.get ('name'));
            */
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
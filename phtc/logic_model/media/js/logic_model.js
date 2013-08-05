(function (jQuery) {
"use strict";


    Backbone.sync = function (method, model, success, error) {
        };

    var DEBUG_PHASE = 1;
    var NUMBER_OF_COLUMNS = 9;

    function findBox (el) {
        return jQuery (el).closest('.backbone_box_div').data('view');
    }


    var Scenario = Backbone.Model.extend({
        defaults: {
        },
        aboutMe: function() {
        },
    });

    var ScenarioCollection = Backbone.Collection.extend({
        model: Scenario
    });

    var ScenarioView = Backbone.View.extend({
        className: "backbone_scenario_div",
        events: {
            //'change textarea' : 'render',
            'click .try_this_scenario' : 'chooseMe'
        },

        initialize: function (options, render) {
            var self = this;
            _.bindAll(self,
                "render"
            );
            self.template = _.template(jQuery("#logic-model-scenario").html());
            var ctx = self.model.toJSON();
            self.el.innerHTML = self.template(ctx);
        },
        chooseMe : function () {
            var self = this;
            //jQuery ('.scenario_info').html (self.model.get ('instructions'));
            jQuery ('.scenario_instructions').html (self.model.get ('instructions'));
            self.LogicModelView.goToNextPhase();

        }
    });
    /////////


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


    var BoxView = Backbone.View.extend({
        className: "backbone_box_div",
        events: {
            'change textarea' : 'render',
            'click .switch_color' : 'nextColor'
        },
        initialize: function (options, render) {
            var self = this;
            _.bindAll(self,
                "render",
                "unrender",
                "setUpDroppable",
                "setUpDraggable",
                "hasText",
                "makeActive", 
                "makeInactive",
                "nextColor",
                "draggedFrom",
                "draggedTo",
                "turnOffDraggableAndDroppable",
                "turnOnDraggable",
                "turnOffDraggable"
            );

            self.model.bind("destroy", self.unrender);
            self.model.bind("makeActive", self.makeActive);
            self.model.bind("makeInactive", self.makeInactive);
            self.model.bind("nextColor", self.nextColor);
            self.model.bind("render", self.render);
            
            self.template = _.template(jQuery("#logic-model-box").html());
            var ctx = self.model.toJSON();
            self.el.innerHTML = self.template(ctx);
            self.setUpDraggable();
            self.setUpDroppable();
            self.render();

            // sorry, but we need to do this for the draggy-droppy stuff.
            self.$el.data('view', this);
        },


            // TODO: turn these into methods of the box object.
        turnOnDraggable: function() {
            var self = this;
            var jel = self.$el;
            jel.find ('.box_droppable').droppable( "disable" );
            jel.find ('.box_draggable').draggable( "enable" );
            jQuery (this.el).find ('.box_handle').show();
        },

        turnOffDraggable: function () {
            var self = this;
            var jel = self.$el;
            var the_droppable = jel.find ('.box_droppable');
            the_droppable.droppable( "enable" );
            jel.find ('.box_draggable').draggable( "disable");
            jQuery (this.el).find ('.box_handle').hide();
        },

        turnOffDraggableAndDroppable : function() {
            var self = this;
            var jel = self.$el;
            jel.find ('.box_droppable').droppable( "disable" );
            jel.find ('.box_draggable').draggable( "disable" );
            jel.find ('.box_handle').hide();
        },

        draggedFrom: function() {
            var self = this;
            var jel = self.$el;
            jel.find ('.box_draggable').css({top: '0px', left: '0px'});
            jel.find ('.box_handle').hide();
            jel.find ('.box_droppable').droppable( "enable" );
            jel.find ('.box_draggable').draggable( "disable");
        },

        draggedTo: function() {
            var self = this;
            var jel = self.$el;
            jel.find(".placeholder").remove();
            jel.find(".box_handle").show();
            jel.find ('.box_droppable').droppable( "disable" );
            jel.find ('.box_draggable').draggable( "enable" );
        },

        onDrop: function (event, ui) {
            var src_box = findBox(ui.draggable.context);
            var dst_box = findBox(event.target);
            src_box.draggedFrom();
            dst_box.draggedTo();
            // transfer text:
            var src_text = src_box.$el.find('.text_box').val();
            dst_box.$el.find('.text_box').val(src_text);
            src_box.$el.find('.text_box').val('');
            // transfer color:
            dst_box.model.set({'color_int': src_box.model.get('color_int')});
            dst_box.setColor();
            src_box.model.set({'color_int': 0});
            src_box.setColor();
        },

        setUpDroppable: function (){
            var self = this;
            var droppable_options = {
                accept: ".box_draggable" ,
                /* activeClass: "active_droppable", */
                hoverClass: "hover_droppable",
                drop: self.onDrop,
                //greedy: true,
                activate: self.render
            };
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

        setColor: function () {
            var self = this;
            var the_colors = self.model.get ('colors');
            var color_int  = self.model.get ('color_int');
            var color =  '#' + (the_colors[color_int % the_colors.length]);
            jQuery(self.el).find ('.cell').css('background-color', color);
            jQuery(self.el).find ('.text_box').css('background-color', color);
        },


        nextColor: function() {
            var self = this;
            self.model.set ({color_int: self.model.get ('color_int') + 1 });
            self.setColor();
        },


        setUpDraggable: function () {
            var self = this;
            var draggable_options = {
                handle : '.box_handle',
                revert : 'invalid',
                cursor: 'move',
                /*                helper: "clone", */

            };
            jQuery (this.el).find ('.box_draggable').draggable(draggable_options);
        },

        render: function () {
            var self = this;

            if (self.model.get('active') === false ) {
                jQuery (this.el).addClass ('inactive_box');
                self.turnOffDraggableAndDroppable();
                jQuery (this.el).find('.text_box').attr({'disabled':true});
            }
            else {
                jQuery (this.el).removeClass ('inactive_box');
                jQuery (this.el).find('.text_box').attr({'disabled':false});
                    if (self.hasText()) {
                        self.turnOnDraggable();
                    } else { // empty
                        self.turnOffDraggable();
                    }
            }
            return this;
        },

        makeActive: function () {
            var self = this;
            self.model.set ({active: true});
        },
        makeInactive: function () {
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
            self.model.bind("check_the_boxes", self.check_the_boxes);
            self.model.set ({boxModels: []});
            self.boxes = new BoxCollection();
            var the_columns = _.map (_.range(1, NUMBER_OF_COLUMNS + 1), function (num) {
                    return {'name':num.toString(), 'column' : self.model};
                }
            );
            self.boxes.add (the_columns);            
            self.model.set ();
            self.template = _.template(jQuery("#logic-model-column").html());
            self.render();
        },

        check_the_boxes: function() {
            // this is basically a render function here.
            var self = this;
            if (self.model.get ('active')) {
                self.boxes.each (function (a) { a.trigger ('makeActive'); });
                jQuery (this.el).addClass ('active_column');
            } else {
                self.boxes.each (function (a) { a.trigger ('makeInactive'); });
                jQuery (this.el).removeClass ('active_column');
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
            var view = new BoxView({
                model: box
            });
            jQuery(self.el).find('.boxes').append(view.el);
            var tmp = self.model.get('boxModels');
            tmp.push (view.model);
            self.model.set ({'boxModels' : tmp});
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
            "click .done-button": "goToNextPhase",
            "click .previous_phase": "goToPreviousPhase",
            "click .change_scenario": "goToFirstPhase"
        },
        phases: null,
        current_phase : null,

        initialize: function(options) {
            var self = this;

            _.bindAll(this ,
                "render" ,
                "onAddColumn",
                "onAddScenario",
                "onRemoveColumn",
                "goToNextPhase",
                "goToPreviousPhase"

            );
            self.getSettings();
            // Paint the columns:
            self.columns = new ColumnCollection();
            self.columns.bind("add", this.onAddColumn);


            self.scenarios = new ScenarioCollection();
            self.scenarios.bind("add", this.onAddScenario);

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
                    self.setUpColors (json.colors);
                    self.phases = json.game_phases;
                    self.scenarios.add (json.scenarios);
                    self.columns_in_each_phase = json.columns_in_each_phase;
                    self.setUpPhases();
                    self.render();
                }
            });
        },

        setUpColors : function (colors) {
            var self = this;
            self.colors = { colors: colors };
            self.columns.each (function (a) {
                var box_models = a.get('boxModels');
                for (var i=0;i<box_models.length;i++)  {
                    box_models[i].set ({colors:colors, color_int: -1});
                    box_models[i].trigger ('nextColor');
                }
             });
        },

        setUpPhases : function() {
            var self = this;
            if (DEBUG_PHASE !== undefined) {
                self.current_phase = DEBUG_PHASE;
            } else {
                self.current_phase = 0;
            }
        },

        paintPhase: function() {
            var self = this;
            jQuery("li.next, h1.section-label-header, li.previous").hide();
            var phase_info = self.phases[self.current_phase];
            var active_columns_for_this_phase = self.columns_in_each_phase[phase_info.id];
            self.columns.each (function (col) {
                if (active_columns_for_this_phase !== undefined) {
                    var whether_active = (active_columns_for_this_phase.indexOf (col.id) != -1 );
                    col.set ({active: whether_active});
                }
                // default is true, btw.
            });
            self.columns.each (function (a) { a.trigger ('check_the_boxes'); });
            // set the #phase_container span so that
            // the CSS can properly paint this phase of the game.
            jQuery("#phase_container").attr("class", phase_info.css_classes);
            jQuery('.logic-model-game-phase-instructions').html(phase_info.instructions);

            if (self.current_phase === 0) {
                jQuery ('.previous_phase').hide();
            } else {
                jQuery ('.previous_phase').show();
            }
            /*
            if (self.current_phase == self.phases.length - 1) {
                jQuery ('.next_phase').hide();
            } else {
                jQuery ('.next_phase').show();
            }
            */

            // unhide the last active donebutton on the page:
            jQuery('.done-button').removeClass ('visible');
            if (self.current_phase != self.phases.length - 1) {
                jQuery('.active_column').last().find ('.done-button').addClass('visible');
            }
        },

        goToFirstPhase: function() {
            var self = this;
            self.current_phase = 0;
            self.paintPhase();
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
            self.paintPhase();
        },

        onAddColumn: function(column) {
            var self = this;
            var view = new ColumnView({
                model: column
            });
            jQuery("div.logic-model-columns").append(view.el);
        },


        onAddScenario: function(scenario) {
            var self = this;

            var view = new ScenarioView({
                model: scenario
            });

            view.LogicModelView = self;

            jQuery("div.logic-model-initial-scenario-list").append(view.el);
        },

        onRemoveColumn: function(column) {
            var self = this;
            console.log ("removingcolumn");
        },
    });

}(jQuery));    
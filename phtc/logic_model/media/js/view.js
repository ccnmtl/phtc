LogicModel.LogicModelView = Backbone.View.extend({
    events: {
        "click .next_phase": "goToNextPhase",
        "click .done-button": "goToNextPhase",
        "click .previous_phase": "goToPreviousPhase",
        "click .change_scenario": "goToFirstPhase",
        "click .game-phase-help-button-div" : "showGamePhaseHelpBox",
        "click .help_box": "closeHelpBox",
        "click .add_a_row_button": "addARow"
    },
    phases: null,
    current_phase : null,

    initialize: function(options) {
        var self = this;

        _.bindAll(this ,
            "render" ,
            "onAddColumn",
            "onAddScenario",
            "goToNextPhase",
            "goToPreviousPhase",
            "showGamePhaseHelpBox",
            "addARow",
            "adjustRows",
            "checkEmptyBoxes"
        );
        self.getSettings();
        

        self.current_number_of_rows = LogicModel.NUMBER_OF_ROWS_INITIALLY_VISIBLE;
        
        // Paint the columns:
        self.columns = new LogicModel.ColumnCollection();
        self.columns.bind("add", this.onAddColumn);

        self.scenarios = new LogicModel.ScenarioCollection();
        self.scenarios.bind("add", this.onAddScenario);
    },

    showGamePhaseHelpBox: function () {
        var self = this;
        var phase_info = self.currentPhaseInfo();
        var the_template = jQuery('#logic-model-help-box').html();
        var title_copy = phase_info.name;
        if (title_copy === '' || title_copy === undefined ) {
            title_copy = 'Lorem ipsum';
        }
        var body_copy = phase_info.instructions;
        if (body_copy === '' || body_copy === undefined ) {
            body_copy = 'Lorem ipsum';
        }
        var the_data = {
            'help_title'  : title_copy,
            'help_body'   : body_copy
        };
        var the_html = _.template(the_template, the_data);
        jQuery( ".help_box" ).html (the_html);
        jQuery( ".help_box" ).show();
    },

    closeHelpBox : function() {
        var self = this;
        jQuery('.help_box').hide();
        jQuery('.help_box').html('');
    },


    checkEmptyBoxes : function() {
        var self = this;
        number_of_empty_active_columns = 0;
        self.columns.each (function (a) {
            column_is_active = a.get ('active');
            var box_models = a.get('boxModels');
            if (column_is_active) {
                column_is_empty = true;
                for (var i=0; i < box_models.length; i++)  {
                    if (box_models[i].get('contents').length > 0) {
                        column_is_empty = false;
                    }
                }
                if (column_is_empty) {
                    number_of_empty_active_columns = number_of_empty_active_columns + 1;
                    return;
                }
            }
        });
        if (number_of_empty_active_columns  === 0) {
            if (self.current_phase != self.phases.length - 1) {
                jQuery('.active_column').last().find ('.done-button').addClass('visible');
            }
        }
        else {
            jQuery('.active_column').last().find ('.done-button').removeClass('visible');
        }
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
                self.adjustRows();
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


    addARow: function() {
        var self = this;
        self.current_number_of_rows = self.current_number_of_rows + 1;
        self.adjustRows();
        if ( self.current_number_of_rows === LogicModel.NUMBER_OF_ROWS_TOTAL) {
            jQuery ('.add_a_row_button').hide();
        }
    },

    adjustRows: function() {
        var self = this;
        self.columns.each (function (c) {
            var box_models = c.get('boxModels');
            for (var i=0;i<box_models.length;i++)  {
                if (box_models[i].get ('row') <= self.current_number_of_rows) {
                    box_models[i].trigger ('showBox');
                }


                //checkEmptyBoxes

            }

         });
    },

    setUpPhases : function() {
        var self = this;
        if (typeof LogicModel.DEBUG_PHASE !== "undefined") {
            self.current_phase = LogicModel.DEBUG_PHASE;
        } else {
            self.current_phase = 0;
        }
    },

    currentPhaseInfo: function() {
        var self = this;
        return self.phases[self.current_phase];
    },

    paintPhase: function() {
        var self = this;
        var phase_info = self.currentPhaseInfo();
        var active_columns_for_this_phase = self.columns_in_each_phase[phase_info.id];
        self.columns.each (function (col) {
            if (active_columns_for_this_phase !== undefined) {
                var whether_active = (active_columns_for_this_phase.indexOf (col.id) != -1 );
                col.set ({active: whether_active});
            }
            // default is true, btw.
        });
        self.columns.each (function (a) { a.trigger ('turnOnActiveBoxes'); });
        // set the #phase_container span so that
        // the CSS can properly paint this phase of the game.
        jQuery("#phase_container").attr("class", phase_info.css_classes);
        jQuery('.logic-model-game-phase-name').html(phase_info.name);

        if (self.current_phase === 0) {
            jQuery ('.previous_phase').hide();
            jQuery("li.previous").show();
        } else {

            jQuery("li.previous").hide();
            jQuery ('.previous_phase').show();
        }


        
        if (self.current_phase == self.phases.length - 1) {
                jQuery("li.next").show();
            //jQuery ('.next_phase').hide();
        } else {
                jQuery("li.next").hide();
            //jQuery ('.next_phase').show();
        }
        

        // unhide the last active donebutton on the page:
        jQuery('.done-button').removeClass ('visible');
        /*
        if (self.current_phase != self.phases.length - 1) {
            jQuery('.active_column').last().find ('.done-button').addClass('visible');
        }
        */

        // unhide the last active donebutton on the page:
        jQuery('.add_a_row_button').removeClass ('visible');
        jQuery('.active_column').first().find('.add_a_row_button').addClass('visible');

        self.checkEmptyBoxes();
        
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
        var view = new LogicModel.ColumnView({
            model: column
        });
        view.parentView = self;

        view.boxes.bind("checkEmptyBoxes", self.checkEmptyBoxes);
        jQuery("div.logic-model-columns").append(view.el);
    },

    onAddScenario: function(scenario) {
        var self = this;
        var view = new LogicModel.ScenarioView({
            model: scenario
        });
        view.LogicModelView = self;
        jQuery("div.logic-model-initial-scenario-list").append(view.el);
    }

});
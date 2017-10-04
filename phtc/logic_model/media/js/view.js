LogicModel.LogicModelView = Backbone.View.extend({
    events: {
        'click .next_phase': 'goToNextPhase',
        'click .done-button': 'goToNextPhase',
        'click .previous_phase': 'goToPreviousPhase',
        'click .change_scenario': 'showSwitchScenarioWarning',
        'click .change_scenario_confirm': 'goToFirstPhase',
        'click .change_scenario_cancel': 'cancelSwitchScenario',
        'click .print_scenario': 'printScenarioTable',
        'click .help_box': 'closeHelpBox',
        'click .add_a_row_button': 'addARow',
        'click .wipe-table-button': 'showWipeTableWarning',
        'click .wipe-table-confirm-button': 'wipeTable',
        'click .wipe-table-cancel-button': 'cancelWipeTable',
    },
    phases: null,
    current_phase: null,

    initialize: function(options) {
        var self = this;

        _.bindAll(this ,
            'render' ,
            'onAddColumn',
            'onAddScenario',
            'goToNextPhase',
            'goToPreviousPhase',
            'addARow',
            'adjustRows',
            'checkEmptyBoxes',
            'showWipeTableWarning',
            'wipeTableValues',
            'wipeTable',
            'cancelWipeTable',
            'showSwitchScenarioWarning',
            'cancelSwitchScenario',
            'beforeLeavePage'
        );
        self.getSettings();

        self.current_number_of_rows =
            LogicModel.NUMBER_OF_ROWS_INITIALLY_VISIBLE;

        // Paint the columns:
        self.columns = new LogicModel.ColumnCollection();
        self.columns.bind('add', this.onAddColumn);

        self.scenarios = new LogicModel.ScenarioCollection();
        self.scenarios.bind('add', this.onAddScenario);

        jQuery('li.next a').on('click', this.beforeLeavePage);
        jQuery('li.previous a').on('click', this.beforeLeavePage);
    },

    closeHelpBox: function() {
        jQuery('.help-overlay').hide();
        jQuery('.help_box').hide();
        jQuery('.help_box').html('');
    },

    showWipeTableWarning: function() {
        jQuery('.help-overlay').show();
        jQuery('.wipe-table-button-div').show();
    },

    wipeTableValues: function() {
        var self = this;
        jQuery('.text_box').each(function(a, b) {b.value = ''; });
        self.columns.each(function(a) {
            var box_models = a.get('boxModels');
            for (var i=0; i < box_models.length; i++)  {
                box_models[i].set({'contents': ''});
                box_models[i].set({'color_int': 0});
                box_models[i].trigger('setColor');
            }
        });
    },

    wipeTable: function() {
        var self = this;
        self.wipeTableValues();
        jQuery('.help-overlay').hide();
        jQuery('.wipe-table-button-div').hide();
        self.current_phase = 1;
        self.current_number_of_rows =
            LogicModel.NUMBER_OF_ROWS_INITIALLY_VISIBLE;
        self.adjustRows();
        self.paintPhase();
    },

    cancelWipeTable: function() {
        jQuery('.help-overlay').hide();
        jQuery('.wipe-table-button').show();
        jQuery('.wipe-table-button-div').hide();
    },

    checkEmptyBoxes: function() {
        var self = this;
        self.ok_to_proceed = false;0;
        var number_of_empty_active_columns = 0;
        self.columns.each(function(a) {
            var column_is_active = a.get('active');
            var box_models = a.get('boxModels');
            if (column_is_active) {
                var column_is_empty = true;
                for (var i=0; i < box_models.length; i++)  {
                    if (box_models[i].get('contents').length > 0) {
                        column_is_empty = false;
                    }
                }
                if (column_is_empty) {
                    number_of_empty_active_columns =
                        number_of_empty_active_columns + 1;
                    return;
                }
            }
        });

        jQuery('.done-button').hide();
        if (number_of_empty_active_columns  === 0) {
            if (self.current_phase != self.phases.length - 1) {
                jQuery('.active_column').last()
                    .find('.done-button').show();
                jQuery('.active_column').last()
                    .find('.done-button').addClass('active');
                self.ok_to_proceed = true;
            }
        }
        else {
            jQuery('.active_column').last()
                .find('.done-button').show();
            jQuery('.active_column').last()
                .find('.done-button').removeClass('active');
            self.ok_to_proceed = false;
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
            error: function() {
                alert('There was an error.');
            },
            success: function(json, textStatus, xhr) {
                self.columns.add(json.columns);
                self.setUpColors(json.colors);
                self.phases = json.game_phases;
                self.scenarios.add(json.scenarios);
                self.columns_in_each_phase = json.columns_in_each_phase;
                self.setUpPhases();
                self.adjustRows();
                self.render();
            }
        });
    },

    setUpColors: function(colors) {
        var self = this;
        self.colors = { colors: colors };
        self.columns.each(function(a) {
            var box_models = a.get('boxModels');
            for (var i=0;i<box_models.length;i++)  {
                box_models[i].set({colors: colors, color_int: -1});
                box_models[i].trigger('nextColor');
            }
        });
    },

    addARow: function() {
        var self = this;
        self.current_number_of_rows = self.current_number_of_rows + 1;
        self.adjustRows();
        if (self.current_number_of_rows === LogicModel.NUMBER_OF_ROWS_TOTAL) {
            jQuery('.add_a_row_button').hide();
        }
    },

    adjustRows: function() {
        var self = this;
        self.columns.each(function(c) {
            var box_models = c.get('boxModels');
            for (var i=0;i<box_models.length;i++)  {
                if (box_models[i].get('row') <= self.current_number_of_rows) {
                    box_models[i].trigger('showBox');
                }
                else {
                    box_models[i].trigger('hideBox');
                }
            }
        });
    },

    setUpPhases: function() {
        var self = this;
        self.current_phase = 0;
        for (var i=1; i < self.phases.length; i++) {
            var phasestep = 'step' + i;
            jQuery('<div/>', {
                class: 'step ' + phasestep,
            }).append(jQuery('<span/>', {
                text: 'Step '+ i
            })).appendTo('.activity-progress');
        }
    },

    currentPhaseInfo: function() {
        return this.phases[this.current_phase];
    },

    paintPhase: function() {
        var self = this;
        var phase_info = self.currentPhaseInfo();
        var active_columns_for_this_phase =
            self.columns_in_each_phase[phase_info.id];
        self.columns.each(function(col) {
            if (active_columns_for_this_phase !== undefined) {
                var whether_active = (
                    active_columns_for_this_phase.indexOf(col.id) != -1);
                col.set({active: whether_active});
            }
            // default is true, btw.
        });
        self.columns.each(function(a) {a.trigger('turnOnActiveBoxes');});
        // set the #phase_container span so that
        // the CSS can properly paint this phase of the game.
        jQuery('#phase_container').attr('class', phase_info.css_classes);
        jQuery('.logic-model-game-phase-name').html(phase_info.name);
        // Need to break this to be compliant
        jQuery('.logic-model-game-phase-instructions').html(
            phase_info.instructions
        );
        jQuery('#stepHeaderTitle').toggleClass('switch-it switch-it2');

        if (self.current_phase === 0) {
            jQuery('.previous_phase').hide();
            jQuery('li.previous').show();
            jQuery('li.next').show();
            jQuery('.scenario-list-stage').show();
            jQuery('.scenario-step-stage').hide();
            self.ok_to_proceed = true;
        } else {
            jQuery('li.previous').show();
            jQuery('li.next').show();
            jQuery('.previous_phase').show();
            jQuery('.scenario-list-stage').hide();
            jQuery('.scenario-step-stage').show();
        }

        jQuery('.activity-progress .step').removeClass('current');

        var currentstep = '.step' + self.current_phase;
        jQuery(currentstep).addClass('current');

        // unhide the last active donebutton on the page:
        jQuery('.done-button').removeClass('visible');

        // unhide the last active donebutton on the page:
        jQuery('.add_a_row_button').removeClass('visible');
        jQuery('.active_column').first()
            .find('.add_a_row_button').addClass('visible');

        if (self.current_phase !== 0) {
            self.checkEmptyBoxes();
        }

        if (self.current_phase == self.phases.length - 1) {
            jQuery('.show_expert_logic_model_link_div')
                .show()
                .addClass('highlight-answerkey');
        } else {
            jQuery('.show_expert_logic_model_link_div')
                .hide()
                .removeClass('highlight-answerkey');
        }
    },

    showSwitchScenarioWarning: function() {
        jQuery('.help-overlay').show();
        jQuery('.switch-scenario-warning').show();
    },

    goToFirstPhase: function() {
        var self = this;
        self.wipeTableValues();
        self.current_phase = 0;
        self.paintPhase();
        jQuery('.help-overlay').hide();
        jQuery('.switch-scenario-warning').hide();
    },

    cancelSwitchScenario: function() {
        jQuery('.help-overlay').hide();
        jQuery('.switch-scenario-warning').hide();
    },

    goToNextPhase: function() {
        var self = this;
        if (self.ok_to_proceed === false) {
            return;
        }
        self.current_phase = self.current_phase  + 1;
        self.paintPhase();

        var stepTag = $('div[id=\'stepTag\']');
        window.parent.jQuery('body')
            .animate({scrollTop: stepTag.offset().top}, 'slow');
    },

    goToPreviousPhase: function() {
        var self = this;
        jQuery('li.next, h1.section-label-header, li.previous').hide();
        self.current_phase = self.current_phase - 1;
        self.paintPhase();

        var stepTag = $('div[id=\'stepTag\']');
        window.parent.jQuery('body')
            .animate({scrollTop: stepTag.offset().top}, 'slow');
    },

    printScenarioTable: function() {
        window.print();
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

        view.boxes.bind('checkEmptyBoxes', self.checkEmptyBoxes);
        jQuery('div.logic-model-columns').append(view.el);
    },

    onAddScenario: function(scenario) {
        var self = this;
        var view = new LogicModel.ScenarioView({
            model: scenario
        });
        view.LogicModelView = self;
        jQuery('div.logic-model-initial-scenario-list').append(view.el);
        jQuery('.loading-overlay').hide();
    },

    beforeLeavePage: function(event) {
        if (this.current_phase < this.phases.length - 1) {
            if(!confirm('You have not completed the activity. ' +
                'Are you sure you want to leave?')) {
                return false;
            }
        }
        return true;
    }
});
/* global STATIC_URL: true */

LogicModel.Scenario = Backbone.Model.extend({
});

LogicModel.ScenarioCollection = Backbone.Collection.extend({
    model: LogicModel.Scenario
});

LogicModel.ScenarioView = Backbone.View.extend({
    className: 'backbone_scenario_div',
    events: {
        'click .try_this_scenario': 'chooseMe'
    },
    initialize: function(options, render) {
        var self = this;
        self.template = _.template(jQuery('#logic-model-scenario').html());
        var ctx = self.model.toJSON();

        // eslint-disable-next-line no-unsafe-innerhtml/no-unsafe-innerhtml
        self.el.innerHTML = self.template(ctx);
    },
    chooseMe: function() {
        var self = this;
        jQuery('.scenario_instructions').html(self.model.get('instructions'));
        jQuery('.scenario_title_2').html(self.model.get('title'));
        var href = STATIC_URL + 'pdf/' + self.model.get('answer_key');
        jQuery('.show_expert_logic_model_link').attr('href', href);
        jQuery('.scenario-step-stage .accordion-body').css('height','auto');
        self.LogicModelView.goToNextPhase();
    }
});
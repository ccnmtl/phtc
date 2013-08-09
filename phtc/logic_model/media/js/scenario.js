//(function (jQuery) {
LogicModel.Scenario = Backbone.Model.extend({
});

LogicModel.ScenarioCollection = Backbone.Collection.extend({
    model: LogicModel.Scenario
});

LogicModel.ScenarioView = Backbone.View.extend({
    className: "backbone_scenario_div",
    events: {
        'click .try_this_scenario' : 'chooseMe'
    },

    initialize: function (options, render) {
        "use strict";
        var self = this;
        self.template = _.template(jQuery("#logic-model-scenario").html());
        var ctx = self.model.toJSON();
        self.el.innerHTML = self.template(ctx);
    },

    chooseMe : function () {
        "use strict";
        var self = this;
        jQuery ('.scenario_instructions').html (self.model.get ('instructions'));
        jQuery ('.scenario_title_2').html (self.model.get ('title'));
        self.LogicModelView.goToNextPhase();
    }
});
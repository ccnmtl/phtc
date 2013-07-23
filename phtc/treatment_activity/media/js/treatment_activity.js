/*
(function (jQuery) {
*/  
    function trickit() {
       $($('.cirrhosis')[1]).click();
       $($('.treatment-status')[0]).val('0');
       $($('.treatment-status')[0]).trigger('change');
       $($('.drug')[0]).click();
    }

    Backbone.sync = function (method, model, success, error) {
    };
    
    String.prototype.capitalize = function() {
        return this.charAt(0).toUpperCase() + this.slice(1);
    };
    
    var TreatmentStep = Backbone.Model.extend({
        defaults: {
            'minimized': false,
            'decision': undefined,
            'initial': true,
            'statusDescription': ''
        },
        aboutMe: function() {
            return ( "#" + this.get ('id') + " " + this.get ('name') + " " + this.get ('type') + this.get ('decision') );
        },

    });
    
    var TreatmentStepCollection = Backbone.Collection.extend({
        model: TreatmentStep
    });
    
    var TreatmentStepView = Backbone.View.extend({
        events: {
        },
        initialize: function (options, render) {
            console.log ("Initialize TreatmentStepView.");
            var self = this;
            
            _.bindAll(this, "render", "unrender");            
            this.model.bind("destroy", this.unrender);
            this.model.bind("change:minimized", this.render);
            this.template = _.template(jQuery("#treatment-step").html());
            
            this.render();
            
            if (self.model.get('last')) {
                setTimeout(function() {
                    var eltStep = jQuery(self.el).find("div.treatment-step");
                    jQuery('html, body').animate({
                        scrollTop: jQuery(eltStep).position().top
                    }, 300);
                    self.model.set('last', false);
                }, 0);
            }
        },
        render: function () {
            console.log ("render TreatmentStepView.");
            var eltStep = jQuery(this.el).find("div.treatment-step");            
            var ctx = this.model.toJSON();
            this.el.innerHTML = this.template(ctx);
        },
        unrender: function () {
            console.log ("unrender TreatmentStepView.");
            jQuery(this.el).fadeOut('fast', function() {
                jQuery(this.el).remove();
            });            
        }
    });
        
    var ActivityState = Backbone.Model.extend({
        defaults: {
            path: '',
            node: '',
            cirrhosis: undefined,
            status: undefined,
            drug: undefined
        },
        statusDescription: function() {
            return '';
        },
        toTemplate: function() {
            console.log ("toTemplate  ActivityState.");
            var ctx = _(this.attributes).clone();
            ctx.patient_factors_complete =
                this.get('cirrhosis') !== undefined &&
                this.get('status') !== undefined &&
                this.get('drug') !== undefined;
            ctx.statusDescription = this.statusDescription();
            return ctx;

        },
        getNextUrl: function() {
            console.log ("getNextUrl  ActivityState.");
            var url = '/_rgt/';
            if (this.get('path')) {
                url += this.get('path') + '/' + this.get('node') + '/';
            }
            return url;  
        },        
        reset: function() {
            console.log ("reset  ActivityState.");
            this.set('path', '');
            this.set('node', '');
        }
    });

    window.TreatmentActivityView = Backbone.View.extend({
        events: {
            "click .reset-state": "onResetState",
            "click .decision-point-button": "onDecisionPoint",
            "click .choose-again": "onChooseAgain",
            "click i.icon-question-sign": "onHelp",
            "click .choose-cirrhosis-again": "onResetState",
            "click .run_test": "onRunTest"            
        },
        initialize: function(options) {
            console.log ('initialize TreatmentActivityView')

            _.bindAll(this,
                "render",
                "onResetState",
                "onDecisionPoint",
                "onChooseAgain",
                "onAddStep",
                "onRemoveStep",
                "onHelp",
                "onRunTest"
            );
            
            this.activityState = new ActivityState();
            this.activityState.reset();
            this.activityState.bind("change", this.render);
            
            this.treatmentSteps = new TreatmentStepCollection();
            this.treatmentSteps.bind("add", this.onAddStep);
            this.treatmentSteps.bind("remove", this.onRemoveStep);
            
            //this.patientFactorsTemplate =
            //   _.template(jQuery("#patient-factors").html()); 
            this.next();
            this.render();
        },
        render: function() {

            console.log ('render TreatmentActivityView')
            var self = this;
            var templateIdx = this.activityState.get('template');
            var context = this.activityState.toTemplate();
            jQuery("div.treatment-activity-view, div.treatment-steps, div.factors-choice").fadeIn("fast");
            console.log ("done rendering...");
        },
        next: function() {
            console.log ('next TreatmentActivityView')
            var self = this;
            
            jQuery.ajax({
                type: 'POST',
                url: self.activityState.getNextUrl(),
                data: {
                    'state': JSON.stringify(this.activityState.toJSON()),
                    'steps': JSON.stringify(this.treatmentSteps.toJSON())
                },
                dataType: 'json',
                error: function () {
                    alert('There was an error.');
                },
                success: function (json, textStatus, xhr) {
                    self.activityState.set({'template': 1,
                                            'path': json.path,
                                            'node': json.node});
                    
                    // Minimize steps 0 - n-1
                    var week = 0;
                    
                    self.treatmentSteps.forEach(function(step, idx) {
                         week += step.get('duration');
                         step.set('minimized', true);                
                    });
                    
                    // Appear the new treatment steps
                    var ts;
                    for (var i = 0; i < json.steps.length; i++) {
                        var opts = json.steps[i];
                        opts.can_edit = json.can_edit;
                        
                        ts = new TreatmentStep(opts);
                        ts.set('week', week);
                        ts.set('last', i === (json.steps.length - 1));
                        self.treatmentSteps.add(ts);
                        week += ts.get('duration');
                    }
                }
            });
        },
        onAddStep: function(step) {
            console.log ('onAddStep TreatmentActivityView')
            var view = new TreatmentStepView({
                model: step,
                parentView: this
            });
            jQuery("div.treatment-steps").append(view.el);
        },
        onRemoveStep: function(step) {
            console.log ('onRemoveStep TreatmentActivityView')
            step.destroy();
        },
        onResetState: function(evt) {
            console.log ('STARTING onResetState TreatmentActivityView')
            var self = this;
            var srcElement = evt.srcElement || evt.target || evt.originalTarget;
            jQuery(srcElement).button("loading");

            /*
            while ((model = self.treatmentSteps.first()) !== undefined) {
                console.log (self.treatmentSteps.length)
                model.destroy();
            }
            */
            
            console.log ("testing")
            decision_points = []
            self.treatmentSteps.forEach(function(step, idx) {
                 console.log (step.aboutMe());
                 console.log (step.get('type'));
                 if (step.get('type') == 'DP') {
                    decision_points.push (step.get ('id'));
                 }
                 
            });
            console.log (decision_points);
            console.log ("done testing")
            while (self.treatmentSteps.last().get('id')!= decision_points[0]) {
                //console.log (self.treatmentSteps.length)
                self.treatmentSteps.last().destroy();
            }
            var new_last_step = self.treatmentSteps.last();
            //self.next();
            self.activityState.set('node', new_last_step.get('id'));

            new_last_step.set({
                "minimized": false,
                "decision": undefined
            });
            this.activityState.set('node', new_last_step);

            //self.next();



            //self.next();
            /*
            self.treatmentSteps.reset();            
            jQuery("div.treatment-steps,div.treatment-activity-view").fadeOut("slow", function() {
                self.activityState.reset();
                //self.treatmentSteps.next();
                //self.next();
            });
            */
            console.log ('DONE WITH onResetState TreatmentActivityView');
            //console.log ("next...");
            //
        },
        onDecisionPoint: function(evt) {
            console.log ('onDecisionPoint TreatmentActivityView')
            var self = this;
            var srcElement = evt.srcElement || evt.target || evt.originalTarget;
            jQuery(srcElement).button("loading");
            var last = this.treatmentSteps.last();
            last.set({'decision': parseInt(jQuery(srcElement).attr('value'), 10)});
            this.activityState.set('node', last.get('id'));
            
            self.next();
        },


        onChooseAgain: function(evt) {
            console.log ('onChooseAgain TreatmentActivityView')
            var srcElement = evt.srcElement || evt.target || evt.originalTarget;
            var rollbackId = jQuery(srcElement).data('id');
            while ((step = this.treatmentSteps.last()) !== undefined) {
                if (step.get('id') === rollbackId) {
                    step.set({
                        "minimized": false,
                        "decision": undefined
                    });
                    this.activityState.set('node', step);
                    return;
                }
                step.destroy();
            }
        },


        onHelp: function(evt) {
            console.log ('onHelp TreatmentActivityView')
            var srcElement = evt.srcElement || evt.target || evt.originalTarget;
            var parent = jQuery(srcElement).parents('div.treatment-step')[0];
            var helpText = jQuery(parent).find('div.treatment-step-help');
            
            jQuery("div.treatment-step-help:visible").not(helpText).hide();
            jQuery(helpText).toggle();
        },
        onRunTest: function(evt) {
            console.log ('onRunTest TreatmentActivityView')
            var self = this;
            self.next();
            console.log ("OK DONE WITH THE TEST")
        }

    });
/*
}(jQuery));    
*/
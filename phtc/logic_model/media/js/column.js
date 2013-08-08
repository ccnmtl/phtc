LogicModel.Column = Backbone.Model.extend({
    what : 'model',
    defaults: {
        active : true
    },
    aboutMe: function() {
    }
});

LogicModel.ColumnCollection = Backbone.Collection.extend({
    model: LogicModel.Column
});

LogicModel.ColumnView = Backbone.View.extend({
    tagName: "span",
    className: "backbone_column_span",
    
    events: {
        "click .column_help_button_span": "showHelpBox"
    },

    initialize: function (options, render) {
        var self = this;
        _.bindAll(self, "render", "unrender",  "addBox", "turnOnActiveBoxes", "showHelpBox");
        self.model.bind("turnOnActiveBoxes", self.turnOnActiveBoxes);
        self.model.set ({boxModels: []});
        self.boxes = new LogicModel.BoxCollection();
        var the_boxes = _.map (_.range(1, LogicModel.NUMBER_OF_ROWS_TOTAL + 1), function (num) {
                return {
                    'row': num,
                    'name':num.toString(),
                    'column' : self.model
                };
            }
        );
        self.boxes.add (the_boxes);
        self.template = _.template(jQuery("#logic-model-column").html());

        var ctx = self.model.toJSON();
        self.el.innerHTML = self.template(ctx);
        //self.current_number_of_rows = LogicModel.NUMBER_OF_ROWS_INITIALLY_VISIBLE;


        self.render();
    

    },

    showHelpBox: function () {
        var self = this;
        var the_template = jQuery('#logic-model-help-box').html();
        var examples_copy = self.model.get ('help_examples'  );
        if (examples_copy === '' || examples_copy == undefined ) {
            examples_copy = 'Lorem ipsum';
        }
        var definition_copy = self.model.get ('help_definition'  );
        if (definition_copy === '' || definition_copy === undefined ) {
            definition_copy = 'Lorem ipsum';
        }
        var the_data = {
            'help_title'  : definition_copy,
            'help_body': examples_copy
        };
        var the_html = _.template(the_template, the_data);
        jQuery( ".help_box" ).html (the_html);
        jQuery( ".help_box" ).show();
    },

    turnOnActiveBoxes: function() {
        // Make boxes in active columns editable and draggable, and turn off the others.
        var self = this;
        if (self.model.get ('active')) {
            self.boxes.each (function (b) { b.trigger ('makeActive'); });
            jQuery (this.el).addClass ('active_column');
        } else {
            self.boxes.each (function (b) { b.trigger ('makeInactive'); });
            jQuery (this.el).removeClass ('active_column');
        } 
        // test all boxes for draggableness.
        self.boxes.each (function (b) { b.trigger ('render'); });
    },

    addBox: function(box) {

        var self = this;        
        var view = new LogicModel.BoxView({
            model: box
        });

        jQuery(self.el).find('.boxes').append(view.el);
        view.parentView = self;
        view.$el.addClass ('hidden_box');
        var tmp = self.model.get('boxModels');
        tmp.push (view.model);
        self.model.set ({'boxModels' : tmp});
    },

    adjustNumberOfVisibleBoxes: function () {
        console.log (parentView.current_number_of_rows);
    },

    render: function () {
        var self = this;
        self.boxes.each(self.addBox);
        return this;
    },
    unrender: function () {
        jQuery(this.el).fadeOut('fast', function() {
            jQuery(this.el).remove();
        });            
    },
});
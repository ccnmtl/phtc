LogicModel.findBox = function (el) {
    return jQuery (el).closest('.backbone_box_div').data('view');
}

LogicModel.Box = Backbone.Model.extend({
    defaults: {
        "contents":  "",
        'active': true
    },
    aboutMe: function() {
    },
});

LogicModel.BoxCollection = Backbone.Collection.extend({
    model: LogicModel.Box
});

LogicModel.BoxView = Backbone.View.extend({
    className: "backbone_box_div",
    events: {
        'change textarea' : 'onBoxEdited',
        'click .switch_color' : 'nextColor'
    },
    initialize: function (options, render) {
        var self = this;
        _.bindAll(self,
            "render",
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
            "turnOffDraggable",
            "startDrag",
            "showBox",
            "hideBox",
            "onBoxEdited"
        );

        self.model.bind("destroy", self.unrender);
        self.model.bind("makeActive", self.makeActive);
        self.model.bind("makeInactive", self.makeInactive);
        self.model.bind("nextColor", self.nextColor)
        self.model.bind("showBox", self.showBox);
        self.model.bind("render", self.render);
        self.model.bind("onBoxEdited", self.onBoxEdited);
        
        self.template = _.template(jQuery("#logic-model-box").html());
        var ctx = self.model.toJSON();
        self.el.innerHTML = self.template(ctx);
        self.setUpDraggable();
        self.setUpDroppable();
        self.render();

        // sorry, but we need to do this for the draggy-droppy stuff.
        self.$el.data('view', this);
    },


    showBox: function() {
        var self = this;
        var jel = self.$el;
        jel.removeClass('hidden_box');
    },


    hideBox: function() {
        var self = this;
        var jel = self.$el;
        jel.addClass('hidden_box');
    },


    turnOnDraggable: function() {
        var self = this;
        var jel = self.$el;
        jel.find ('.box_droppable').droppable( "disable" );
        jel.find ('.box_draggable').draggable( "enable" );
        jel.find ('.box_handle').show();
    },

    turnOffDraggable: function () {
        var self = this;
        var jel = self.$el;
        var the_droppable = jel.find ('.box_droppable');
        the_droppable.droppable( "enable" );
        jel.find ('.box_draggable').draggable( "disable");
        jel.find ('.box_handle').hide();
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
        //self.model.trigger('onBoxEdited');
    },

    draggedTo: function() {
        var self = this;
        var jel = self.$el;
        jel.find (".placeholder").remove();
        jel.find (".box_handle").show();
        jel.find ('.box_droppable').droppable( "disable" );
        jel.find ('.box_draggable').draggable( "enable" );
        //self.model.trigger('onBoxEdited');
    },

    onDrop: function (event, ui) {
        var self = this;
        var src_box = LogicModel.findBox(ui.draggable.context);
        var dst_box = LogicModel.findBox(event.target);
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


        dst_box.model.trigger ('onBoxEdited');
        src_box.model.trigger ('onBoxEdited');
    },

    setUpDroppable: function (){
        var self = this;
        var droppable_options = {
            accept: ".box_draggable" ,
            /* activeClass: "active_droppable", */
            hoverClass: "hover_droppable",
            drop: self.onDrop,
            //activate: self.render,
            activate: self.startDrag,
            tolerance: 'pointer'
        };
        jQuery (this.el).find ('.box_droppable').droppable(droppable_options);

    },

    startDrag: function(event, ui) {
        var self = this;
        ui.helper.css('z-index', 100);
        self.render();
    },

    hasText: function() {
        var self = this;
        if (jQuery (self.el).find('.text_box').val().length > 0) {
            return true;
        }
        return false;
    },

    setColor: function () {
        var self = this;
        var the_colors = self.model.get ('colors');
        var color_int  = self.model.get ('color_int');
        var color =  '#' + (the_colors[color_int % the_colors.length]);
        //jQuery(self.el).find ('.cell').css('background-color', color);
        //jQuery(self.el).find ('.text_box').css('background-color', color);


        jQuery(self.el).find ('.text_box').css('color', color);
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
            cursor: 'move'
        };
        jQuery (this.el).find ('.box_draggable').draggable(draggable_options);
    },

    onBoxEdited: function () {
        var self = this;
        self.model.set ({'contents': self.$el.find ('.text_box').val()});
        self.model.trigger('checkEmptyBoxes')
        self.render();
        
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
                } else {
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
    }
});

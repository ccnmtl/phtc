jQuery(document).ready(function(){ 
	// This is the text for the Code and Scenario labels
	var scenario_label  = "List of Data Collection Methods";
	var code_label = "Evaluation Questions"
	jQuery('#codes').prev().text(scenario_label); 
	jQuery('#header-table td.code-label h5').text(code_label);
})
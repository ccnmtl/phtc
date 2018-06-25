APP=phtc
JS_FILES=media/js/dashboard.js \
	media/js/checkbox_activity media/js/data_collection_methods.js \
	media/js/design-notation.js media/js/edit_profile.js \
	media/js/feedback.js media/js/matching.js \
	media/js/modalpage.js media/js/nylearns_test_user.js \
	media/js/phtc_chart.js media/js/post_test.js \
	media/js/profile.js media/js/quizshow.js media/js/reading_exercise.js \
	media/js/registration.js media/js/required_answers.js \
	media/js/special_question.js phtc/logic_model/media/js
MAX_COMPLEXITY=7
PY_DIRS=phtc quizblock

all: jenkins

include *.mk


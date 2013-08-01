--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET search_path = public, pg_catalog;

--
-- Data for Name: logic_model_column; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO logic_model_column (id, name, order_rank, css_classes, help_definition, help_examples, flavor) VALUES (3, 'inputs', 1, 'inputs', '', '', 'first');
INSERT INTO logic_model_column (id, name, order_rank, css_classes, help_definition, help_examples, flavor) VALUES (4, 'activities', 2, 'activities', '', '', 'middle');
INSERT INTO logic_model_column (id, name, order_rank, css_classes, help_definition, help_examples, flavor) VALUES (5, 'outputs', 3, 'outputs', '', '', 'middle');
INSERT INTO logic_model_column (id, name, order_rank, css_classes, help_definition, help_examples, flavor) VALUES (6, 'short-term outcomes', 4, 'short_term_outcomes', '', '', 'middle');
INSERT INTO logic_model_column (id, name, order_rank, css_classes, help_definition, help_examples, flavor) VALUES (7, 'intermediate outcomes', 5, 'intermediate_outcomes', '', '', 'middle');
INSERT INTO logic_model_column (id, name, order_rank, css_classes, help_definition, help_examples, flavor) VALUES (8, 'long-term outcomes', 6, 'long_term_outcomes', '', '', 'end');


--
-- Data for Name: logic_model_gamephase; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO logic_model_gamephase (id, name, instructions, order_rank, css_classes) VALUES (1, 'Pick a scenario!', 'Choose a nice scenario.', 1, 'pick_scenario');
INSERT INTO logic_model_gamephase (id, name, instructions, order_rank, css_classes) VALUES (6, 'Conclusion', 'Now you can print, view the final results, and/or move on to the post-test', 6, 'conclusion');
INSERT INTO logic_model_gamephase (id, name, instructions, order_rank, css_classes) VALUES (3, 'Add Long-Term Outcomes', 'Now add the long-term outcomes.
', 3, 'add_long_term_outcomes');
INSERT INTO logic_model_gamephase (id, name, instructions, order_rank, css_classes) VALUES (5, 'Finish', 'Now finish your work.', 5, 'finish_work');
INSERT INTO logic_model_gamephase (id, name, instructions, order_rank, css_classes) VALUES (2, 'Add Inputs', 'Now add the inputs.', 2, 'add_inputs');
INSERT INTO logic_model_gamephase (id, name, instructions, order_rank, css_classes) VALUES (4, 'Add Intermediate columns', '... And the intermediate columns.', 4, 'add_intermediate_columns');


--
-- Data for Name: logic_model_activephase; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO logic_model_activephase (id, game_phase_id, column_id) VALUES (1, 2, 3);
INSERT INTO logic_model_activephase (id, game_phase_id, column_id) VALUES (2, 3, 8);
INSERT INTO logic_model_activephase (id, game_phase_id, column_id) VALUES (3, 4, 4);
INSERT INTO logic_model_activephase (id, game_phase_id, column_id) VALUES (4, 4, 5);
INSERT INTO logic_model_activephase (id, game_phase_id, column_id) VALUES (5, 4, 7);
INSERT INTO logic_model_activephase (id, game_phase_id, column_id) VALUES (6, 4, 6);
INSERT INTO logic_model_activephase (id, game_phase_id, column_id) VALUES (7, 5, 3);
INSERT INTO logic_model_activephase (id, game_phase_id, column_id) VALUES (8, 5, 4);
INSERT INTO logic_model_activephase (id, game_phase_id, column_id) VALUES (9, 5, 5);
INSERT INTO logic_model_activephase (id, game_phase_id, column_id) VALUES (10, 5, 6);
INSERT INTO logic_model_activephase (id, game_phase_id, column_id) VALUES (11, 5, 7);
INSERT INTO logic_model_activephase (id, game_phase_id, column_id) VALUES (12, 5, 8);


--
-- Name: logic_model_activephase_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('logic_model_activephase_id_seq', 12, true);


--
-- Data for Name: logic_model_boxcolor; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO logic_model_boxcolor (id, name, color, order_rank) VALUES (2, 'Red', 'E40045', 2);
INSERT INTO logic_model_boxcolor (id, name, color, order_rank) VALUES (3, 'Green', '61D7A4', 3);
INSERT INTO logic_model_boxcolor (id, name, color, order_rank) VALUES (5, 'Light Green', 'E3FB71', 4);
INSERT INTO logic_model_boxcolor (id, name, color, order_rank) VALUES (1, 'Olive', 'A1B92E', 5);
INSERT INTO logic_model_boxcolor (id, name, color, order_rank) VALUES (6, 'Purple', 'AB2B52', 6);
INSERT INTO logic_model_boxcolor (id, name, color, order_rank) VALUES (4, 'Yellow', 'FFE173', 1);


--
-- Name: logic_model_boxcolor_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('logic_model_boxcolor_id_seq', 6, true);


--
-- Name: logic_model_column_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('logic_model_column_id_seq', 8, true);


--
-- Name: logic_model_gamephase_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('logic_model_gamephase_id_seq', 6, true);


--
-- Data for Name: logic_model_scenario; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO logic_model_scenario (id, title, order_rank, instructions, difficulty) VALUES (1, 'U.S. Outlines N.S.A.’s Culling of Data for All Domestic Calls', 1, 'The declassified papers included an order requiring a Verizon subsidiary to turn over its customers’ phone logs. A separate document, published in The Guardian, described a program to access massive amounts of Web-browsing activity.', 'Easy');
INSERT INTO logic_model_scenario (id, title, order_rank, instructions, difficulty) VALUES (2, 'Egypt Orders Breakup of Pro-Morsi Camps', 2, 'Security forces were told to disperse supporters of the ousted leader, Mohamed Morsi, who have been occupying two large squares in Cairo, risking new violence.', 'Medium');
INSERT INTO logic_model_scenario (id, title, order_rank, instructions, difficulty) VALUES (3, 'Weighing Pick for Fed Chief, Obama Defends Summers', 3, 'President Obama said Lawrence H. Summers had been maligned in the liberal news media, while emphasizing that no choice had been made on the next leader of the central bank.', 'Hard');


--
-- Name: logic_model_scenario_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('logic_model_scenario_id_seq', 3, true);


--
-- PostgreSQL database dump complete
--


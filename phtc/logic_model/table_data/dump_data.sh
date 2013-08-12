pg_dump -U pusher \
--column-inserts \
--data-only \
--no-owner \
--table=logic_model_scenario \
--table=logic_model_gamephase  \
--table=logic_model_column  \
--table=logic_model_activephase \
--table=logic_model_boxcolor \
phtc

import json
from django.http import HttpResponse
from phtc.logic_model.models import Column, Scenario, GamePhase
from phtc.logic_model.models import ActivePhase, BoxColor


def settings(request):

    columns_in_each_phase = {}
    for ap in ActivePhase.objects.all():
        if ap.game_phase_id in columns_in_each_phase:
            columns_in_each_phase[ap.game_phase.id].append(ap.column.id)
        else:
            columns_in_each_phase[ap.game_phase.id] = [ap.column.id]

    the_settings = {
        'colors': [c.color for c in BoxColor.objects.all()],
        'columns': [c.to_json() for c in Column.objects.all()],
        'scenarios': [s.to_json() for s in Scenario.objects.all()],
        'game_phases': [g.to_json() for g in GamePhase.objects.all()],
        'columns_in_each_phase': columns_in_each_phase
    }

    return HttpResponse(
        json.dumps(the_settings, indent=2),
        content_type="application/json")

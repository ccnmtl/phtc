from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from phtc.logic_model.models import Column, Scenario, GamePhase
import simplejson

@login_required
def settings(request):
    """ get the columns out to the front end."""
    #if not request.is_ajax() or request.method != "POST":
    #    return HttpResponseForbidden()

    columns =     [c.to_json() for c in Column.objects.all()]
    scenarios =   [s.to_json() for s in Scenario.objects.all()]
    game_phases = [g.to_json() for g in GamePhase.objects.all()]

    the_settings = {
        'columns': columns,
        'scenarios': scenarios,
        'game_phases': game_phases
    }

    return HttpResponse(simplejson.dumps(the_settings, indent=2),  mimetype="application/json")

# i don't think we actually need any other views here...
if 1 == 0:
    @login_required
    def get_next_steps(request, path_id, node_id):
        if not request.is_ajax():
            return HttpResponseForbidden()
        node = TreatmentNode.objects.get(id=node_id)

        next_steps = []
        prev = None
        if node.type == 'DP':
            steps = simplejson.loads(request.POST.get('steps'))
            decision = steps[len(steps) - 1]['decision']
            node = node.get_children()[decision - 1]
            next_steps.append(node.to_json())
            prev = node

        for node in node.get_descendants():
            if prev and prev.type == 'DP':
                break
            else:
                next_steps.append(node.to_json())
                prev = node

        data = {'steps': next_steps,
                'node': prev.id,
                'path': path_id,
                'can_edit': request.user.is_superuser}

        return HttpResponse(simplejson.dumps(data, indent=2),
                            mimetype="application/json")


    @login_required
    def choose_treatment_path(request):
        """ This will soon be obsolete."""
        if not request.is_ajax() or request.method != "POST":
            return HttpResponseForbidden()
        path = TreatmentPath.objects.all()[0]
        return get_next_steps(request, path.id, path.tree.id)


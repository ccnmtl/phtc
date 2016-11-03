import json
from django.http import HttpResponse, HttpResponseForbidden
from phtc.treatment_activity.models import TreatmentPath, TreatmentNode


def get_next_steps(request, path_id, node_id):
    if not request.is_ajax():
        return HttpResponseForbidden()
    node = TreatmentNode.objects.get(id=node_id)

    next_steps = []
    prev = None
    if node.type == 'DP':
        steps = json.loads(request.POST.get('steps'))
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

    return HttpResponse(json.dumps(data, indent=2),
                        content_type="application/json")


def choose_treatment_path(request):
    """ This will soon be obsolete."""
    if not request.is_ajax() or request.method != "POST":
        return HttpResponseForbidden()
    path = TreatmentPath.objects.all()[0]
    return get_next_steps(request, path.id, path.tree.id)

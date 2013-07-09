from django.core.management.base import BaseCommand
from xml.dom import minidom
from optparse import make_option
from nynjaetc.treatment_activity.models import TreatmentNode, NODE_CHOICES
from nynjaetc.treatment_activity.models import TreatmentPath


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--file',
                    dest='file',
                    help='.xml file defining treatment paths'),
    )

    choices = dict(NODE_CHOICES)

    def add_children(self, childNodes, parent):
        for node in childNodes:
            if node.nodeType == node.TEXT_NODE:
                continue

            label = node.attributes.getNamedItem('Label')
            child = parent.add_child(
                name=label.nodeValue,
                type=self.get_activity_type(node))

            duration = node.attributes.getNamedItem('Duration')
            if duration:
                child.duration = duration.nodeValue

            value = node.attributes.getNamedItem('Value')
            if value:
                child.value = value.nodeValue

            text = node.attributes.getNamedItem('Text')
            if text:
                child.text = text.nodeValue

            help_text = node.attributes.getNamedItem('Help')
            if help_text:
                child.help = help_text.nodeValue

            child.save()

            if node.hasChildNodes():
                self.add_children(node.childNodes, child)

    def get_activity_type(self, node):
        node_type = node.attributes.getNamedItem('Type').nodeValue
        for key, value in self.choices.items():
            if node_type == value:
                return key
        return ''

    def get_nodes_by_name(self, parent, name):
        a = []
        for node in parent.childNodes:
            if node.nodeName == name:
                a.append(node)
        return a

    def handle(self, *args, **options):
        args = """Usage: ./manage.py import_treatment_paths --file filename"""

        if len(options) < 1:
            print args
            return

        xmldoc = minidom.parse(options.get('file'))

        root_nodes = xmldoc.getElementsByTagName('TreatmentNodes')
        for r in root_nodes:
            node = self.get_nodes_by_name(r, 'TreatmentNode')[0]
            label = node.attributes.getNamedItem('Label').nodeValue

            try:
                root = TreatmentNode.objects.get(name=label,
                                                 type='RT')
            except TreatmentNode.DoesNotExist:
                root = TreatmentNode.add_root(
                    name=label,
                    type=self.get_activity_type(node))

            self.add_children(node.childNodes, root)

        paths = xmldoc.getElementsByTagName('TreatmentPath')
        if len(paths) > 0:
            TreatmentPath.objects.all().delete()
            for p in paths:
                new_path = TreatmentPath()
                fields = self.get_nodes_by_name(p, 'field')
                for f in fields:
                    name = f.attributes.getNamedItem('name').nodeValue
                    value = f.childNodes[0].nodeValue
                    if name == 'tree':
                        value = TreatmentNode.objects.get(name=value)
                    elif name == 'cirrhosis':
                        value = value == 'True'
                    new_path.__setattr__(name, value)
                new_path.save()

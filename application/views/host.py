"""
Host Model View
"""
# pylint: disable=too-few-public-methods
from flask_login import current_user
from flask_admin.actions import action
from flask import flash
from flask import Markup
from flask_admin.contrib.mongoengine.filters import BaseMongoEngineFilter
from application.views.default import DefaultModelView
from application.models.host import Host


class FilterLabelValue(BaseMongoEngineFilter):
    """
    Filter for Label Value
    """

    def apply(self, query, value):
        return query.filter(labels__value__icontains=value)

    def operation(self):
        return "contains"

class FilterLabelKey(BaseMongoEngineFilter):
    """
    Filter for Label Key
    """

    def apply(self, query, value):
        return query.filter(labels__key=value)

    def operation(self):
        return "contains"

class HostModelView(DefaultModelView):
    """
    Host Model
    """
    can_edit = False
    can_view_details = True
    column_details_list = [
        'hostname', 'labels', 'log',
        'last_seen', 'source_account_name'
    ]
    column_filters = (
       'hostname',
       'source_account_name',
       'available',
       FilterLabelKey(
        Host,
        "Label Key"
       ),
       FilterLabelValue(
        Host,
        "Label Value"
       ),
    )


    def format_log(v, c, m, p):
        """ Format Log view"""
        html = "<ul>"
        for entry in m.log:
            html+=f"<li>{entry}</li>"
        html += "</ul>"
        return Markup(html)

    def format_labels(v, c, m, p):
        """ Format Log view"""
        html = "<table>"
        for entry in m.labels:
            html += f"<tr><th>{entry.key}</th><td>{entry.value}</td></tr>"
        html += "</table>"
        return Markup(html)


    column_formatters = {
        'log': format_log,
        'labels': format_labels,
    }

    column_exclude_list = (
        'source_account_id',
        'log'
    )

    column_editable_list = (
        'force_update',
    )


    @action('force_update', 'Force Update')
    def action_update(self, ids):
        """
        Set force Update Attribute
        """
        for host_id in ids:
            host = Host.objects.get(id=host_id)
            host.force_update = True
            host.save()
        flash("Updated {} hosts".format(len(ids)))
        return self.index_view()

    def is_accessible(self):
        """ Overwrite """
        return current_user.is_authenticated and current_user.has_right('host')

"""
Rule
"""
# pylint: disable=no-member, too-few-public-methods
from application import db


rule_types = [
    ('all', "All conditions must match"),
    ('any', "Any condition can match"),
    ('anyway', "Match without any condition"),
]

condition_types = [
    ('equal', "Equal"),
    ('in', "Contains"),
    ('ewith', "Endswith"),
    ('swith', "Startswith"),
]

action_outcome_types = [
    ("move_folder", "Move Host to given Folder"),
    ("source_folder", "Add this Folder as basefolder before the specifed in 'Move host to given Folder'"),
    ("ignore", "Ignore this host"),
]


host_params_types = [
    ('ignore_hosts', "Ignore matching Hosts"),
    ('add_custom_label', "Add Custom Label (use name and value)"),
]


class ActionCondition(db.EmbeddedDocument):
    """
    Condition
    """
    match_type = db.StringField(choices=[('host', "Match for Hostname"),('tag', "Match for Tag")])

    hostname_match = db.StringField(choices=condition_types)
    hostname_match_negate = db.BooleanField()
    hostname = db.StringField()

    tag_match = db.StringField(choices=condition_types)
    tag_match_negate = db.BooleanField()
    tag = db.StringField()

    value_match = db.StringField(choices=condition_types)
    value_match_negate = db.BooleanField()
    value = db.StringField()
    meta = {
        'strict': False,
    }

class ActionOutcome(db.EmbeddedDocument):
    """
    Outcome
    """
    type = db.StringField(choices=action_outcome_types)
    param = db.StringField()

class ActionRule(db.Document):
    """
    Rule to control Actions based on labels
    """

    name = db.StringField(required=True, unique=True)
    condition_typ = db.StringField(choices=rule_types)
    conditions = db.ListField(db.EmbeddedDocumentField(ActionCondition))
    outcome = db.ListField(db.EmbeddedDocumentField(ActionOutcome))
    last_match = db.BooleanField(default=False)
    enabled = db.BooleanField()
    sort_field = db.IntField()

    meta = {
        'strict': False,
    }

label_outcome_types = [
    ('add', 'Add matching Labels'),
    ('remove', 'Dismiss matching Labels'),
    ('strip', 'Strip Spaces End/Begin'),
    ('lower', 'Make label lowercase'),
    ('replace', 'Replace whitespaces with _'),
]

class LabelCondition(db.EmbeddedDocument):
    """
    Condition
    """
    match_negate = db.BooleanField()
    match = db.StringField(choices=condition_types)
    match_on = db.StringField(choices=[('label_name', 'Label Name'),
                                       ('label_value', 'Label Value')])
    value = db.StringField(required=True)
    meta = {
        'strict': False,
    }


class LabelRule(db.Document):
    """
    Rule to filter Labels
    """
    name = db.StringField(required=True, unique=True)
    conditions = db.ListField(db.EmbeddedDocumentField(LabelCondition))
    outcome = db.ListField(db.StringField(choices=label_outcome_types))
    enabled = db.BooleanField()
    sort_field = db.IntField()

class HostCondition(db.EmbeddedDocument):
    """
    Host Condition
    """
    match_negate = db.BooleanField()
    match = db.StringField(choices=condition_types)
    hostname = db.StringField(required=True)
    meta = {
        'strict': False,
    }

class HostParams(db.EmbeddedDocument):
    """
    Custom Params
    """
    type = db.StringField(choices=host_params_types)
    name = db.StringField()
    value = db.StringField()
    meta = {
        'strict': False
    }


class HostRule(db.Document):
    """
    Host Rule to add custom Parameters for importers or exporters
    """
    name = db.StringField(required=True, unique=True)
    conditions = db.ListField(db.EmbeddedDocumentField(HostCondition))
    params = db.ListField(db.EmbeddedDocumentField(HostParams))
    enabled = db.BooleanField()
    target = db.StringField(choices=[('import', 'Import'),('export', 'Export')])
    sort_field = db.IntField()
    meta = {
        'strict': False
    }

from django import template


register = template.Library()


@register.tag
def get_relation_by_type_list(parser, token):
    """Gets list of relations from object identified by a content type.

    Syntax::

        {% get_relation_list [content_type_app_label.content_type_model] for [object] as [varname] [direction] %}
    """
    tokens = token.contents.split()
    if len(tokens) not in (6, 7):
        raise template.TemplateSyntaxError(
            "%r tag requires 6 arguments" % tokens[0]
        )

    if tokens[2] != 'for':
        raise template.TemplateSyntaxError(
            "Third argument in %r tag must be 'for'" % tokens[0]
        )

    if tokens[4] != 'as':
        raise template.TemplateSyntaxError(
            "Fifth argument in %r tag must be 'as'" % tokens[0]
        )

    direction = 'forward'
    if len(tokens) == 7:
        direction = tokens[6]

    return RelationByTypeListNode(
        name=tokens[1], obj=tokens[3], as_var=tokens[5], direction=direction
    )


class RelationByTypeListNode(template.Node):

    def __init__(self, name, obj, as_var, direction='forward'):
        self.name = template.Variable(name)
        self.obj = template.Variable(obj)
        self.as_var = template.Variable(as_var)
        self.direction = template.Variable(direction)

    def render(self, context):
        name = self.name.resolve(context)
        content_type_app_label, content_type_model = name.split('.')
        obj = self.obj.resolve(context)
        as_var = self.as_var.resolve(context)
        try:
            direction = self.direction.resolve(context)
        except template.VariableDoesNotExist:
            direction = 'forward'
        #import pdb;pdb.set_trace()
        context[as_var] = obj.get_permitted_related_items(direction=direction).filter(
            content_type__app_label=content_type_app_label, 
            content_type__model=content_type_model
        )
        return ''

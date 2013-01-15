from jmbo.models import ModelBase
from jmbo.view_modifiers.items import GetItem


class CategoryRelatedItem(GetItem):

    def modify(self, view):
        category = self.request.GET.get(self.get['name'], 'all')
        obj = ModelBase.permitted.get(slug=view.params['slug'])
        qs = obj.get_permitted_related_items(direction='both')
        if category != 'all':
            qs = qs.filter(primary_category__slug=category)
        view.params['extra_context']['related_items'] = qs
        return view

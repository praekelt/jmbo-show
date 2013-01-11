from jmbo.view_modifiers.items import GetItem


class CategoryItem(GetItem):

    def modify(self, view):
        category = self.request.GET.get(self.get['name'], 'all')
        if category != 'all':
            qs = view.params['queryset']
            qs = qs.filter(primary_category__slug=category)
            view.params['queryset'] = qs
        return view

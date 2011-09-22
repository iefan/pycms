#encoding=utf-8
import web
from admin.util import render, admin_login_required
from blog.dbutil import get_category, get_categories, category_tree, category_tree2, get_templates, save_category, del_category
from admin.form import category_form


class index:
    @admin_login_required
    def GET(self):
        categories = category_tree()
        req = web.ctx.req
        req.update({
            'categories': categories,
            })
        return render.category_index(**req)

class add:
    @admin_login_required
    def GET(self):
        form = category_form()
        templates = get_templates()
        categories = category_tree()
        parent_id = web.input(parent_id=None).parent_id
        form.parent_id.set_value(parent_id)
        req = web.ctx.req
        req.update({
            'form': form,
            'templates': templates,
            'categories': categories,
            })
        return render.category_edit(**req)

    @admin_login_required
    def POST(self):
        form = category_form()
        if not form.validates():
            templates = get_templates()
            categories = category_tree()
            req = web.ctx.req
            req.update({
                'form': form,
                'templates': templates,
                'categories': categories,
                })
            return render.category_edit(**req)
        save_category(-1, form.d)
        raise web.seeother('/category/index')

class edit:
    @admin_login_required
    def GET(self, id):
        form = category_form()
        category = get_category(id)
        templates = get_templates()
        categories = category_tree()
        form.fill(category)
        req = web.ctx.req
        req.update({
            'form': form,
            'templates': templates,
            'categories': categories,
            })
        return render.category_edit(**req)

    @admin_login_required
    def POST(self, id):
        form = category_form()
        if not form.validates():
            return render.category_edit(form=form)
        save_category(int(id), form.d)
        raise web.seeother('/category/index')

class delete:
    @admin_login_required
    def GET(self, id):
        del_category(id)
        raise web.seeother('/category/index')

class tree:
    def GET(self):
        category_tree_html = category_tree2()
        req = web.ctx.req
        req.update({
            'category_tree_html': category_tree_html,
            })
        return render.category_tree(**req)



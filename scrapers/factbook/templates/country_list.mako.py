from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1236954256.972533
_template_filename='/home/aloha/prog/python/2.6/home/home/templates/country_list.mako'
_template_uri='/country_list.mako'
_template_cache=cache.Cache(__name__, _modified_time)
_source_encoding='utf-8'
from webhelpers.html import escape
_exports = []


def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        g = context.get('g', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        for country in g.factbook.keys():
            # SOURCE LINE 2
            __M_writer(u'  <img src="')
            __M_writer(escape(g.factbook[country]["image"]))
            __M_writer(u'">\n')
        return ''
    finally:
        context.caller_stack._pop_frame()



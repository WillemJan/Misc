from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1236975662.9917779
_template_filename='/home/aloha/prog/python/2.6/home/home/templates/country.mako'
_template_uri='/country.mako'
_template_cache=cache.Cache(__name__, _modified_time)
_source_encoding='utf-8'
from webhelpers.html import escape
_exports = []


def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        g = context.get('g', UNDEFINED)
        int = context.get('int', UNDEFINED)
        chr = context.get('chr', UNDEFINED)
        range = context.get('range', UNDEFINED)
        enumerate = context.get('enumerate', UNDEFINED)
        sorted = context.get('sorted', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        runtime._include_file(context, 'header.html', _template_uri)
        __M_writer(u'\n\n<div id="container1"> \n<font size="10">a</font>\n')
        # SOURCE LINE 5
        for i in range(1,26):
            # SOURCE LINE 6
            __M_writer(u'    ')
            j=(chr(97+int(i))) 
            
            __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin()[__M_key]) for __M_key in ['j'] if __M_key in __M_locals_builtin()]))
            __M_writer(u'\n    ')
            # SOURCE LINE 7
            __M_writer(escape(j))
            __M_writer(u'\n')
        # SOURCE LINE 9
        __M_writer(u'\n')
        # SOURCE LINE 10
        for i, country in enumerate(sorted(g.factbook.keys())):
            # SOURCE LINE 11
            if i<10:
                # SOURCE LINE 12
                __M_writer(u'\n<div id="container"> \n<a href="">\n<img src="')
                # SOURCE LINE 15
                __M_writer(escape(g.factbook[country]["image"]))
                __M_writer(u'"><h4>')
                __M_writer(escape(g.factbook[country]["fullname"]))
                __M_writer(u'</h4> \n</a>\n<p>\nPopulation : \n\n<br>\nSize :<br>\n</p>\n</div>\n\n')
        # SOURCE LINE 27
        __M_writer(u'</div>\n')
        # SOURCE LINE 28
        runtime._include_file(context, 'footer.html', _template_uri)
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()



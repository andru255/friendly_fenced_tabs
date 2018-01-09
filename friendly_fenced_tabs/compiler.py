from .utils import Utils

class Compiler(object):
    def __init__(self, settings, extra_extensions):
        self.settings = settings
        self.extensions = extra_extensions

    def update_settings(self, key, value):
        self.settings[key] = value

    def header_output(self, tab_node, tab_options):
        output = tab_node.copy()
        output['options'] = tab_options
        return output

    def content_output(self, tab_node, tab_options):
        #if exists the codehilite config
        if 'codehilite_config' in self.settings:
            codehilite_config = self.settings['codehilite_config']

            #check exists hl_lines
            hl_lines = []
            value_hl_lines = Utils.get_value_by_key_name(tab_options, 'hl_lines')
            if value_hl_lines:
                hl_lines = value_hl_lines

            #formating with the active class
            css_class = codehilite_config['css_class'][0]
            if tab_node['active_class']:
                css_class = "{} {}".format(
                    codehilite_config['css_class'][0],
                    tab_node['active_class'])

            highlighter = self.extensions['Codehilite'](
                tab_node['code'],
                linenums=codehilite_config['linenums'][0],
                guess_lang=codehilite_config['guess_lang'][0],
                css_class=css_class,
                style=codehilite_config['pygments_style'][0],
                lang=(tab_node['language'] or None),
                noclasses=codehilite_config['noclasses'][0],
                hl_lines=self.extensions['parse_hl_lines'](hl_lines)
            )
            tab_node['code'] = highlighter.hilite()

        output = tab_node.copy()
        output['options'] = tab_options
        return output

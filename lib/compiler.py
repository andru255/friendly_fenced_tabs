class Compiler(object):
    def __init__(self, settings, extra_extensions):
        self.settings = settings
        self.extensions = extra_extensions

    def update_settings(self, key, value):
        self.settings[key] = value

    def header_output(self, tab_config, tab_node):
        #header
        header = self.settings['template_header_item'].format(
            **tab_node
        ) 
        return header

    def content_output(self, tab_config, tab_node):
        template = self.settings['template_content_item']

        #if exists the codehilite config
        if 'codehilite_config' in self.settings:
            codehilite_config = self.settings['codehilite_config']
            highlighter =  self.extensions['Codehilite'](
                tab_node['code'],
                linenums=codehilite_config['linenums'][0],
                guess_lang=codehilite_config['guess_lang'][0],
                css_class=codehilite_config['css_class'][0],
                style=codehilite_config['pygments_style'][0],
                lang=(tab_node['language'] or None),
                noclasses=codehilite_config['noclasses'][0]
            ) 
            tab_node['code'] = highlighter.hilite()
        
        content = template.format(
            **tab_node
        ) 
        return content

    def compile(self, headers, contents):

        html_headers = self.settings['template_header_container'].format(
            headers= headers
        )
        html_contents = self.settings['template_content_container'].format(
            contents= contents
        )

        result = self.settings['template_container'].format(
            template_header=html_headers,
            template_content=html_contents
        )
        return result

    def compile_one_tab(self, tab_config, tab_node):
        result = self.settings['template_block_no_tab'].format(
            **tab_node
        )
        if self.settings['single_block_as_tab']:
            headers = self.header_output(tab_config, tab_node)
            content = self.content_output(tab_config, tab_node)
            result = self.compile(headers, content)
        return result
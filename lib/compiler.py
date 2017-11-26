class Compiler(object):
    def __init__(self, settings):
        self.settings = settings

    def header_output(self, tab_config, tab_node):
        #header
        header = self.settings['template_header_item'].format(
            **tab_node
        ) 
        return header

    def content_output(self, tab_config, tab_node):
        template = self.settings['template_content_item']
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
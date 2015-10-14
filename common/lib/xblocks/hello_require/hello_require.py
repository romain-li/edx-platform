from xblock.core import XBlock
from xblock.fragment import Fragment


class HelloRequireXBlock(XBlock):
    def student_view(self, context):
        fragment = Fragment()

        fragment.add_javascript_url(self.runtime.local_resource_url(self, 'public/js/main.js'))
        fragment.initialize_js('xblock-hello-require/public/js/main', use_require_js=True)

        return fragment

    @staticmethod
    def workbench_scenarios():
        return [
            ("Hello require", """<xblock-hello-require/>""")
        ]

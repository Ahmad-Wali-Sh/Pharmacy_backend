from rest_framework_csv.renderers import CSVRenderer
import codecs

        
class UTF8CSVRenderer(CSVRenderer):
    media_type = 'text/csv'
    format = 'csv'

    def render(self, data, media_type=None, renderer_context=None, writer_opts=None):
        # Add UTF-8 BOM for Excel compatibility
        csv_output = super().render(data, media_type, renderer_context, writer_opts)
        bom = codecs.BOM_UTF8.decode('utf-8')  # Decode BOM to attach it as a string
        return bom + csv_output
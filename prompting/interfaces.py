class PromptStrategy:
    def build(self, html1, html2):
        raise NotImplementedError
    def get_metadata(self):
        return {} 
    def uses_images(self):
        return False

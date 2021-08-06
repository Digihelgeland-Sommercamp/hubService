from classFolder.contacter import Contacter

class UploadAttachment():
    def __init__(self, data):
        self.data = data
        self.contacter = Contacter()

    def upload_attachment(self):
        res = self.contacter.upload_attachment(self.data)
        return res
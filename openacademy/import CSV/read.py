import base64
import csv
import StringIO

class read():

    def __init__(self):
        input_file = fields.Binary("libelle")

    def get_reader(self):
        data = base64.b64decode(self.input_file)
        return csv.reader(StringIO.StringIO(data), delimiter=str(';'))

    @api.one
    def ma_fonction(self):
        reader = self.get_reader()
        for ligne in reader:
            #traitement pour une ligne
            a=ligne[0]
            b=ligne[1]
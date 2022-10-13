from PIL import Image
from magic import Magic

class ImageConverter():
    
    @staticmethod
    def convert(filePath, newImagePath = None):
        generatedFilePath = newImagePath if newImagePath != None else filePath
        im = Image.open(filePath)
        mime_type = Magic.from_file(filePath, mime=True)
        if( mime_type != "image/png"): 
            im.save(fp=generatedFilePath, format="png" )
        
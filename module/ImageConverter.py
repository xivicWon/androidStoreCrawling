from PIL import Image
import magic


class ImageConverter():
    
    @staticmethod
    def convert(filePath, newImagePath = None):
        generatedFilePath = newImagePath if newImagePath != None else filePath
        im = Image.open(filePath)
        mime_type = magic.from_file(filePath, mime=True)
        if( mime_type != "image/png"): 
            im.save(fp=generatedFilePath, format="png" )
        
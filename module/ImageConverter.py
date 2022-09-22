from PIL import Image

class ImageConverter():
    
    @staticmethod
    def convert(filePath, newImagePath = None):
        generatedFilePath = newImagePath if newImagePath != None else filePath
        im = Image.open(filePath)
        im.save(fp=generatedFilePath, format="png" )
        
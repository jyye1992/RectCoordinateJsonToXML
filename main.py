import json
import xml.etree.cElementTree as ET
import os
import math

def reaJson(filename):
    f = open('./TrainDataset/json/' +filename)
    j = json.loads(f.read())

    return j

class AnnotationXML:
    def __init__(self, filename, ):
        self.filename = filename.split('.')[0]
        self.root = ET.Element("annotation")
        ET.SubElement(self.root, "folder").text = 'tests'
        ET.SubElement(self.root, "filename").text = self.filename 
        
    def addObject(self, cx, cy, w, h, angle="0"):
        object = ET.SubElement(self.root, "object")
        ET.SubElement(object, "type").text = 'robndbox'
        ET.SubElement(object, "name").text = 'rot'
        ET.SubElement(object, "pose").text = 'Unspecified'    
        robndbox = ET.SubElement(object, "robndbox")
        ET.SubElement(robndbox, "cx").text = cx
        ET.SubElement(robndbox, "cy").text = cy
        ET.SubElement(robndbox, "w").text = w
        ET.SubElement(robndbox, "h").text = h
        ET.SubElement(robndbox, "angle").text = angle

    def write(self, out_dir):
        tree = ET.ElementTree(self.root)
        
        tree.write('./' + out_dir + '/' + self.filename + ".xml")

class Point:
    def __init__(self, x, y):
        self._x = x
        self._y = y
    
    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y


class RectTangle:
    def __init__(self, point1, point2, point3, point4):
        '''
        1  2
        4  3
        '''
        self.point1 = point1
        self.point2 = point2
        self.point3 = point3
        self.point4 = point4
    
    @property
    def cx(self):
        return (self.point1.x + self.point2.x) / 2

    @property
    def cy(self):
        return (self.point1.y + self.point2.y) / 2

    @property
    def w(self):
        return self.point2.x - self.point1.x

    @property
    def h(self):
        return self.point2.x - self.point1.x

    @property
    def angle(self):
        diffs = [self.point1.x - self.point4.x, self.point1.y - self.point4.y]

        if diffs[1] == 0:
           return 0
        else:
            return math.atan(abs(diffs[0])/abs(diffs[1]))

def main():
    file_list = os.listdir('TrainDataset/json')

    for filename in file_list:
        data = reaJson(filename)

        xml = AnnotationXML(data['imagePath'])
        for shape in data['shapes']:
            rect = RectTangle(
                Point(shape['points'][0][0], shape['points'][0][1]),
                Point(shape['points'][1][0], shape['points'][1][1]),
                Point(shape['points'][2][0], shape['points'][2][1]),
                Point(shape['points'][3][0], shape['points'][3][1]),
            )
            xml.addObject(
                str(rect.cx), 
                str(rect.cy), 
                str(rect.w), 
                str(rect.h), 
                str(rect.angle)
            )
        xml.write('output')
    

if __name__ == '__main__':
    main()
    print('done')


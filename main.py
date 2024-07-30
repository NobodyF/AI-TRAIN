# Required packages
import os
from PIL import Image, ExifTags

# Function to correct image orientation based on EXIF data
def correct_orientation(image):
    try:
        # Get the EXIF data from the image
        exif = image._getexif()
        if exif:
            # Loop through the tags and find the orientation tag
            for tag, value in ExifTags.TAGS.items():
                if value == 'Orientation':
                    orientation = exif.get(tag)
                    # Rotate or flip the image according to the orientation
                    if orientation == 3:
                        image = image.rotate(180, expand=True)
                    elif orientation == 6:
                        image = image.rotate(270, expand=True)
                    elif orientation == 8:
                        image = image.rotate(90, expand=True)
    except AttributeError:
        # If no EXIF data is found or there's an error, do nothing
        pass
    return image

# Source
path_images = "E:/TestForRotating/Dataset/img"
path_labels = "E:/TestForRotating/Dataset/imgL"

# Destination
dest_images = "E:/TestForRotating/Dataset640/imgR/"
dest_labels = "E:/TestForRotating/Dataset640/imgRL/"

# Split configuration
size = 640
overlap = int(0.2 * size)
step = 640 - overlap

# Identify if object is out of cropped image
def OutOfCrop( box, crop ):
    if VerticalOutOfCrop( box['y1'], box['y2'], crop['y1'], crop['y2'] ):
        return True
    if HorizontalOutOfCrop( box['x1'], box['x2'], crop['x1'], crop['x2'] ):
        return True
    else:
        return False
    
def VerticalOutOfCrop( y_top, y_down, boxUp, boxDown ):
    if y_down < boxUp:
        return True
    if y_top > boxDown:
        return True

def HorizontalOutOfCrop( x_left, x_right, boxLeft, boxRight ):
    if x_left > boxRight:
        return True
    if x_right < boxLeft:
        return True

# Identify if object is located in cropped image
def BelongToCrop( box, crop ):
    if (box['x1'] >= crop['x1']) and (box['x2'] <= crop['x2']) and (box['y1'] >= crop['y1']) and (box['y2'] <= crop['y2']):
        return True
    else:
        return False

# Identify if object is located in corner of image
def x1y1BelongToCrop( box, crop ):
    if (box['x1'] >= crop['x1']) and (box['x1'] < crop['x2']) and (box['y1'] >= crop['y1']) and (box['y1'] < crop['y2']):
        return True
    else:
        return False
    
def x2y1BelongToCrop( box, crop ):
    if (box['x2'] <= crop['x2']) and (box['x2'] > crop['x1']) and (box['y1'] >= crop['y1']) and (box['y1'] < crop['y2']):
        return True
    else:
        return False
    
def x1y2BelongToCrop( box, crop ):
    if (box['x1'] >= crop['x1']) and (box['x1'] < crop['x2']) and (box['y2'] <= crop['y2']) and (box['y2'] > crop['y1']):
        return True
    else:
        return False
    
def x2y2BelongToCrop( box, crop ):
    if (box['x2'] <= crop['x2']) and (box['x2'] > crop['x1']) and (box['y2'] <= crop['y2']) and (box['y2'] > crop['y1']):
        return True
    else:
        return False

# Identify if half of object is located in image
def RightHalfBelongToCrop( box, crop ):
    if x2y1BelongToCrop( box, crop ) and x2y2BelongToCrop( box, crop ):
        return True
    else:
        return False

def LeftHalfBelongToCrop( box, crop ):
    if x1y1BelongToCrop( box, crop ) and x1y2BelongToCrop( box, crop ):
        return True
    else:
        return False
    
def TopHalfBelongToCrop( box, crop ):
    if x1y1BelongToCrop( box, crop ) and x2y1BelongToCrop( box, crop ):
        return True
    else:
        return False
    
def DownHalfBelongToCrop( box, crop ):
    if x1y2BelongToCrop( box, crop ) and x2y2BelongToCrop( box, crop ):
        return True
    else:
        return False
    
# Identify if object is greater than cropped image
def LeftLineBelongToCrop( box, crop ):
    if (box['x1'] >= crop['x1']) and (box['x1'] < crop['x2']) and (box['y1'] < crop['y1']) and (box['y2'] > crop['y2']):
        return True
    else:
        return False
    
def RightLineBelongToCrop( box, crop ):
    if (box['x2'] <= crop['x2']) and (box['x2'] > crop['x1']) and (box['y1'] < crop['y1']) and (box['y2'] > crop['y2']):
        return True
    else:
        return False
    
def TopLineBelongToCrop( box, crop ):
    if (box['x1'] < crop['x1']) and (box['x2'] > crop['x2']) and (box['y1'] >= crop['y1']) and (box['y1'] < crop['y2']):
        return True
    else:
        return False
    
def DownLineBelongToCrop( box, crop ):
    if (box['x1'] < crop['x1']) and (box['x2'] > crop['x2']) and (box['y2'] <= crop['y2']) and (box['y2'] > crop['y1']):
        return True
    else:
        return False
    
def HorizontalLinesBelongToCrop( box, crop ):
    if TopLineBelongToCrop( box, crop ) and DownLineBelongToCrop( box, crop ):
        return True
    else:
        return False
    
def VerticalLinesBelongToCrop( box, crop ):
    if LeftLineBelongToCrop( box, crop ) and RightLineBelongToCrop( box, crop ):
        return True
    else:
        return False

def x1y1Crop( box, crop ):
    x1 = box['x1']
    y1 = box['y1']
    x2 = crop['x2']
    y2 = crop['y2']
    return {'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2}
    
def x2y1Crop( box, crop ):
    x1 = crop['x1']
    y1 = box['y1']
    x2 = box['x2']
    y2 = crop['y2']
    return {'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2}
    
def x1y2Crop( box, crop ):
    x1 = box['x1']
    y1 = crop['y1']
    x2 = crop['x2']
    y2 = box['y2']
    return {'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2}
       
def x2y2Crop( box, crop ):
    x1 = crop['x1']
    y1 = crop['y1']
    x2 = box['x2']
    y2 = box['y2']
    return {'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2}

def RightCrop( box, crop ):
    x1 = crop['x1']
    y1 = box['y1']
    x2 = box['x2']
    y2 = box['y2']
    return {'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2}

def LeftCrop( box, crop ):
    x1 = box['x1']
    y1 = box['y1']
    x2 = crop['x2']
    y2 = box['y2']
    return {'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2}

def DownCrop( box, crop ):
    x1 = box['x1']
    y1 = crop['y1']
    x2 = box['x2']
    y2 = box['y2']
    return {'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2}

def TopCrop( box, crop ):
    x1 = box['x1']
    y1 = box['y1']
    x2 = box['x2']
    y2 = crop['y2']
    return {'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2}

def DownLineCrop( box, crop ):
    x1 = crop['x1']
    y1 = box['y1']
    x2 = crop['x2']
    y2 = crop['y2']
    return {'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2}

def TopLineCrop( box, crop ):
    x1 = crop['x1']
    y1 = crop['y1']
    x2 = crop['x2']
    y2 = box['y2']
    return {'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2}

def LeftLineCrop( box, crop ):
    x1 = crop['x1']
    y1 = crop['y1']
    x2 = box['x2']
    y2 = crop['y2']
    return {'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2}

def RightLineCrop( box, crop ):
    x1 = box['x1']
    y1 = crop['y1']
    x2 = crop['x2']
    y2 = crop['y2']
    return {'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2}

def HorizontalLinesCrop( box, crop ):
    x1 = crop['x1']
    y1 = box['y1']
    x2 = crop['x2']
    y2 = box['y2']
    return {'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2}

def VerticalLinesCrop( box, crop ):
    x1 = box['x1']
    y1 = crop['y1']
    x2 = box['x2']
    y2 = crop['y2']
    return {'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2}

# Structure of YoLo box (without class)
def BoxToYolo( box ):
    width = box['x2'] - box['x1']
    height = box['y2'] - box['y1']
    x = box['x1'] + (width / 2.0)
    y = box['y1'] + (height / 2.0)
    return {'x': x, 'y': y, 'width': width, 'height': height}

# Recalculate coordinates
def NormBox( box, crop ):
    box['x1'] = (box['x1'] - crop['x1']) / (crop['x2'] - crop['x1'])
    box['x2'] = (box['x2'] - crop['x1']) / (crop['x2'] - crop['x1'])
    box['y1'] = (box['y1'] - crop['y1']) / (crop['y2'] - crop['y1'])
    box['y2'] = (box['y2'] - crop['y1']) / (crop['y2'] - crop['y1'])
    return box

# Stringify YoLo box
def BoxToString( boxYolo ):
    yoloStr = '%s %s %s %s' % (boxYolo['x'], boxYolo['y'], boxYolo['width'], boxYolo['height'])
    return yoloStr

# Box is converted to YoLo string (without class)
def BoxToYoloStr( box, crop ):
    box = NormBox( box, crop )
    box = BoxToYolo( box )
    return BoxToString( box )

# Dataset opening
images = os.listdir( path_images )
labels = os.listdir( path_labels )

for img in images:
    
    # image reading
    im = Image.open( path_images + '/' + img )
    imgWidth = im.width
    imgHeight = im.height
    
    # related label file
    labelFile = img[:-4] + '.txt'
    # TODO: if label file does not exist, create it and then run script
    # label extraction from file
    with open( path_labels + '/' + labelFile ) as f:
        labels = f.readlines()
        f.close()
    for i in range(len(labels)):
        labels[i] = labels[i].replace('\n', '')
            
    # cropping cycle
    counter = 0
    for startX in range(0, imgWidth-size, step):
        for startY in range(0, imgHeight-size, step):
            
            endX = startX+size
            endY = startY+size
            
            # Crop of image
            tempImg = im.crop( (startX, startY, endX, endY) )
            
            # Cropped image coordinates
            xMin = startX / imgWidth
            xMax = endX / imgWidth
            yMin = startY / imgHeight
            yMax = endY / imgHeight
            
            # Crop box
            crop = {
                'x1': xMin,
                'x2': xMax,
                'y1': yMin,
                'y2': yMax,
            }
            
            nboxes = []
            for label in labels:
                
                # Splitting YoLo parameters
                params = label.split(' ')
                cls = int(params[0])
                x = float(params[1])
                y = float(params[2])
                width = float(params[3])
                height = float(params[4])
                
                # Point coordinates calculation
                x_left = x - width/2.0
                x_right = x + width/2.0
                y_top = y - height/2.0
                y_down = y + height/2.0
                
                # Boxing of coordinates 
                box = {
                    'x1': x_left,
                    'x2': x_right,
                    'y1': y_top,
                    'y2': y_down,
                }
                
                # Box cropping
                if OutOfCrop( box, crop ):
                    continue
                elif BelongToCrop( box, crop ):
                    box = box
                elif RightHalfBelongToCrop( box, crop ):
                    box = RightCrop( box, crop )
                elif LeftHalfBelongToCrop( box, crop ):
                    box = LeftCrop( box, crop )
                elif TopHalfBelongToCrop( box, crop ):
                    box = TopCrop( box, crop )
                elif DownHalfBelongToCrop( box, crop ):
                    box = DownCrop( box, crop )
                elif HorizontalLinesBelongToCrop( box, crop ):
                    box = HorizontalLinesCrop( box, crop )
                elif VerticalLinesBelongToCrop( box, crop ):
                    box = VerticalLinesCrop( box, crop )
                elif TopLineBelongToCrop( box, crop ):
                    box = TopLineCrop( box, crop )
                elif DownLineBelongToCrop( box, crop ):
                    box = DownLineCrop( box, crop )
                elif RightLineBelongToCrop( box, crop ):
                    box = RightLineCrop( box, crop )
                elif LeftLineBelongToCrop( box, crop ):
                    box = LeftLineCrop( box, crop )
                elif x1y1BelongToCrop( box, crop ):
                    box = x1y1Crop( box, crop )
                elif x2y1BelongToCrop( box, crop ):
                    box = x2y1Crop( box, crop )
                elif x1y2BelongToCrop( box, crop ):
                    box = x1y2Crop( box, crop )
                elif x2y2BelongToCrop( box, crop ):
                    box = x2y2Crop( box, crop )
                else:
                    print('Error')
                nboxes.append( str(cls) + ' ' + BoxToYoloStr( box, crop ) + '\n' )
            
            # Save cropped image and related labels
            if len(nboxes) > 0:
                tempImg.save(dest_images + img[:-4] + '_' + str(counter) + '.jpg')
                with open(dest_labels + img[:-4] + '_' + str(counter) + '.txt', 'w') as f:
                    f.writelines(nboxes)
                    f.close()
                counter = counter + 1    

for img in images:
    
    # Image reading
    im = Image.open(path_images + '/' + img)
    im = correct_orientation(im)  # Correct the orientation
    imgWidth = im.width
    imgHeight = im.height
    
    # Related label file
    labelFile = img[:-4] + '.txt'
    # TODO: if label file does not exist, create it and then run script
    # Label extraction from file
    with open(path_labels + '/' + labelFile) as f:
        labels = f.readlines()
        f.close()
    for i in range(len(labels)):
        labels[i] = labels[i].replace('\n', '')
            
    # Cropping cycle
    counter = 0
    for startX in range(0, imgWidth - size, step):
        for startY in range(0, imgHeight - size, step):
            
            endX = startX + size
            endY = startY + size
            
            # Crop of image
            tempImg = im.crop((startX, startY, endX, endY))
            
            # Cropped image coordinates
            xMin = startX / imgWidth
            xMax = endX / imgWidth
            yMin = startY / imgHeight
            yMax = endY / imgHeight
            
            # Crop box
            crop = {
                'x1': xMin,
                'x2': xMax,
                'y1': yMin,
                'y2': yMax,
            }
            
            nboxes = []
            for label in labels:
                
                # Splitting YoLo parameters
                params = label.split(' ')
                cls = int(params[0])
                x = float(params[1])
                y = float(params[2])
                width = float(params[3])
                height = float(params[4])
                
                # Point coordinates calculation
                x_left = x - width / 2.0
                x_right = x + width / 2.0
                y_top = y - height / 2.0
                y_down = y + height / 2.0
                
                # Boxing of coordinates 
                box = {
                    'x1': x_left,
                    'x2': x_right,
                    'y1': y_top,
                    'y2': y_down,
                }
                
                # Box cropping
                if OutOfCrop(box, crop):
                    continue
                elif BelongToCrop(box, crop):
                    box = box
                elif RightHalfBelongToCrop(box, crop):
                    box = RightCrop(box, crop)
                elif LeftHalfBelongToCrop(box, crop):
                    box = LeftCrop(box, crop)
                elif TopHalfBelongToCrop(box, crop):
                    box = TopCrop(box, crop)
                elif DownHalfBelongToCrop(box, crop):
                    box = DownCrop(box, crop)
                elif HorizontalLinesBelongToCrop(box, crop):
                    box = HorizontalLinesCrop(box, crop)
                elif VerticalLinesBelongToCrop(box, crop):
                    box = VerticalLinesCrop(box, crop)
                elif TopLineBelongToCrop(box, crop):
                    box = TopLineCrop(box, crop)
                elif DownLineBelongToCrop(box, crop):
                    box = DownLineCrop(box, crop)
                elif RightLineBelongToCrop(box, crop):
                    box = RightLineCrop(box, crop)
                elif LeftLineBelongToCrop(box, crop):
                    box = LeftLineCrop(box, crop)
                elif x1y1BelongToCrop(box, crop):
                    box = x1y1Crop(box, crop)
                elif x2y1BelongToCrop(box, crop):
                    box = x2y1Crop(box, crop)
                elif x1y2BelongToCrop(box, crop):
                    box = x1y2Crop(box, crop)
                elif x2y2BelongToCrop(box, crop):
                    box = x2y2Crop(box, crop)
                else:
                    print('Error')
                nboxes.append(str(cls) + ' ' + BoxToYoloStr(box, crop) + '\n')
            
            # Save cropped image and related labels
            if len(nboxes) > 0:
                tempImg.save(dest_images + img[:-4] + '_' + str(counter) + '.jpg')
                with open(dest_labels + img[:-4] + '_' + str(counter) + '.txt', 'w') as f:
                    f.writelines(nboxes)
                    f.close()
                counter += 1
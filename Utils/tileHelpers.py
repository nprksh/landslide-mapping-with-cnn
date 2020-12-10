import cv2


def returnTile(image, tileSize, centerLocation):
    assert (tileSize % 2) == 0 ## Check that tileSize is even
    halfSpan = int(tileSize/2)
    
    if len(image.shape) == 2:
        return image[centerLocation[1] - halfSpan : centerLocation[1] + halfSpan, centerLocation[0] - halfSpan : centerLocation[0] + halfSpan]
    elif len(image.shape) == 3:
        return image[centerLocation[1] - halfSpan : centerLocation[1] + halfSpan, centerLocation[0] - halfSpan : centerLocation[0] + halfSpan, : ]
    else:
        print("DIMENSION ERROR!!!! IMAGE NEEDS 2 or 3 DIM.")
        return 0
        
    
def trueMaskPercentInTile(mask, tileSize, centerLocation):
    """
    Percentage of area which are 'True' or 1 in the tile
    mask = expects a binary mask
    return back a number between 0 to 1 for percentage
    """
    currMask = returnTile(mask, tileSize, centerLocation)
    return currMask.sum()/(tileSize*tileSize*1.0) 



def rescaleInput(image, shape, interpolation=cv2.INTER_CUBIC):
    if image.shape[ : 2] == shape:
        return image
    else:
        return cv2.resize(image, (shape[1], shape[0]), interpolation)


def isValidTile(mask, tileSize, centerLocation, threshold = 0.5):   
    return trueMaskPercentInTile(mask, tileSize, centerLocation) >= threshold


def bbox(img):
    scn = np.any(img, axis=1)
    pix = np.any(img, axis=0)
    scnMin, scnMax = np.where(scn)[0][[0, -1]]
    pixMin, pixMax = np.where(pix)[0][[0, -1]]
    return [scnMin, scnMax, pixMin, pixMax]



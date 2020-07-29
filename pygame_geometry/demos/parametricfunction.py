"""The goal of this file is to be able to make a parametric function of a
picture or a disordered list of points. If this program succeed, it will be
possible to make a fourier transform of any picture which can be cool."""

from curves import Trajectory
#import numpy as np
import math
import cv2
import pickle
import time

sj = "saint jalm.jpg"
vl = "valentin.png"
tm = "tetedemarc.png"
pm = "profiledemarc.jpg"


def searchPoints(canny_image):
    """Return the list of white points of a canny image."""
    l = []
    height, width = image.shape[:2]
    for x in range(width):
        for y in range(height):
            if canny_image[y][x]:
                l.append((x, y))
    return l


def getClosestPoint(pt, ps):
    """Get the closest point to pt within the list of points ps."""
    psd = [(getDistance(pt, ps[i]), i) for i in range(len(ps))]
    p = min(psd, key=lambda x: x[0])
    return p[1]


def getClosestPoints(ps1, ps2):
    """Return the two closest points from ps1 and ps2."""
    # Naive way to proceed...
    l = [(getClosestPoint(ps1[i], ps2), i) for i in range(len(ps1))]
    p = min(psd, key=lambda x: x[0])
    return p[1]


def getDistance(p1, p2):
    """Return the distance between p1 and p2."""
    return math.sqrt(sum([(p1[i] - p2[i])**2 for i in range(max(len(p1), len(p2)))]))


def getDistances(pts):
    return sum([getDistance(pts[i], pts[i + 1]) for i in range(len(pts) - 1)])


def getPath(ps):
    """Return the path (list of points) that stars and p and pass through all the points."""
    p = ps[0]
    del ps[0]
    path = [p]
    n = 0
    l = len(ps)
    to = time.time()
    while len(ps) > 0:
        n += 1
        i = getClosestPoint(p, ps)
        path.append(ps[i])
        p = ps[i]
        del ps[i]
        # print(round(100*(1-len(ps)/l),3),"%")
        print(getTimeLeft(to, 0, l - len(ps), l))
    return path


def cleanPoints(points):
    """Delete the doublons but loose the order."""
    return list(set(points))


def interpolate(path, n=200):
    """Interpolate n points from the path."""
    return Trajectory.createFromTuples(path).sample(n)


def getToPlane(p, shape):
    """Convert coordonnates in the plane coordonnates system."""
    x, y = p
    h, w = shape[:2]
    m = max(w, h)
    return (x / m, -y / m)


def getAllToPlane(ps, shape):
    """Convert all the coordonnnates in the plane coordonnates system."""
    return [getToPlane(p, shape) for p in ps]


def getTimeLeft(to, start, position, end):
    """Return the time left in the loop."""
    return (end - position) * (time.time() - to) / (position - start)


def reduceFormat(image):
    pass


def sampleOnceEveryN(l, n=2):
    """Sample some points."""
    return [l[i] for i in range(0, len(l), n)]


# image=cv2.imread(tm)
# gray=cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
# blur=cv2.GaussianBlur(gray,(5,5),0)
# canny=cv2.Canny(image,50,150)
# pts=searchPoints(canny)
# print(getDistances(pts))
# path=getPath(pts)
# print(getDistances(path))

# cv2.imshow("result",canny)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# plt.imshow(canny)
# plt.show()

sj = "saint jalm.jpg"
vl = "valentin.png"
tm = "tetedemarc.png"
pm = "profiledemarc.jpg"
mx = "maxime.jpg"


if __name__ == "__main__":
    from fouriervf import VisualFourier
    from context import Context

    filename = "FourierObjects/Path"
    imagename = tm

    try:
        path = pickle.load(open(filename, 'rb'))['path']
        raise None
    except:
        to = time.time()
        # Sample the picture into an ordered list of points.
        image = cv2.imread(imagename)
        canny = cv2.Canny(image, 50, 150)
        pts = searchPoints(canny)
        pts = cleanPoints(pts)
        pts = sampleOnceEveryN(pts, n=10)
        path = getPath(pts)
        path = interpolate(path)
        print(time.time() - to)
        path = getAllToPlane(path, image.shape)
        pickle.dump({'path': path}, open(filename, 'wb'))

    # Use this ordered list of points to make the fourier transform.
    context = Context(
        name="Application of the Fourier Transform.", fullscreen=False)
    fourier = VisualFourier(context, image=imagename)
    # fourier.load()
    fourier.drawing = path
    fourier.updateSample()
    fourier()
    fourier.save()

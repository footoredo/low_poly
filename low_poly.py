from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import random
from oct2py import octave
import numpy
from scipy.spatial import distance
import math
import sys
octave.addpath('octave/')

def average_color(vertices, mask, source):
  x0 = min(p[0] for p in vertices)
  x1 = max(p[0] for p in vertices)
  y0 = min(p[1] for p in vertices)
  y1 = max(p[1] for p in vertices)

  valids = map(source.getpixel, filter(lambda x: mask.getpixel(x)==1, [ (x,y) for x in range(x0, x1+1) for y in range(y0, y1+1) ]) )
#print valids
  result = tuple([sum(x)/len(x) for x in zip(*valids)])
#print result
  return result

def triangulation(x, y, draw, source):
  T = map(lambda x:map(lambda x:int(x)-1,x),octave.delaunay(x,y))
  mask = Image.new('L', source.size, 0)
  mask_draw = ImageDraw.Draw(mask)
  for triangle in T:
#for i in range(0,3):
#draw.line(((x[triangle[i]],y[triangle[i]]),(x[triangle[(i+1)%3]],y[triangle[(i+1)%3]])), fill="grey")
    vertices = [ (x[v], y[v]) for v in triangle[:3] ]
#center = (lambda x: (x[0]/3,x[1]/3))( reduce(lambda x,y: (x[0]+y[0],x[1]+y[1]), vertices)) 
#draw.polygon( vertices, fill = source.getpixel( center ) ) 
    mask_draw.polygon( vertices, fill = 1 )
#print vertices
    draw.polygon( vertices, fill = average_color(vertices, mask, source) )
    mask_draw.polygon( vertices, fill = 0 )

def P(x,y,source,edges):
  '''diff = numpy.mean([distance.euclidean(source.getpixel((x+dx,y+dy)),source.getpixel((x,y))) for dx in [-1,0,1] for dy in [-1,0,1]])  
#print diff
  return 0.1 if diff > 50 else 0 '''
  return 0.1 if edges.getpixel((x,y))>50 else 0

def low_poly(source, min_dist, factor):
  image = source
  draw = ImageDraw.Draw(image)
  width, height = image.size
  '''x = octave.poissrnd(width/2,1,cnt).tolist()[0]
  y = octave.poissrnd(height/2,1,cnt).tolist()[0]
  print type(x)
  print x,y
  filtl = lambda x: 0 if x < 0 else x
  filtr = lambda bound: ( lambda x: bound-1 if x >= bound else x )
  x = map(filtr(width),map(filtl,x))
  y = map(filtr(height),map(filtl,y))
  print x,y
  triangulation(x, y, draw, source)'''
 
  S = octave.generate_poisson_2d(numpy.array([width,height]),min_dist,20)
  x = [ int(p[0]) for p in S ]
  y = [ int(p[1]) for p in S ]
  edges = image.filter(ImageFilter.FIND_EDGES).convert("L")
#edges.show()
  enhancer = ImageEnhance.Brightness(edges)
  edges = enhancer.enhance(factor)
#edges.show()
  for i in range(0,width):
    for j in range(0,height):
      if random.random() < P(i,j,source,edges):
        x.append(i)
        y.append(j)
  triangulation(x,y,draw,source)
  return image

#octave.fvckeverything()
#print "fvck"  
source = Image.open(sys.argv[1]).convert("RGB")
image = low_poly(source,float(sys.argv[2]),float(sys.argv[3]))
image.show()
if len(sys.argv) > 4:
  image.save(sys.argv[4])

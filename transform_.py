from javax.media.j3d import Transform3D
from javax.vecmath import Vector3d, AxisAngle4d, Point3d
from java.lang import Math

def computeWorldCorrection():
  x0, y0, z0 = 43324.0, 41836.0, 0.0
  x1, y1, z1 = 46780.0, 45532.0, 22950.0
  x2, y2, z2 = x0, y0, z1
  
  # A point in the first section that should be directly on top of the x0,y0,z0
  x3, y3, z3 = 48164, 23372, 0

  trans = Transform3D()
  trans.setTranslation(Vector3d(-x0, -y0, 0))

  rot = Transform3D()

  p0 = Vector3d(0, 0, z1)
  p1 = Vector3d(x1 - x0, y1 - y0, z1 - z0)
  pc = Vector3d()
  pc.cross(p1, p0)

  angle = Math.atan(Math.sqrt(Math.pow(x1 - x0, 2) + Math.pow(y1 - y0, 2)) / (z1 - z0))
  print angle * 180 / Math.PI

  rot.setRotation(AxisAngle4d(pc, angle))

  t = Transform3D()
  t.mul(rot)
  t.mul(trans)

  # Transform the third point
  p3 = Point3d(x3, y3, z3)
  t.transform(p3)
  print "A p3:", p3

  # test
  p0 = Point3d(x0, y0, z0)
  t.transform(p0)
  print "A: p0", p0

  p1 = Point3d(x1, y1, z1)
  t.transform(p1)
  print "A: p1", p1

  # Compute rotation of third point around Z axis
  rotZ = Transform3D()
  angleZ = Math.atan((p3.x - 0) / (p3.y - 0))
  print "angleZ", angleZ
  rotZ.setRotation(AxisAngle4d(Vector3d(0,0,1), angleZ))

  t.mul(rotZ, t)
  
  
  # test
  p0 = Point3d(x0, y0, z0)
  t.transform(p0)
  print p0

  p1 = Point3d(x1, y1, z1)
  t.transform(p1)
  print p1

  p3 = Point3d(x3, y3, z3)
  t.transform(p3)
  print p3

  return t

t = computeWorldCorrection()
print t

m = [0.9509217490842972, 0.24926674965164644, -0.18334097915241027, -51626.05759575438,
     -0.2722540786706435, 0.9555797748775074, -0.11289380183274611, -28182.499757448437,
     0.14705626054561627, 0.15726850086128405, 0.9765454801857332, -12950.550433910958,
     0.0, 0.0, 0.0, 1.0]

# yes: it's the same
#t2 = Transform3D(m)
#print t2
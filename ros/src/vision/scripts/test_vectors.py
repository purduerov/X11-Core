from vectors import Vector
from random import randint
import numpy as np

def test_get_vector_start_point(line_fail):
  v = Vector()

  Vector.prev_vector = [2,1]
  st_pt = v.get_vector_start_point()
  if st_pt != [0, Vector.y_cam_height / 2] and line_fail[0] == -1:
    line_fail[0] = 8

  Vector.prev_vector = [1,2]
  st_pt = v.get_vector_start_point()
  if st_pt != [Vector.x_cam_width / 2, Vector.y_cam_height] and line_fail[0] == -1:
    line_fail[0] = 13

  Vector.prev_vector = [-2,1]
  st_pt = v.get_vector_start_point()
  if st_pt != [Vector.x_cam_width, Vector.y_cam_height / 2] and line_fail[0] == -1:
    line_fail[0] = 18

  Vector.prev_vector = [1,-2]
  st_pt = v.get_vector_start_point()
  if st_pt != [Vector.x_cam_width / 2, 0] and line_fail[0] == -1:
    line_fail[0] = 23

def test_get_thrust_vect(line_fail):
  v = Vector()

  Vector.prev_vector = [2,1]
  st_pt = v.get_vector_start_point()
  center = [Vector.x_cam_width / 2 + randint(-80,80), Vector.y_cam_height / 2 + randint(-80,80)]
  v.get_thrust_vect(st_pt, center)
  if not np.array_equal(np.add(Vector.prev_vector, v.thrust_vect), v.resultant_vect) and line_fail[0] == -1:
    line_fail[0] = 36
    print("prev_vector:",Vector.prev_vector)
    print("thrust_vector:",v.thrust_vect)
    print("resultant_vector:",v.resultant_vect)
    

if __name__ == "__main__":
  line_fail = [-1]
  test_get_vector_start_point(line_fail)
  test_get_thrust_vect(line_fail)

  print(line_fail[0])

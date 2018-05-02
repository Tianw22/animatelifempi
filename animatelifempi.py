#This is the with boarder version.
from memory_profiler import profile
from mpi4py import MPI
import numpy
import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from tqdm import tqdm
fig = plt.figure()
prob = 0.7 ##0.2, 0.4, 0.5, 0.75, & 0.9
COLS = 400
ROWS = 210
generations = 200

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()
subROWS=ROWS / (size - 1)
def cal_life(row_min, row_max, life_env_data):
  intermediateM = numpy.copy(life_env_data)
  for ROWelem in range(row_min,row_max):
    for COLelem in range(1,COLS-1):
      sum = (
          life_env_data[ROWelem-1,COLelem-1]
          +life_env_data[ROWelem-1,COLelem]
          +life_env_data[ROWelem-1,COLelem+1]
          +life_env_data[ROWelem,COLelem-1]
          +life_env_data[ROWelem,COLelem+1]
          +life_env_data[ROWelem+1,COLelem-1]
          +life_env_data[ROWelem+1,COLelem]
          +life_env_data[ROWelem+1,COLelem+1]
        )
      if life_env_data[ROWelem,COLelem] == 1:
        if sum < 2:
          intermediateM[ROWelem,COLelem] = 0
        elif sum > 3:
          intermediateM[ROWelem,COLelem] = 0
        else:
          intermediateM[ROWelem,COLelem] = 1

      if life_env_data[ROWelem,COLelem] == 0:
        if sum == 3:
          intermediateM[ROWelem,COLelem] = 1
        else:
          intermediateM[ROWelem,COLelem] = 0
  return intermediateM[row_min:row_max]


if rank == 0:
  if (size-1) > ROWS:
    print("Not enough ROWS")
    exit()
  if size < 2:
    print("Not enough MPI size")
    exit()
  if ROWS % (size - 1) != 0:
    print("rows can not be distributed evenly")
    exit()
  N=numpy.random.binomial(1,prob,size=(ROWS+2)*COLS)
  M=numpy.reshape(N,(ROWS+2,COLS))
  M[0,:] = 0
  M[ROWS+1,:] = 0
  M[:,0] = 0
  M[:,COLS-1] = 0
  generation = 0
  ims=[]
  local_data = numpy.copy(M)

for i in tqdm(range(generations)):
  local_data = comm.bcast(local_data if rank == 0 else None, root=0)

  if rank == 0:
    generation = generation + 1
    combine_data = None
  else:
    combine_data = cal_life((rank-1)*subROWS+1,((rank)*subROWS) + 1,local_data)

  ret = comm.gather(combine_data,root=0)

  if rank == 0:
    ret1=numpy.reshape(range(COLS),(1,COLS))
    ret1[0:COLS] = 0
    last_row = ret1[0:COLS]
    for aaa in range(1, size):
      ret1 = numpy.r_[ret1, ret[aaa]]

    ret1 = numpy.r_[ret1, last_row]

    local_data = numpy.copy(ret1)

    im=plt.imshow(local_data, animated=True,interpolation='None')
    ims.append([im])
    if numpy.sum(local_data) == 0:
      print("Extinction Occurs at generation = ",generation)
      break

if rank == 0:
  print("Present Generation = %d" %(generation))
  ani = animation.ArtistAnimation(fig, ims, interval=25, blit=False,repeat_delay=500)
  ani.save('animate_life.mp4')
  plt.show()

  ## mpirun -n 4 python animatelifempi.py
  ## 4 can be replaced by 8 ro 16. Attention: 210%(number-1)==0.

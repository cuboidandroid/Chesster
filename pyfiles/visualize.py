import matplotlib.pyplot as plt
from board_and_pieces import *


ex, ey = 7, 6

f, axs = plt.subplots(2, 3)
f.set_figheight(6)
f.set_figwidth(10)

visu = setup_position()
ind = np.array(list(zip(*bishop(ex, ey, visu))))
visu[ind[0], ind[1]] = 1
print(visu)
print('')

ex, ey = 7, 1
visu = setup_position()
ind = np.array(list(zip(*rook(ex, ey, visu))))
visu[ind[0], ind[1]] = 1
print(visu)
print('')

ex, ey = 5, 7
visu = setup_position()
ind = np.array(list(zip(*queen(ex, ey, visu))))
visu[ind[0], ind[1]] = 1
print(visu)
print('')

ex, ey = 3, 6
visu = setup_position()
ind = np.array(list(zip(*knight(ex, ey, visu))))
visu[ind[0], ind[1]] = 1
print(visu)
print('')

axs[1, 0].imshow(visu)
#
# visu = setup_board()
# ind = np.array(list(zip(*king(ex, ey))))
# visu[ind[0], ind[1]] = -1
# visu[ex, ey] = 2
#
# axs[1, 1].imshow(visu)
#
# visu = setup_board()
# ind = np.array(list(zip(*wpawn(ex, ey))))
# visu[ind[0], ind[1]] = -1
# visu[ex, ey] = 2
#
# axs[1, 2].imshow(visu)
plt.show()

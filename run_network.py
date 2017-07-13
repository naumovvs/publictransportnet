from stochastic import stochastic
from transportnet import net

# generation of a random transport network
# given:    num_nodes - number of nodes in a net
#           num_links - number of links in a net
#           link_weight - stochastic variable
#
#   num_nodes   max(num_links)
#   1           0  0*1
#   2           2  1*2
#   3           6  2*3
#   4           12 3*4
#   5           ?  4*5(?)
#   ...         ...
#   n           n*(n-1)

# forming the network
#
n = net.Net()

# stochastic variable of the links weight
sw = stochastic.Stochastic(1, 1, 0.2)
# stochastic variable of the number of line stops
sn = stochastic.Stochastic(0, 3, 4)
# generating the links
n.generate(6, 30, sw)
# generating the lines
n.gen_lines(5, sn)
# print out simulation results
n.print_characteristics()
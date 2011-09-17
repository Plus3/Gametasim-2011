#import events

testlevel2 = {
1:"#################",
2:"#  ##########   #",
3:"#  ##     ###   #",
4:"#  ##     ###   #",
5:"#  #####  ###  ##",
6:"#              ##",
7:"#################"
}

testlevel2_events = {
(8,3): [(8,3), "msg", {"msg":"The room is dark! You can't see anything!"}, True]
}

testlevel = {
1:"################",
2:"#    #      ####",
3:"#    #      ####",
4:"###     ########",
5:"################"
}

testlevel_events = {
(3,3): [(3,3), "pickup", {"item":1}, True],
(12,2): [(12,2), "changemap", {"map":1}, False]
}



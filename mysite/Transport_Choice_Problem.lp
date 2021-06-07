\* Transport_Choice_Problem *\
Maximize
Total_cost: 30 _1 + 100 _2 + 150 _3 + 200 _4
Subject To
CostMaximum: 30 _1 + 100 _2 + 150 _3 + 200 _4 <= 1250
CostMinimum: 30 _1 + 100 _2 + 150 _3 + 200 _4 >= 1
Need_transport: _1 + _2 + _3 + _4 = 12
Bounds
0 <= _1 <= 12
0 <= _2 <= 12
0 <= _3 <= 12
0 <= _4 <= 12
Generals
_1
_2
_3
_4
End

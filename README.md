这是针对vnpy框架的高频策略客制

# 回测思路
    由生成的交易指令确定下单策略订单到成交面的高度，即历史订单尾+新增或取消的订单修正（乘0.5加在历史订单尾）（与策略订单同周期的）。下一tick级进行撮合判断，在撮合范围则订单成交，非撮合范围则降低策略订单到成交面的高度，降低的距离为撮合量（成交量）
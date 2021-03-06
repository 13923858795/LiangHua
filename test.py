class PlanServices:
    def __init__(self, top, bottom, buy_start, sell_start, top_share, increase, reduce):
        """价格区间"""
        self.top = top  # 价格顶部
        self.bottom = bottom  # 价格底部
        self.buy_start = buy_start  # 起始买入点
        self.sell_start = sell_start  # 起始卖出点
        self.top_share = top_share  # 买入时 顶部股分数量
        self.increase = increase  # 买入数量增长率
        self.reduce = reduce  # 价位减少率
        self.count_amount = 0  # 总买入金额
        self.count_sell_amount = 0
        self.count_share = 0  # 总买入股数
        self.share_plan = []  # 最后获取到的 股分买入顺序
        self.profit_rate = 0  # 利润率
        self.plan_info = []  # 计划表
        self.initial_position_amount = 0  # 初始买入资金
        self.initial_position = 0  # 初始买入仓位比率
        self.sell_top_price = 0 # 卖出的最高价

    def run(self):
        """1 获取买入计划表
        {'price': 1.9, 'plan_share': 1100, 'buy': 1100, 'buy_amount': 2090.0, 'count_share': 2100, 'count_amount': 4090.0}
        """
        buy_info = self.buy_plan()

        self.initial_position = round(self.initial_position_amount/self.count_amount, 3)

        self.plan_info = self.sell_plan(buy_info)
        self.sell_top_price = self.plan_info[0]['price']
        return True

    def sell_plan(self, buy_info):

        _long = len(buy_info)
        _sell_n = 0

        remaining_position = self.count_share
        _sell_count = 0

        for n in range(_long, -1, -1):

            if n < 1:
                break
            info = buy_info[n-1]
            """补充 买入 仓位比"""
            info["buy_position_rate"] = round(info["count_amount"] / self.count_amount, 2)

            if n == _long:
                _sell = 0  # 最底部卖出为0
            elif info['price'] < self.sell_start:

                # _sell = self.top * self.top_share / info['price']//100 * 100
                _sell = self.share_plan[0]

            else:
                _sell = self.share_plan[_sell_n]  # 获取对应的第n个
                _sell_n += 1

            info["sell_share"] = _sell
            _sell_count += _sell
            remaining_position -= _sell
            info["remaining_position"] = remaining_position
            self.count_sell_amount += int(_sell * info['price'])
            info["count_sell_amount"] = self.count_sell_amount

        """计算超出顶端的"""
        _rate = round(1/self.reduce, 2)  # 价格向上增长比率
        _rate_n = 1

        for i in range(_sell_n, len(self.share_plan)):

            _sell = self.share_plan[i]
            if remaining_position - _sell < 0:
                _sell = remaining_position

            price = round(self.top * _rate ** _rate_n, 3)
            _rate_n += 1
            self.count_sell_amount += int(_sell * price)

            remaining_position -= _sell
            _info = {"price": price, 'plan_share': 0, 'buy': 0, 'buy_amount': 0, 'count_share': 0, 'count_amount': 0,
                     'buy_position_rate': 0, "sell_share": _sell, "remaining_position": remaining_position,
                     "count_sell_amount": self.count_sell_amount}
            buy_info.insert(0, _info)
            if remaining_position == 0:
                break

        # for i in buy_info:
        #     a = (i['count_sell_amount'] + i['remaining_position'] * i['price'])/self.count_amount * 100
        #     print(round(a), i)
        #
        #
        # print(len(buy_info))

        self.profit_rate = round(self.count_sell_amount/self.count_amount -1, 3)

        return buy_info

    def buy_plan(self):
        date = []
        n = 0
        count_share = 0
        count_amount = 0
        BuyFlg = False
        while True:
            _price = round(self.top * self.reduce ** n, 3)

            if _price < self.bottom:
                break

            _plan_share = int(self.top_share * self.increase ** n//100 * 100)
            self.share_plan.append(_plan_share)
            count_share += _plan_share

            if _price <= self.buy_start and not BuyFlg :
                BuyFlg = True
                buy = count_share
                self.initial_position_amount = round(count_amount + buy*_price, 1)

            elif BuyFlg:
                buy = _plan_share
            else:
                buy = 0

            buy_amount = round(buy*_price, 1)
            count_amount = round(count_amount + buy_amount, 1)

            date.append({"price": _price, 'plan_share': _plan_share, "buy": buy, "buy_amount": buy_amount,
                         'count_share': count_share, "count_amount": count_amount})
            n += 1

        self.count_amount = count_amount
        self.count_share = count_share
        return date


def func(increase, reduce):
    plan = PlanServices(top, bottom, buy_start, sell_start, top_share, increase, reduce)
    plan.run()
    return plan


def func2():
    for x in range(100, 200):
        for y in range(50, 100):
            try:
                plan = func(x/100, y/100)
            except:
                continue

            count_amount = plan.count_amount
            rate = plan.profit_rate

            if x < 100 or y < 97 or rate < 0.2 or count_amount >100000:
                continue

            sell_top = plan.plan_info[0]["price"]
            print(f"股数增长比:{x/100}  价格下降比:{y/100} 总层数：{len(plan.plan_info)} 初始仓位比{plan.initial_position} "
                  f"最高价格: {plan.sell_top_price}"
                  f"总资金：{count_amount} 增长：{rate}")

def func3():
    plan = PlanServices(top, bottom, buy_start, sell_start, top_share, increase, reduce)
    plan.run()
    n = 1
    for i in plan.plan_info:
        print(n, i)

        if i['plan_share']:
            n = n + 1
    print(plan.profit_margin, int(plan.profit_margin * plan.count_amount))


top = 10
bottom = 5
buy_start = 6
sell_start = 6.5
top_share = 600
increase = 1.04
reduce = 0.975

func2()
# func3()
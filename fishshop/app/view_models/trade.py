
class TradeInfo:
    def __init__(self,goods):
        self.total=0
        self.trades=[]
        self.__parse(goods)

    #赠送与索要信息列表
    def __parse(self, goods):
        self.total = len(goods)
        self.trades = [self.__map_to_trade(single) for single in goods]

    # 处理赠送与索要者单条数据

    def __map_to_trade(self, single):
        # 首先判断时间是否为空
        if single.create_datetime:
            time = single.create_datetime.strftime('%Y-%m-%d')
        else:
            time = '未名'
        return dict(
            user_name=single.user.nickname,
            time=time,
           id=single.id)




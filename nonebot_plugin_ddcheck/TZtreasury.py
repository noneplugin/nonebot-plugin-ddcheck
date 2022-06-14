from services.db_context import db

class TZtreasury(db.Model):
    __tablename__ = "tz_treasury"

    id = db.Column(db.Integer(), primary_key=True)
    group_id = db.Column(db.BigInteger(), nullable=False)
    money = db.Column(db.BigInteger(), nullable=False, default=0)

    welfare_lottery  = db.Column(db.BigInteger(), nullable=False, default=1000)


    _idx1 = db.Index("tz_treasury_idx1", "group_id", unique=True)

    @classmethod
    async def spend(cls,  group_id: int, num: int):
        query = cls.query.where(cls.group_id == group_id)
        query = query.with_for_update()
        my = await query.gino.first()

        if my:
            await my.update(money=my.money + num).apply()
        else:
            await cls.create( group_id=group_id, money=10000 - num)

    @classmethod
    async def add(cls, group_id: int, num: int):
        query = cls.query.where(cls.group_id == group_id)
        query = query.with_for_update()
        my = await query.gino.first()
        
        if my:
            await  my.update(money=my.money + num).apply()
        else:
            await cls.create( group_id=group_id, money=10000 + num)

    @classmethod
    async def set(cls,  group_id: int, num: int):
        query = cls.query.where(cls.group_id == group_id)
        query = query.with_for_update()
        my = await query.gino.first()

        if my:
            await  my.update(money= num).apply()
        else:
            await cls.create( group_id=group_id, money=10000 + num)

    @classmethod
    async def get(cls, group_id: int):
        query = cls.query.where(cls.group_id == group_id)
        query = query.with_for_update()
        my = await query.gino.first()

        if my:
            return my.money
        else:
            await cls.create( group_id=group_id, money=10000)
            return 10000

    
    @classmethod
    async def getLotteryGold(cls, group_id: int):
        query = cls.query.where(cls.group_id == group_id)
        query = query.with_for_update()
        my = await query.gino.first()

        if my:
            return my.welfare_lottery
        else:
            await cls.create( group_id=group_id, welfare_lottery=1000)
            return 1000

    @classmethod
    async def setLotteryGold(cls,  group_id: int, num: int):
        query = cls.query.where(cls.group_id == group_id)
        query = query.with_for_update()
        my = await query.gino.first()

        if my:
            await  my.update(welfare_lottery = num).apply()
        else:
            await cls.create( group_id=group_id, welfare_lottery = 1000 + num)
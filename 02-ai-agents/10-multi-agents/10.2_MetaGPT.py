# 导入所需的库
import re
import fire
from metagpt.actions import Action, UserRequirement
from metagpt.logs import logger
from metagpt.roles import Role
from metagpt.schema import Message
from metagpt.team import Team

# 定义订单处理动作
class ProcessOrder(Action):
    PROMPT_TEMPLATE: str = """
    Process the following order: {order_details}.
    """

    name: str = "ProcessOrder"

    async def run(self, order_details: str):
        prompt = self.PROMPT_TEMPLATE.format(order_details=order_details)
        rsp = await self._aask(prompt)
        return rsp.strip()

# 定义订单处理角色
class OrderProcessor(Role):
    name: str = "OrderProcessor"
    profile: str = "Process orders"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._watch([UserRequirement])
        self.set_actions([ProcessOrder])


# 定义库存管理动作
class ManageInventory(Action):
    PROMPT_TEMPLATE: str = """
    Update inventory based on the following order: {order_details}.
    """

    name: str = "ManageInventory"

    async def run(self, order_details: str):
        prompt = self.PROMPT_TEMPLATE.format(order_details=order_details)
        rsp = await self._aask(prompt)
        return rsp.strip()

# 定义库存管理角色
class InventoryManager(Role):
    name: str = "InventoryManager"
    profile: str = "Manage inventory"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._watch([ProcessOrder])
        self.set_actions([ManageInventory])


# 定义客服处理动作
class HandleCustomerService(Action):
    PROMPT_TEMPLATE: str = """
    Handle the following customer service request: {request_details}.
    """

    name: str = "HandleCustomerService"

    async def run(self, request_details: str):
        prompt = self.PROMPT_TEMPLATE.format(request_details=request_details)
        rsp = await self._aask(prompt)
        return rsp.strip()

# 定义客服处理角色
class CustomerServiceRepresentative(Role):
    name: str = "CustomerServiceRepresentative"
    profile: str = "Handle customer service"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._watch([UserRequirement, ManageInventory])
        self.set_actions([HandleCustomerService])


# 主函数
async def main(
    order_details: str = "A bouquet of red roses",
    investment: float = 3.0,
    n_round: int = 5,
    add_human: bool = False,
):
    logger.info(order_details)

    team = Team()
    team.hire(
        [
            OrderProcessor(),
            InventoryManager(),
            CustomerServiceRepresentative(is_human=add_human),
        ]
    )

    team.invest(investment=investment)
    team.run_project(order_details)
    await team.run(n_round=n_round)

# 执行程序
if __name__ == "__main__":
    fire.Fire(main)

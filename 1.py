# 题目需求1：定义Category类，初始化接收名称作为参数
# 题目需求2：类包含实例属性ledger，是存储事务字典的列表
class Category:
    # 通过__init__构造方法进行类实例初始化
    def __init__(self, name):
        self.name = name  # 保存当前分类的名称，实例属性
        self.ledger = []  # 题目需求2：初始化账本空列表，所有收支记录以字典存入

    # 题目需求3-deposit：存款方法，接收金额、可选描述，描述默认空字符串
    def deposit(self, amount, description=""):
        """存入资金，金额为正数"""
        # 题目需求3：向ledger追加固定格式字典 {"amount":金额, "description":描述}
        self.ledger.append({"amount": amount, "description": description})

    # 题目需求3-check_funds：资金校验方法，供withdraw、transfer调用
    def check_funds(self, amount):
        """判断当前余额是否足够支付指定金额"""
        # 调用get_balance获取当前总余额，对比支出金额
        return amount <= self.get_balance()

    # 题目需求3-withdraw：取款方法，金额存负数，余额充足返回True，不足返回False；描述默认空字符串
    def withdraw(self, amount, description=""):
        """取出资金，金额为负数；如果余额不足则拒绝"""
        # 调用check_funds校验余额是否充足
        if self.check_funds(amount):
            # 余额充足，存入负金额代表支出
            self.ledger.append({"amount": -amount, "description": description})
            return True  # 取款成功返回True（测试点5）
        # 余额不足，取款失败返回False（测试点14）
        return False

    # 题目需求3-get_balance：基于ledger账本计算并返回当前分类总余额
    def get_balance(self):
        """计算当前余额（所有交易金额的代数和）"""
        total = 0  # 初始化余额总和
        # 遍历ledger中所有收支记录，累加amount
        for item in self.ledger:
            total += item["amount"]
        return total

    # 题目需求3-transfer：转账方法，接收金额与目标Category实例
    def transfer(self, amount, other_category):
        """转账：从当前类别取出金额，存入另一个类别"""
        # 先校验自身余额是否足够转出
        if self.check_funds(amount):
            # 当前分类生成转出记录，固定描述 Transfer to [目标名称]（测试点7）
            self.withdraw(amount, f"Transfer to {other_category.name}")
            # 目标分类生成转入记录，固定描述 Transfer from [当前名称]（测试点11）
            other_category.deposit(amount, f"Transfer from {self.name}")
            return True  # 转账成功返回True（测试点8）
        # 余额不足，转账失败返回False（测试点15）
        return False

    # 题目需求4：打印Category对象自动调用__str__，格式化输出固定样式文本
    def __str__(self):
        """返回符合要求的字符串表示（用于print打印实例）"""
        # 1. 标题行：30字符宽度，类别名居中，两侧填充*（题目需求4）
        title = self.name.center(30, "*")
        # 初始化输出字符串，先拼接标题+换行
        output = title + "\n"

        # 2. 循环遍历账本每一条收支记录
        for item in self.ledger:
            # 描述截取前23字符，ljust(23)左对齐补齐23位空格（题目要求描述最多23字符左对齐）
            desc = item["description"][:23].ljust(23)
            # 金额保留两位小数，rjust(7)右对齐占7字符（题目要求金额右对齐7字符、两位小数）
            amt = f"{item['amount']:.2f}".rjust(7)
            # 拼接单行记录，追加换行符
            output += desc + amt + "\n"

        # 3. 拼接底部总额行 Total: 余额
        total = f"Total: {self.get_balance():.2f}"
        output += total
        # 返回完整拼接好的字符串，print(category)自动调用此方法（测试点16）
        return output


# 题目需求5：外部独立函数create_spend_chart，接收类别列表，返回支出百分比条形图字符串
def create_spend_chart(categories):
    # 1. 计算每个类别纯支出总额：仅统计取款负数，取绝对值累加，存款不计入支出
    spent_amounts = []
    for cat in categories:
        spent = 0
        for item in cat.ledger:
            if item["amount"] < 0:          # 判断是取款支出记录
                spent += -item["amount"]    # 负数取绝对值累加支出
        spent_amounts.append(spent)

    # 2. 求和计算所有类别总支出
    total_spent = sum(spent_amounts)

    # 3. 计算每个类别支出占总支出百分比，向下取整到最近10（测试点19）
    percentages = []
    for s in spent_amounts:
        if total_spent > 0:
            raw = (s / total_spent) * 100
            # 整除10再乘10，实现向下取整到10的倍数，如36→30
            p = int(raw) // 10 * 10
        else:
            p = 0
        percentages.append(p)

    # 图表开头固定标题：Percentage spent by category（测试点17）
    chart = "Percentage spent by category\n"

    # 4. Y轴刻度循环：从100到0，步长-10绘制百分比行（测试点18）
    for label in range(100, -1, -10):
        # 左侧刻度数字右对齐占3字符，拼接竖线与空格
        line = str(label).rjust(3) + "| "
        # 遍历每个分类的百分比，绘制条形
        for p in percentages:
            if p >= label:
                line += "o  "   # 有支出百分比：o加两个空格，类别之间天然2空格（测试点20）
            else:
                line += "   "   # 无对应刻度：3空格占位，保证每行宽度统一
        chart += line + "\n"

    # 5. 绘制水平分割线：前置4空格，每个分类3个'-'，末尾多一格横线满足最后条形后额外两空格要求（测试点21）
    chart += "    " + "-" * (len(categories) * 3 + 1) + "\n"

    # 6. 垂直打印类别名称，先获取所有分类名称最长长度
    max_name_len = max(len(cat.name) for cat in categories)

    # 逐字符循环，垂直输出名称
    for i in range(max_name_len):
        line = "     "   # 前置5空格，与左侧刻度对齐
        for cat in categories:
            if i < len(cat.name):
                # 存在当前字符则输出字符+两空格
                line += cat.name[i] + "  "
            else:
                # 名称长度不足，填充3空格占位，保证每行等长
                line += "   "
        chart += line + "\n"

    # 题目需求22：图表末尾不能存在多余换行符，rstrip删除末尾换行再返回
    return chart.rstrip("\n")



import random

class Task():
    def __init__(self):
        self.todolist = ['《入门》项目 1h',
                    '《流畅》看书 1h',
                    'aiyo爬虫教程 2h',
                    '统计学习看书 1h',
                    'LeetCode刷题 1.5h',
                    '数据结构看书 1h',
                    'Excel教程 1h']
        self.todolist2 = {'《入门》项目': '1',
                          '《流畅》看书': '1',
                          'aiyo爬虫教程': '2',
                          '统计学习看书': '1',
                          'LeetCode刷题': '1.5',
                          '数据结构看书': '1'}
        self.finished_task = {'《入门》项目': '10',
                              '《流畅》看书': '10',
                              'aiyo爬虫教程': '10',
                              '统计学习看书': '20',
                              'LeetCode刷题': '20',
                              '数据结构看书': '10'}
        self.finished_percent = {'《入门》项目': 0,
                                '《流畅》看书': 0,
                                'aiyo爬虫教程': 0,
                                '统计学习看书': 0,
                                'LeetCode刷题': 0,
                                '数据结构看书': 0}

    def percent(self,choose_each):
        """每个任务所占的比重"""
        perc = int(self.todolist2[choose_each])/int(self.finished_task[choose_each])
        return perc

    def choose_one(self):
        """每天的计划（不超过5.5h）"""
        rst = []
        hour = 0
        while True:
            task = random.choice(list(self.todolist2))
            each_hour = self.todolist2[str(task)]
            hour += float(each_hour)
            if hour<=5.5:
                self.finished_percent[task]+= self.percent(task)
                rst.append(task)
            else:
                hour-=float(each_hour)
                break
        return rst

    def choose_week(self):
        """每周的计划（五天）"""
        all_rst = []
        for i in range(1,6):
            all_rst.append(self.choose_one())
        return all_rst

task = Task()
print(task.choose_week())
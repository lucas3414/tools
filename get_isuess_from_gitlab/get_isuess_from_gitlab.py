import gitlab
import time
from xlwt import Workbook

bug_levels = ["!", "!!", "!!!", "!!!!"]
bug_types = ["Platform", "Platform_Adapter", "Platform_AP", "Platform_Application", "Platform_Portal",
             "Platform_WeiXin"]
bug_feature = ["feature"]
bug_todos = ["网上问题"]


class BugProgectInfo():

    def __init__(self, url, token):
        self.url = url
        self.token = token

    def get_gitlab_api(self):
        gl = gitlab.Gitlab(self.url, self.token)
        return gl

    def get_project_list(self):
        for i in range(len(self.get_gitlab_api().projects.list())):
            ret = convert_to_dict(self.get_gitlab_api().projects.list()[i])
            project_id = ret['id']
            project_description = ret['description']
            project_name = ret['name_with_namespace']
            print(project_id, project_name, project_description)

    def get_project_info(self, progect_id):
        project = self.get_gitlab_api().projects.get(progect_id)
        return project

    def get_all_list(self, progect_id, **kwargs):
        issue = self.get_project_info(progect_id).issues.list(all=True, **kwargs)
        return issue


def convert_to_dict(obj):
    dict = {}
    dict.update(obj.__dict__)
    return dict['_attrs']


def bug_name_show(key):
    if key == 62:
        name = "无限云"
    elif key == 80:
        name = "出租屋"
    else:
        name = "无限云"
    return name


def bug_levels_show(key):
    if key == "!":
        levels_show = "轻微"
    elif key == "!!":
        levels_show = "一般"
    elif key == "!!!":
        levels_show = "严重"
    elif key == "!!!!":
        levels_show = "致命"
    return levels_show


def bug_types_show(key):
    if key == "Platform":
        levels_show = "平台"
    elif key == "Platform_Adapter":
        levels_show = "适配器"
    elif key == "Platform_AP":
        levels_show = "AP设备"
    elif key == "Platform_Application":
        levels_show = "应用"
    elif key == "Platform_Portal":
        levels_show = "Protal"
    elif key == "Platform_WeiXin":
        levels_show = "微信号"
    return levels_show


def bug_status_show(key):
    if key == "opened":
        status = "打开"
    else:
        status = "关闭"
    return status


def bug_milestone_show(key):
    if key == None:
        milestone = None
    else:
        milestone = key['title']
    return milestone


def create_excle(sheet_name='sheet1', *args, **kwargs):
    book = Workbook(encoding='utf-8')
    sheet1 = book.add_sheet(sheet_name, cell_overwrite_ok=True)
    ret = BugProgectInfo(url, token).get_all_list(id, **kwargs)
    issues_num = len(ret)
    for i in range(len(args[0])):
        sheet1.write(0, i, args[0][i])

    for k in range(issues_num):
        issues_dict = convert_to_dict(ret[k])
        sheet1.write(k + 1, 0, bug_name_show(issues_dict['project_id']))
        sheet1.write(k + 1, 1, issues_dict['iid'])
        sheet1.write(k + 1, 2, issues_dict['title'])
        sheet1.write(k + 1, 3, bug_status_show(issues_dict['state']))
        sheet1.write(k + 1, 4, issues_dict['created_at'])
        sheet1.write(k + 1, 5, bug_milestone_show(issues_dict['milestone']))
        sheet1.write(k + 1, 6, issues_dict['author']['name'])
        tag1 = ""
        tag2 = ""
        tag3 = ""
        tag4 = ""
        for i in range(len(issues_dict['labels'])):
            if issues_dict['labels'][i] in bug_levels:
                tag1 += bug_levels_show(issues_dict['labels'][i]) + ","
                sheet1.write(k + 1, 7, tag1.strip(","))
            elif issues_dict['labels'][i] in bug_types:
                tag2 += bug_types_show(issues_dict['labels'][i]) + ","
                sheet1.write(k + 1, 8, tag2.strip(","))
            elif issues_dict['labels'][i] in bug_feature:
                tag3 += issues_dict['labels'][i] + ","
                sheet1.write(k + 1, 9, tag3.strip(","))
            elif issues_dict['labels'][i] in bug_todos:
                tag4 += issues_dict['labels'][i] + ","
                sheet1.write(k + 1, 10, tag4.strip(","))
    excle_name = time.strftime("%Y-%m-%d", time.localtime()) + "_BugLists.xls"
    book.save(excle_name)
    return excle_name


if __name__ == '__main__':
    # gitlab 服务器的url 以及用户的token
    url = 'http://192.168.1.71'
    token = 'AE5WxZCwd2K25pk2EtU1'
    # 获取全部项目的id 名称 描述
    """
    122 zzt / wlanscope-analysis wlanscope产品线之 网络应用数据分析方案
    117 廖水朱 / wlanscope-analysis wlanscope产品线之 网络应用数据分析方案
    105 云AC / wxEdit 
    62 云AC / test 测试工程
    49 云AC / wlanscope-front 

    """
    BugProgectInfo(url, token).get_project_list()
    # 项目id
    id = 119
    # 生成的buglist中Excel对应的列名称
    list1 = ['项目名', '编号', '标题', '是否关闭', '创建时间', '版本', '作者', '严重度', '类型', '是否是需求', '是否线网问题']
    # 导出的bug的筛选条件 labels：bug，版本：milestone，时间：created_after 等
    # 获取全部的bug单 dict2 = {'labels': ['bug']}
    # 获取单独一个版本的bug单  dict2 = {'labels': ['bug'], 'milestone': 'v1.4.0'}
    # 获取某个时间节点之后的bug单  dict2 = {'labels': ['bug'],  'created_after': '2019-01-24'}
    dict2 = {'labels': ['bug']}
    # bb = BugProgectInfo(url, token).get_all_list(id, **dict2)
    # print(len(bb))
    # 生成bug单列表的Excel
    ret = create_excle('问题列表', list1, **dict2)

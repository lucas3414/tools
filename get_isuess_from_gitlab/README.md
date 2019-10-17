# tools
这是一个小的工具项目


1、get_isuess_from_gitlab
  通过gitlab提供的API接口，可以选择不同项目，不同版本，不同时间，不同类型的isuess拉取到本地，存错到excle中

    # 导出的bug的筛选条件 labels：bug，版本：milestone，时间：created_after 等
    # 获取全部的bug单 dict2 = {'labels': ['bug']}
    # 获取单独一个版本的bug单  dict2 = {'labels': ['bug'], 'milestone': 'v1.4.0'}
    # 获取某个时间节点之后的bug单  dict2 = {'labels': ['bug'],  'created_after': '2019-01-24'}
    
    bug在excle展示：
    
![image](https://github.com/lucas3414/tools/blob/master/get_isuess_from_gitlab/img/bugList.png)


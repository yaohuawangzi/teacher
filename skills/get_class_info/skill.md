---
name: query_class_info
id: query_class_info
description: 查询指定班级的信息，班级人数，学生姓名等
parameters:
  - name: class_id
    description: 班级id
    required: true
    type: string
---

# 班级信息查询
## 什么时候使用
- 当你需要查询指定班级的学生姓名
- 当你需要查询指定班级的学生人数

## 具体方法
### 查询学生的班级的人数
```bash
python3 main.py query_class_info --class_id <class_id>
```



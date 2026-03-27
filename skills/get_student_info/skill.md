---
name: query_student_info
id: query_student_info
description: 查询指定学生的个人信息
parameters:
  - name: student_id
    type: string
    description: 学生的学号
---
# 学生信息查询
## 什么时候使用
- 查询学生的班级
- 查询学生的个人信息
- 查询学生的成绩
- 查询学生的考试安排
- 查询学生的考试成绩
- 查询学生的考试排名

## 具体方法
### 查询学生的班级
执行以下python脚本
```bash
python3 {baseDir}/scrpts/get_student_info.py --student_id <student_id>
```

### 查询学生的成绩
执行以下python脚本
```bash
python3 {baseDir}/scrpts/get_student_info.py  --student_id <student_id>
```

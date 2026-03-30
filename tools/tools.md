---
- id: read_file
  name: 读取文件
  description: 可以读取本地指定文件的内容，（可以读取技能的md文件）
  class: tools.file_read.FileReadTool
  parameters:
    - name: file_path
      description: 文件路径
      required: true
      type: string
      
- id: python_run
  name: 执行python命令
  description: 可以执行python的代码命令
  class: tools.python_run.PythonRunTool
  parameters:
    - name: python_script_cmd
      description: python的执行命令
      required: true
      type: string
    
- id: knowledge_query
  name: 知识库查询
  description: 根据查询文本返回Top命中段
  class: tools.knowledge_query.KnowledgeQueryTool
  parameters:
    - name: query_text
      description: 查询文本
      required: true
      type: string
    - name: top_k
      description: 返回条数
      required: false
      type: integer
    - name: where
      description: 过滤条件
      required: false
      type: object
---

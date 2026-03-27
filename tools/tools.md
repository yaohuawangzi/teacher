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
    - name:
---
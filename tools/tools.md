---
- id: read_file
  name: 读取文件
  description: 可以读取本地指定文件的内容
  file: ./read_file.py
  parameters:
    - name: file_path
      description: 文件路径
      required: true
      type: string
---
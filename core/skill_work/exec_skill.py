# import os
# import re
# import tempfile
# import subprocess
# import json
# from typing import Dict, Any, Union
#
#
# def load_skill_code_from_md(skill_id: str, skills_dir: str = "skills") -> str:
#     """
#     从 skill.md 中提取 Python 代码块
#     :param skill_id: 技能ID（对应文件夹名）
#     :return: 提取的代码字符串
#     """
#     skill_dir = os.path.join(skills_dir, skill_id)
#     skill_md = os.path.join(skill_dir, "skill.md")
#
#     if not os.path.exists(skill_md):
#         raise FileNotFoundError(f"技能 {skill_id} 的 MD 文件不存在：{skill_md}")
#
#     # 读取 MD 文件
#     with open(skill_md, "r", encoding="utf-8") as f:
#         content = f.read()
#
#     # 提取 ```python ``` 包裹的代码块
#     code_blocks = re.findall(r"```python\n(.*?)```", content, re.DOTALL)
#     if not code_blocks:
#         raise ValueError(f"技能 {skill_id} 的 MD 文件中未找到 Python 代码块")
#
#     # 返回第一个代码块（主执行逻辑）
#     return code_blocks[0]
#
#
# def execute_skill(skill_id: str, params: Dict[str, Any], skills_dir: str = "skills") -> Union[float, str, Dict]:
#     """
#     超进阶版：从 MD 文件加载代码并执行
#     """
#     # 1. 提取 MD 中的代码
#     code = load_skill_code_from_md(skill_id, skills_dir)
#
#     # 2. 生成临时 Python 文件（避免污染本地文件）
#     with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8") as f:
#         # 把参数注入代码（生成调用逻辑）
#         code += f"""
# # 自动注入参数并执行
# if __name__ == "__main__":
#     import json
#     params = {json.dumps(params, ensure_ascii=False)}
#     # 假设 MD 中的代码定义了 run() 函数
#     try:
#         result = run(params)
#         print(json.dumps({{"success": True, "result": result}}, ensure_ascii=False))
#     except Exception as e:
#         print(json.dumps({{"success": False, "error": str(e)}}, ensure_ascii=False))
# """
#         temp_file = f.name
#
#     try:
#         # 3. 执行临时文件（子进程运行，安全隔离）
#         result = subprocess.run(
#             ["python3", temp_file],
#             capture_output=True,
#             text=True,
#             timeout=10  # 超时控制
#         )
#
#         # 4. 解析执行结果
#         if result.returncode != 0:
#             raise RuntimeError(f"技能 {skill_id} 执行失败：{result.stderr}")
#
#         output = json.loads(result.stdout.strip())
#         if not output["success"]:
#             raise ValueError(f"技能 {skill_id} 执行出错：{output['error']}")
#
#         return output["result"]
#
#     finally:
#         # 5. 删除临时文件
#         os.unlink(temp_file)
#
#
# # ========== 配套的 skill.md 示例（skills/math-add/skill.md） ==========
# """
# ---
# name: 数字相加
# skill_id: math-add
# parameters:
#   - name: a
#     type: number
#   - name: b
#     type: number
# ---
#
# # 数字相加技能
# ```python
# def run(params):
#     \"\"\"MD 中定义的主执行函数\"\"\"
#     a = float(params["a"])
#     b = float(params["b"])
#     return a + b
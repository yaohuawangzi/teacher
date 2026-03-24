# tools/file_read.py
import os
import sys
from typing import Dict, Optional, Any

def file_read(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    OpenClaw 核心 file_read 工具（Python 版）
    功能：安全读取本地文件内容，返回结构化结果
    :param params: 入参字典，必须包含 filePath，可选 encoding、max_size
                   - filePath: 目标文件路径（相对/绝对）
                   - encoding: 文件编码，默认 utf-8
                   - max_size: 最大读取字节数，默认 10MB（防止读取超大文件）
    :return: 结构化结果字典
             - success: bool，是否读取成功
             - content: str|None，文件内容（成功时返回）
             - error: str|None，错误信息（失败时返回）
             - path: str，解析后的绝对路径（便于排查）
    """
    # 1. 初始化默认返回值
    result: Dict[str, Any] = {
        "success": False,
        "content": None,
        "error": None,
        "path": None
    }

    # 2. 必选参数校验
    if "filePath" not in params or not params["filePath"]:
        result["error"] = "参数错误：缺少必填项 filePath"
        return result

    # 3. 解析入参（设置默认值）
    raw_path = params["filePath"]
    encoding = params.get("encoding", "utf-8")
    max_size = params.get("max_size", 10 * 1024 * 1024)  # 默认10MB

    # 4. 路径处理：转为绝对路径，解决相对路径歧义
    try:
        abs_path = os.path.abspath(raw_path)
        result["path"] = abs_path
    except Exception as e:
        result["error"] = f"路径解析失败：{str(e)}"
        return result

    # 5. 安全校验：限制读取范围（核心！防止LLM读取系统敏感文件）
    # 定义 OpenClaw 允许读取的根目录（可根据实际部署调整）
    allowed_roots = [
        os.path.abspath("./skills"),    # OpenClaw 的技能文件目录
        os.path.abspath("./src"),       # OpenClaw 源码目录
        os.path.abspath("./data")       # 数据目录
    ]
    # 检查目标文件是否在允许的目录内
    is_allowed = any(abs_path.startswith(root) for root in allowed_roots)
    if not is_allowed:
        result["error"] = (
            f"安全限制：禁止读取非授权目录的文件\n"
            f"目标路径：{abs_path}\n"
            f"允许目录：{allowed_roots}"
        )
        return result

    # 6. 检查文件是否存在且是普通文件（排除目录、管道等）
    if not os.path.exists(abs_path):
        result["error"] = f"文件不存在：{abs_path}"
        return result
    if not os.path.isfile(abs_path):
        result["error"] = f"路径不是普通文件：{abs_path}"
        return result

    # 7. 检查文件大小（防止读取超大文件导致内存溢出）
    file_size = os.path.getsize(abs_path)
    if file_size > max_size:
        result["error"] = (
            f"文件过大：{abs_path}\n"
            f"文件大小：{file_size/1024/1024:.2f}MB，最大允许：{max_size/1024/1024:.2f}MB"
        )
        return result

    # 8. 读取文件内容（处理编码兼容和异常）
    try:
        with open(abs_path, "r", encoding=encoding) as f:
            content = f.read()
        result["success"] = True
        result["content"] = content
        result["error"] = None
    except UnicodeDecodeError:
        # 编码错误时，尝试用 GBK/GB2312（兼容中文Windows文件）
        try:
            with open(abs_path, "r", encoding="gbk") as f:
                content = f.read()
            result["success"] = True
            result["content"] = content
            result["error"] = None
        except Exception as e:
            result["error"] = f"编码解析失败（已尝试 {encoding}/gbk）：{str(e)}"
    except PermissionError:
        result["error"] = f"权限不足：无法读取 {abs_path}（需要读权限）"
    except Exception as e:
        result["error"] = f"读取文件失败：{str(e)}"

    return result

# ------------------------------
# 测试用例（直接运行该文件即可验证）
# ------------------------------
if __name__ == "__main__":
    # 测试1：读取合法文件（先创建测试文件）
    test_dir = "./skills"
    os.makedirs(test_dir, exist_ok=True)
    test_file = os.path.join(test_dir, "test_skill.md")
    with open(test_file, "w", encoding="utf-8") as f:
        f.write("# 测试Skill\n这是OpenClaw的测试技能文件")

    # 调用工具读取测试文件
    test_params1 = {"filePath": test_file}
    res1 = file_read(test_params1)
    print("测试1 - 读取合法文件：")
    print(f"结果：{res1}\n")

    # 测试2：读取非授权文件（如系统hosts文件）
    test_params2 = {"filePath": "/etc/hosts"}  # Windows: "C:\Windows\System32\drivers\etc\hosts"
    res2 = file_read(test_params2)
    print("测试2 - 读取非授权文件：")
    print(f"结果：{res2}\n")

    # 测试3：读取不存在的文件
    test_params3 = {"filePath": "./skills/nonexist.md"}
    res3 = file_read(test_params3)
    print("测试3 - 读取不存在的文件：")
    print(f"结果：{res3}")
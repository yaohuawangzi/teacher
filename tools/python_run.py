import sys
import subprocess
from .base_tools import BaseTool, ToolResult
from typing import Dict, Optional, Any
import shlex


class PythonRunTool(BaseTool):
    def execute(params: Dict[str, Any]) -> ToolResult:
        result = ToolResult(success=False)
        if "python_script_cmd" not in params or not params["python_script_cmd"]:
            result.error = "参数错误：缺少必填项 python_script_cmd"
            return result

        python_run_cmd = params.get("python_script_cmd", "")

        if not python_run_cmd:
            result.error = "命令不能为空"
            return result

        try:
            # 安全拆分命令（处理带引号的参数）
            cmd = shlex.split(python_run_cmd)
            # 执行命令
            res = subprocess.run(
                args=cmd,
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=30  # ✅ 新增超时保护，避免死锁
            )
            # 处理执行结果
            if res.returncode == 0:
                result.success = True
                result.data = res.stdout
                result.message = "执行成功"
            else:
                result.error = res.stderr
                result.message = f"执行失败，退出码: {res.returncode}"
        except subprocess.TimeoutExpired:
            result.error = "执行超时"
        except Exception as e:
            result.error = f"执行异常: {str(e)}"
        return result



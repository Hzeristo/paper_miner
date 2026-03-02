#!/usr/bin/env python3
"""
keep_awake.py - 阻止Windows系统进入睡眠状态（带状态输出）
用法: python keep_awake.py
保持运行即可，按 Ctrl+C 退出并恢复系统睡眠策略。
"""

import ctypes
import time
import sys
from datetime import datetime

# 定义Windows API常量
ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001
ES_DISPLAY_REQUIRED = 0x00000002


class WindowsKeepAwake:
    """一个优雅的阻止睡眠的上下文管理器"""

    def __init__(self, keep_display_on=False):
        """
        初始化
        :param keep_display_on: 是否同时阻止显示器关闭
        """
        self.kernel32 = ctypes.windll.kernel32
        self.flags = ES_CONTINUOUS | ES_SYSTEM_REQUIRED
        if keep_display_on:
            self.flags |= ES_DISPLAY_REQUIRED
        self._previous_state = None

    def __enter__(self):
        """进入上下文，设置线程执行状态"""
        self._previous_state = self.kernel32.SetThreadExecutionState(self.flags)
        if not self._previous_state:
            print("⚠️  警告: 无法设置执行状态。程序将继续，但可能无法阻止睡眠。")
        else:
            action = "系统和显示器" if (self.flags & ES_DISPLAY_REQUIRED) else "系统"
            print(f"🛡️  已阻止{action}进入睡眠状态。")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文，恢复之前的执行状态"""
        if self._previous_state:
            self.kernel32.SetThreadExecutionState(ES_CONTINUOUS)
            print("✅ 已恢复系统睡眠策略。")

    def keep_alive(self):
        """可供外部调用的保持激活的方法"""
        self.kernel32.SetThreadExecutionState(self.flags)
        return True


def main():
    """主函数：阻止睡眠，直到用户按下 Ctrl+C"""
    print("🚀 Keep-Awake 守护进程已启动")
    print("📌 本进程正在阻止系统睡眠，以便后台任务持续运行。")
    print("📌 按 Ctrl + C 可安全退出并恢复系统正常睡眠策略。")
    print("-" * 50)

    try:
        # 使用上下文管理器，确保即使异常退出也能恢复
        with WindowsKeepAwake(keep_display_on=False) as keeper:
            loop_count = 0
            while True:
                # 每60秒输出一次状态
                loop_count += 1
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                status = keeper.keep_alive()  # 重置系统空闲计时器

                if status:
                    print(f"[{current_time}] 保持唤醒状态 | 已运行 {loop_count} 个周期")
                else:
                    print(f"[{current_time}] ⚠️  状态更新失败")

                # 休眠300秒
                time.sleep(300)

    except KeyboardInterrupt:
        print("\n👋 用户中断，正在退出...")
    except Exception as e:
        print(f"\n💥 发生未知错误: {e}")
    finally:
        print("守护进程已停止。")
        sys.exit(0)


if __name__ == "__main__":
    main()

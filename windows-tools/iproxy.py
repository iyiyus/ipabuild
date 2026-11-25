"""iproxy 的 Windows 等价实现（基于 pymobiledevice3）。

native_ssh.py 调用 `iproxy -u <udid> <本地端口>:22` 建立 USB→SSH 端口转发。
参数格式与 libimobiledevice 的 iproxy 兼容：
  iproxy -u <udid> 2222:22
  iproxy 2222:22          （单设备时可省略 -u）
转发会一直运行直到进程被终止（与原版一致）。
"""

import subprocess
import sys


def main() -> None:
    args = sys.argv[1:]
    src_port = None
    dst_port = None

    # 解析 "本地端口:设备端口"（原版还支持多组映射，这里只用一组就够）
    for arg in args:
        if ":" in arg:
            left, right = arg.split(":", 1)
            if left.isdigit() and right.isdigit():
                src_port, dst_port = left, right
    if src_port is None:
        print("usage: iproxy [-u <udid>] <local_port>:<device_port>", file=sys.stderr)
        sys.exit(1)

    result = subprocess.run(
        [sys.executable, "-m", "pymobiledevice3", "usbmux", "forward", src_port, dst_port],
    )
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()

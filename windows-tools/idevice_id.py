"""idevice_id 的 Windows 等价实现（基于 pymobiledevice3）。

retrieve.py 调用 `idevice_id -l` 获取 USB 连接的设备 UDID 列表。
用法与 libimobiledevice 的 idevice_id 保持一致：
  idevice_id -l   列出通过 USB 连接的设备 UDID（每行一个）
"""

import json
import subprocess
import sys


def main() -> None:
    if "-l" not in sys.argv and "-n" not in sys.argv:
        print("usage: idevice_id [-l|-n]", file=sys.stderr)
        sys.exit(1)
    out = subprocess.run(
        [sys.executable, "-m", "pymobiledevice3", "usbmux", "list"],
        capture_output=True, text=True, check=True, timeout=30,
    ).stdout
    devices = json.loads(out)
    for item in devices:
        udid = item.get("UniqueDeviceID") or item.get("Identifier")
        if udid:
            print(udid)


if __name__ == "__main__":
    main()

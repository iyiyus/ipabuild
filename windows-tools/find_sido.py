"""在设备上定位 IC-Info.sido 与 FairPlay 相关文件。"""

import paramiko

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect('127.0.0.1', 2222, username='root', password='yuchen',
          timeout=8, allow_agent=False, look_for_keys=False)

CMDS = [
    # 全盘搜 FairPlay 目录与 IC-Info.sido
    'find /private/var/mobile/Library/FairPlay -maxdepth 4 2>/dev/null | head -20',
    'find /private/var -name "IC-Info.sido" 2>/dev/null | head -5',
    'ls /private/var/mobile/Library/ | grep -i fair',
    # 设备上是否有已装 App Store 应用（看 FairPlay 是否被使用过）
    'find /private/var/containers/Bundle/Application -maxdepth 2 -name "*.app" 2>/dev/null | head -5',
    'ls /private/var/mobile/Library/FairPlay 2>&1',
]

for cmd in CMDS:
    _, out, err = c.exec_command(cmd, timeout=30)
    print('$ ' + cmd[:70])
    print(out.read().decode(errors='replace')[:900])
    e = err.read().decode(errors='replace')[:200]
    if e.strip():
        print('[stderr]', e)
    print('---')
c.close()

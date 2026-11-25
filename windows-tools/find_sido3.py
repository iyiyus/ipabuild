"""在 /rootfs（真实数据分区）下找 FairPlay 数据。"""

import paramiko

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect('127.0.0.1', 2222, username='root', password='yuchen',
          timeout=8, allow_agent=False, look_for_keys=False)

CMDS = [
    'ls -la /rootfs/ 2>&1 | head -10',
    'ls /rootfs/private/var/mobile/Library/FairPlay 2>&1',
    'find /rootfs/private/var/mobile/Library/FairPlay -maxdepth 5 2>/dev/null | head -15',
    'find /rootfs/private/var -name "IC-Info.sido" 2>/dev/null | head -5',
    # 对比：SSH 会话内 /var/mobile/Library 与 /rootfs 下的是否同一目录
    'ls -i /var/mobile/Library/ /rootfs/private/var/mobile/Library/ 2>/dev/null | head -8',
]

for cmd in CMDS:
    _, out, err = c.exec_command(cmd, timeout=60)
    print('$ ' + cmd[:70])
    print(out.read().decode(errors='replace')[:900])
    e = err.read().decode(errors='replace')[:150]
    if e.strip():
        print('[stderr]', e)
    print('---')
c.close()

"""检查设备已装应用中的 FairPlay SINF 许可数据（SC_Info）。"""

import paramiko

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect('127.0.0.1', 2222, username='root', password='yuchen',
          timeout=8, allow_agent=False, look_for_keys=False)

CMDS = [
    # App Store 安装的应用目录里带 SC_Info（FairPlay 许可）
    'find /rootfs/private/var/containers/Bundle/Application -maxdepth 3 -name "SC_Info" 2>/dev/null | head -10',
    'find /rootfs/private/var/containers/Bundle/Application -maxdepth 4 -name "*.sinf" 2>/dev/null | head -10',
    # 也看看应用容器里哪些是 .app（列出所有，好判断哪些是 App Store 装的）
    'ls /rootfs/private/var/containers/Bundle/Application 2>/dev/null | head -20',
    # App Store 登录账号线索
    'find /rootfs/private/var/mobile/Library/Accounts -maxdepth 3 -name "*.accounts*" 2>/dev/null | head -5',
]

for cmd in CMDS:
    _, out, err = c.exec_command(cmd, timeout=60)
    print('$ ' + cmd[:70])
    print(out.read().decode(errors='replace')[:1000])
    e = err.read().decode(errors='replace')[:150]
    if e.strip():
        print('[stderr]', e)
    print('---')
c.close()

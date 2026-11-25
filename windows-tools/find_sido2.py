"""RootHide 布局下进一步探测 FairPlay 数据与 jbroot 环境。"""

import paramiko

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect('127.0.0.1', 2222, username='root', password='yuchen',
          timeout=8, allow_agent=False, look_for_keys=False)

CMDS = [
    'command -v jbroot; ls /var/jb 2>/dev/null | head -5',
    'ls /var/mobile/Library/ | head -40',
    'ls /var/mobile/Media/iTunes_Control 2>&1 | head -5',
    'find /var/mobile/Library -maxdepth 1 -iname "*fair*" -o -maxdepth 1 -iname "*itunes*" 2>/dev/null',
    'mount | grep -iE "fair|mobile" | head -5',
    'ls /var/root/Library/FairPlay 2>&1',
    'find /var/root -maxdepth 4 -name "IC-Info.sido" 2>/dev/null',
]

for cmd in CMDS:
    _, out, err = c.exec_command(cmd, timeout=30)
    print('$ ' + cmd[:70])
    print(out.read().decode(errors='replace')[:900])
    e = err.read().decode(errors='replace')[:150]
    if e.strip():
        print('[stderr]', e)
    print('---')
c.close()

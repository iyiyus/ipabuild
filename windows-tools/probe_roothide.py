"""探测 RootHide 隐藏机制与 FairPlay 真实可见性。"""

import paramiko

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect('127.0.0.1', 2222, username='root', password='yuchen',
          timeout=8, allow_agent=False, look_for_keys=False)

CMDS = [
    'ls /usr/bin/roothide /usr/sbin/roothide /var/jb/usr/bin/roothide 2>&1; command -v roothide',
    'jbroot 2>&1 | head -3',
    'ls /var/mobile/Library/Accounts /var/mobile/Library/Safari 2>&1 | head -4',
    'stat /var/mobile/Library/FairPlay 2>&1',
    'ls -la /var/mobile/ | head -20',
    'cat /var/jb/bootstrap.plist 2>/dev/null | head; ls /var/jb/usr/bin 2>/dev/null | head -20',
]

for cmd in CMDS:
    _, out, err = c.exec_command(cmd, timeout=30)
    print('$ ' + cmd[:70])
    print(out.read().decode(errors='replace')[:700])
    e = err.read().decode(errors='replace')[:150]
    if e.strip():
        print('[stderr]', e)
    print('---')
c.close()

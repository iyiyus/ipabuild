"""诊断设备 sshd 配置与 .ssh 目录权限（一次性脚本）。"""

import paramiko

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect('127.0.0.1', 2222, username='root', password='yuchen',
          timeout=8, allow_agent=False, look_for_keys=False)

CMDS = [
    'which sshd; ps -ef | grep -i sshd | grep -v grep',
    'ls -la /var/root/ /var/root/.ssh/ 2>&1',
    'cat /var/root/.ssh/authorized_keys',
    'grep -iE "pubkey|strictmodes|authorizedkeysfile|passwordauth" /etc/ssh/sshd_config 2>/dev/null | grep -v "^#" | head -20',
    'ls /etc/ssh/sshd_config.d/ 2>/dev/null; grep -riE "pubkey|strictmodes" /etc/ssh/sshd_config.d/ 2>/dev/null | head',
]

for cmd in CMDS:
    _, out, err = c.exec_command(cmd, timeout=10)
    print('$ ' + cmd)
    print(out.read().decode(errors='replace')[:800])
    e = err.read().decode(errors='replace')[:200]
    if e:
        print('[stderr]', e)
    print('---')
c.close()

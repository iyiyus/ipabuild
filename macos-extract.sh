#!/bin/bash
# ============================================================================
# macos-extract.sh —— 在 Mac 上一键提取 FairPlay 凭证（credential.bin）
# ----------------------------------------------------------------------------
# 用途：zake 砸壳平台需要每个 Apple 账号一个 16 字节 FairPlay 凭证，
#       只能在「Mac + 已越狱 iOS 设备」上提取一次，之后 Windows/Linux
#       服务器可长期复用，无需再连设备。
#
# 前提条件：
#   1. 本机已安装 Xcode（xcodebuild 可用）或至少 Command Line Tools
#   2. 一台已越狱的 iPhone/iPad（iOS 10+），用 USB 线连接本机
#   3. 设备上已安装至少一个 App Store 应用（用目标 Apple 账号购买的）
#   4. 设备已与本机配对并信任（弹窗点信任）
#
# 使用：
#   1. 把整个 fairplay-decrypt-main 目录拷到 Mac
#   2. cd fairplay-decrypt-main && chmod +x macos-extract.sh && ./macos-extract.sh
#   3. 成功后输出目录里有 credential.bin —— 把它拷回 Windows，
#      在管理端「IPA 砸壳 → Apple 账号 → 上传凭证」上传给对应账号
#
# 可选参数：
#   ./macos-extract.sh /path/to/app.ipa   指定某个应用的 ipa（多账号时用来
#                                          选定账号；设备上仍需装着该账号的应用）
# ============================================================================

set -e
cd "$(dirname "$0")"

echo "==> [1/4] 检查依赖（Xcode 工具链 / ldid / libimobiledevice）"
# ldid 和 libimobiledevice（idevice_id/iproxy）缺失时自动用 Homebrew 安装
if ! command -v ldid >/dev/null 2>&1 || ! command -v idevice_id >/dev/null 2>&1; then
  echo "    缺少 ldid 或 libimobiledevice，尝试通过 Homebrew 安装..."
  if ! command -v brew >/dev/null 2>&1; then
    echo "错误：未安装 Homebrew，请先安装：https://brew.sh" >&2
    exit 1
  fi
  brew install ldid libimobiledevice
fi

echo "==> [2/4] 确认设备连接"
# 列出通过 USB 连接并已配对的设备；没有则终止
DEVICES=$(idevice_id -l 2>/dev/null || true)
if [ -z "$DEVICES" ]; then
  echo "错误：未检测到已配对的 iOS 设备。" >&2
  echo "      请用 USB 线连接已越狱设备，解锁屏幕并在弹窗中点「信任」。" >&2
  exit 1
fi
echo "    已连接设备: $DEVICES"

echo "==> [3/4] 编译注入组件（需要 Xcode 工具链，首次约 1-2 分钟）"
make

echo "==> [4/4] 提取凭证（脚本会通过 USB SSH 连接设备，保持解锁状态）"
OUT="$HOME/Desktop/zake-credential-$(date +%Y%m%d-%H%M%S)"
if [ -n "$1" ]; then
  # 传了 --ipa 参数：指定用某个应用的许可提取（多账号场景）
  echo "    指定 IPA: $1"
  python3 credential-retrieval/retrieve.py --output-dir "$OUT" --ipa "$1"
else
  python3 credential-retrieval/retrieve.py --output-dir "$OUT"
fi

echo ""
echo "============================================================"
echo "✅ 提取成功！凭证文件位于:"
echo "   $OUT/credential.bin"
echo ""
echo "下一步：把这个文件拷回 Windows（微信/AirDrop/网盘均可），"
echo "       打开管理端「IPA 砸壳 → Apple 账号」→ 对应账号点「上传凭证」。"
echo "注意：凭证与 Apple 账号一一绑定，换账号要重新提取。"
echo "============================================================"

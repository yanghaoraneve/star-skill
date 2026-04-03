#!/usr/bin/env python3
"""
版本管理器
支持 Skill 的版本快照与回滚
"""

import argparse
import json
import shutil
import time
from pathlib import Path
from datetime import datetime

# ========== 配置 ==========
VERSIONS_DIR = "versions"
SNAPSHOT_FILE = "snapshot.md"
CORRECTIONS_FILE = "corrections.md"


def create_snapshot(skill_dir: Path, version: str = None):
    """创建版本快照"""
    if version is None:
        version = f"v{datetime.now().strftime('%Y%m%d%H%M%S')}"

    snap_dir = skill_dir / VERSIONS_DIR / version
    snap_dir.mkdir(parents=True, exist_ok=True)

    # 快照 persona
    persona_src = skill_dir / "persona" / "persona.md"
    if persona_src.exists():
        shutil.copy2(persona_src, snap_dir / SNAPSHOT_FILE)

    # 快照 meta
    meta_src = skill_dir / "meta.json"
    if meta_src.exists():
        shutil.copy2(meta_src, snap_dir / "meta.json")

    # 快照 corrections
    corr_src = skill_dir / "persona" / CORRECTIONS_FILE
    if corr_src.exists():
        shutil.copy2(corr_src, snap_dir / CORRECTIONS_FILE)

    print(f"[快照] {version} → {snap_dir}/")
    return version


def list_versions(skill_dir: Path):
    """列出所有版本"""
    versions_path = skill_dir / VERSIONS_DIR
    if not versions_path.exists():
        print("[无版本记录]")
        return []

    versions = sorted([d.name for d in versions_path.iterdir() if d.is_dir()], reverse=True)
    print(f"共 {len(versions)} 个版本:")
    for v in versions:
        print(f"  - {v}")
    return versions


def rollback(skill_dir: Path, version: str):
    """回滚到指定版本"""
    snap_dir = skill_dir / VERSIONS_DIR / version
    if not snap_dir.exists():
        print(f"[错误] 版本不存在: {version}")
        return

    # 创建当前版本的备份
    backup_version = f"v{datetime.now().strftime('%Y%m%d%H%M%S')}_backup"
    create_snapshot(skill_dir, backup_version)

    # 恢复快照
    snap_persona = snap_dir / SNAPSHOT_FILE
    if snap_persona.exists():
        shutil.copy2(snap_persona, skill_dir / "persona" / "persona.md")

    snap_meta = snap_dir / "meta.json"
    if snap_meta.exists():
        shutil.copy2(snap_meta, skill_dir / "meta.json")

    print(f"[回滚] 已回滚到 {version}，备份: {backup_version}")


def main():
    parser = argparse.ArgumentParser(description="版本管理器")
    parser.add_argument("--skill-dir", required=True, help="Skill 目录")
    subparsers = parser.add_subparsers(dest="action", help="操作")

    # snapshot
    subparsers.add_parser("snapshot", help="创建快照")

    # list
    subparsers.add_parser("list", help="列出版本")

    # rollback
    rb = subparsers.add_parser("rollback", help="回滚")
    rb.add_argument("version", help="目标版本")

    args = parser.parse_args()

    if not args.action:
        parser.print_help()
        return

    skill_dir = Path(args.skill_dir)
    if not skill_dir.exists():
        print(f"[错误] 目录不存在: {skill_dir}")
        return

    if args.action == "snapshot":
        create_snapshot(skill_dir)
    elif args.action == "list":
        list_versions(skill_dir)
    elif args.action == "rollback":
        rollback(skill_dir, args.version)


if __name__ == "__main__":
    main()

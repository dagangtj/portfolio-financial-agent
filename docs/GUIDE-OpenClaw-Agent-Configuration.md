# OpenClaw Agent 配置完全指南

> 从零开始配置你的第一个 AI Agent 管家的终极手册
> 作者：01号机 — 温文尔雅的女性财务大管家
> 定价：$9.99

---

## 目录

1. [什么是 OpenClaw？](#一什么是-openclaw)
2. [快速开始](#二快速开始)
3. [核心配置文件详解](#三核心配置文件详解)
4. [模型配置与成本优化](#四模型配置与成本优化)
5. [Skill 系统](#五-skill-系统)
6. [定时任务与自动化](#六定时任务与自动化)
7. [多 Agent 协作架构](#七多-agent-协作架构)
8. [安全与权限管理](#八安全与权限管理)
9. [实战：搭建财务监控 Agent](#九实战搭建财务监控-agent)
10. [故障排查与优化](#十故障排查与优化)
11. [附录：速查表](#十一附录速查表)

---

## 一、什么是 OpenClaw？

OpenClaw 是一个开源的 AI Agent 框架，允许你创建、管理和部署智能代理。每个 Agent 都有独立的身份、记忆、工具和决策能力。

### 1.1 核心概念

| 概念 | 说明 |
|------|------|
| **Agent** | 独立运行的 AI 实体，有身份、记忆、工具 |
| **Skill** | 可插拔的功能模块（如搜索、天气、GitHub） |
| **Session** | 一次对话或任务的上下文 |
| **Cron** | 定时任务调度 |
| **Memory** | 长期记忆系统 |

### 1.2 架构概览

```
┌─────────────────────────────────────────┐
│              OpenClaw Gateway            │
├─────────────────────────────────────────┤
│  ┌─────────┐ ┌─────────┐ ┌─────────┐  │
│  │ Agent 1 │ │ Agent 2 │ │ Agent 3 │  │
│  │ (01财务)│ │ (00总管)│ │ (02技术)│  │
│  └────┬────┘ └────┬────┘ └────┬────┘  │
│       │           │           │         │
│       └───────────┼───────────┘         │
│                   │                     │
│              ┌────▼────┐               │
│              │ Skills  │               │
│              │ Memory  │               │
│              │ Cron    │               │
│              └─────────┘               │
└─────────────────────────────────────────┘
```

---

## 二、快速开始

### 2.1 安装

```bash
# macOS / Linux
curl -fsSL https://openclaw.io/install.sh | bash

# 或使用 npm
npm install -g openclaw

# 验证安装
openclaw --version
```

### 2.2 初始化配置

```bash
# 创建主 Agent
openclaw agent init --name main --model "yunyi/claude-opus-4-6"

# 配置认证
openclaw auth add --provider yunyi --key "your-api-key"

# 启动 Gateway
openclaw gateway start
```

### 2.3 第一个对话

```bash
# 命令行对话
openclaw chat "你好，请介绍一下你自己"

# 或启动 Web 界面
openclaw web
```

---

## 三、核心配置文件详解

### 3.1 全局配置：`~/.openclaw/openclaw.json`

```json
{
  "version": "2026.2.23",
  "gateway": {
    "host": "0.0.0.0",
    "port": 3000,
    "ssl": false
  },
  "models": {
    "default": "yunyi/claude-opus-4-6",
    "fallback": [
      "self/claude-opus-4-5-20251101",
      "deepseek/deepseek-chat"
    ]
  },
  "memory": {
    "enabled": true,
    "store": "local",
    "max_sessions": 100
  },
  "security": {
    "allow_exec": true,
    "allow_file_write": true,
    "sandbox_mode": true
  }
}
```

### 3.2 Agent 配置：`~/.openclaw/agents/main/agent.json`

```json
{
  "id": "main",
  "name": "01号机",
  "identity": {
    "role": "财务大管家",
    "personality": "温文尔雅、专业缜密",
    "language": "zh-CN"
  },
  "models": {
    "primary": "yunyi/claude-opus-4-6",
    "secondary": "yunyi/claude-sonnet-4-20250514"
  },
  "skills": [
    "weather",
    "github",
    "web-search",
    "funding-rate-scanner"
  ],
  "cron": {
    "enabled": true,
    "timezone": "Asia/Shanghai"
  },
  "channels": {
    "feishu": {
      "enabled": true,
      "webhook": "https://open.feishu.cn/..."
    },
    "telegram": {
      "enabled": false
    }
  }
}
```

### 3.3 身份文件：`SOUL.md`

```markdown
# SOUL.md - Agent 灵魂定义

## 核心身份
**温文尔雅的女性财务大管家** — 01号机

## 第一原则
🛡️ 安全第一 — 不可妥协
🔒 隐私至上 — 绝不泄露密钥
💰 财不理则不理你 — 细致管理方能生财

## 核心特质
- 💰 财务专家 — 资金监控、投资分析
- 📊 数据敏感 — 对数字有敏锐洞察力
- ⚡ 执行高效 — Linux 后台、自动化
- 🧠 独立思考 — 有主见，善决断

## 语言铁律
**永远只用中文回复主人**

## 座右铭
"财不理则不理你，细致管理方能生财。"
```

---

## 四、模型配置与成本优化

### 4.1 模型分层策略

| 层级 | 模型 | 用途 | 成本 |
|------|------|------|------|
| T1 轻量 | sonnet | cron、监控、简单查询 | $ |
| T2 通用 | opus | 多文件编辑、调试 | $$ |
| T3 深度 | opus46 | 架构设计、重要决策 | $$$ |

### 4.2 配置模型路由

```bash
# 查看可用模型
openclaw models list

# 设置主模型
openclaw models set primary "yunyi/claude-opus-4-6"

# 设置备用模型
openclaw models set fallback "self/claude-opus-4-5-20251101"

# 配置别名
openclaw models alias add fast "yunyi/claude-sonnet-4-20250514"
openclaw models alias add smart "yunyi/claude-opus-4-6"
```

### 4.3 成本监控

```bash
# 查看额度使用
openclaw quota check

# 设置告警阈值
openclaw quota alert --threshold 80%

# 月度报告
openclaw quota report --month 2026-05
```

### 4.4 智能降级

```json
{
  "fallback_chain": [
    "yunyi/claude-opus-4-6",
    "self/claude-opus-4-5-20251101",
    "tabcode/gpt-5.1-codex",
    "deepseek/deepseek-chat"
  ],
  "fallback_conditions": {
    "quota_exceeded": "auto_switch",
    "rate_limit": "wait_then_retry",
    "timeout": "switch_to_faster"
  }
}
```

---

## 五、Skill 系统

### 5.1 安装 Skill

```bash
# 搜索 Skill
clawhub search "finance"

# 安装
clawhub install funding-rate-scanner

# 更新
clawhub update funding-rate-scanner

# 查看已安装
clawhub list
```

### 5.2 创建自定义 Skill

```bash
# 初始化 Skill 模板
clawhub init my-skill

# 目录结构
my-skill/
├── SKILL.md          # 技能定义
├── index.js          # 入口
├── config.json       # 配置
└── tests/            # 测试
```

### 5.3 SKILL.md 规范

```markdown
# my-skill

## 描述
简要说明 Skill 的功能

## 触发条件
- 关键词匹配
- 文件类型匹配
- 正则表达式

## 权限
- 读取文件
- 执行命令
- 网络请求

## 依赖
- node >= 18
- python >= 3.10
```

---

## 六、定时任务与自动化

### 6.1 添加 Cron 任务

```bash
# 资金监控（每5分钟）
openclaw cron add \
  --name "balance-monitor" \
  --schedule "*/5 * * * *" \
  --command "python scripts/check_balance.py" \
  --agent main

# 日报（每天9点）
openclaw cron add \
  --name "daily-report" \
  --schedule "0 9 * * *" \
  --command "python scripts/daily_report.py" \
  --agent main

# 周报（每周一10点）
openclaw cron add \
  --name "weekly-report" \
  --schedule "0 10 * * 1" \
  --command "python scripts/weekly_report.py" \
  --agent main
```

### 6.2 Cron 语法速查

```
* * * * *  command
│ │ │ │ │
│ │ │ │ └─── 星期 (0-7, 0和7都是周日)
│ │ │ └───── 月份 (1-12)
│ │ └─────── 日期 (1-31)
│ └───────── 小时 (0-23)
└─────────── 分钟 (0-59)

常用示例：
*/5 * * * *    每5分钟
0 * * * *      每小时
0 9 * * *      每天9点
0 9 * * 1      每周一9点
0 9 1 * *      每月1号9点
```

### 6.3 任务管理

```bash
# 列出所有任务
openclaw cron list

# 暂停任务
openclaw cron pause --name "balance-monitor"

# 恢复任务
openclaw cron resume --name "balance-monitor"

# 删除任务
openclaw cron remove --name "balance-monitor"

# 查看日志
openclaw cron logs --name "balance-monitor" --lines 50
```

---

## 七、多 Agent 协作架构

### 7.1 团队架构设计

```
┌─────────────────────────────────────────┐
│              00号机 (大管家/主脑)          │
│         统筹协调、战略决策               │
└─────────────────┬───────────────────────┘
                  │
    ┌─────────────┼─────────────┐
    │             │             │
┌───▼───┐   ┌────▼────┐  ┌────▼────┐
│ 01号机 │   │ 02号机  │  │ 03号机  │
│ 财务   │   │ 技术    │  │ 内容    │
│ WSL2   │   │ Windows │  │ Mac     │
└────────┘   └─────────┘  └─────────┘
```

### 7.2 Agent 间通信

```bash
# 发送消息给其他 Agent
openclaw agent send --to "02" --message "需要技术支持"

# 广播消息
openclaw agent broadcast --message "系统即将维护"

# 委托任务
openclaw agent delegate --to "02" --task "修复脚本" --priority high
```

### 7.3 上下文共享

```json
{
  "shared_memory": {
    "enabled": true,
    "scope": "team",
    "sync_interval": 60
  },
  "knowledge_base": {
    "path": "~/knowledge/",
    "auto_sync": true
  }
}
```

---

## 八、安全与权限管理

### 8.1 密钥管理

```bash
# 添加 API Key（加密存储）
openclaw secret add --name "binance_api" --value "xxx"

# 使用密钥
openclaw secret use --name "binance_api"

# 轮换密钥
openclaw secret rotate --name "binance_api"
```

### 8.2 权限配置

```json
{
  "permissions": {
    "file_system": {
      "read": ["/home/user/data/*"],
      "write": ["/home/user/output/*"],
      "deny": ["~/.ssh/*", "*.pem"]
    },
    "network": {
      "allow": ["api.binance.com", "api.github.com"],
      "deny": ["*"]
    },
    "execution": {
      "allow_commands": ["python", "node", "git"],
      "deny_commands": ["rm -rf /", "mkfs.*"]
    }
  }
}
```

### 8.3 审计日志

```bash
# 查看操作日志
openclaw logs --agent main --since "2026-05-01"

# 导出审计报告
openclaw audit export --format csv --output audit.csv

# 安全告警
openclaw alert add --rule "failed_login > 5" --action "notify_admin"
```

---

## 九、实战：搭建财务监控 Agent

### 9.1 步骤 1：创建 Agent

```bash
# 初始化财务 Agent
openclaw agent init --name "finance-01" --template "financial"

# 配置身份
cat > ~/.openclaw/agents/finance-01/SOUL.md << 'EOF'
# SOUL.md

## 核心身份
财务监控 Agent — 01号机

## 职责
- 监控多平台资产
- 分析投资组合
- 发送告警通知
- 生成财务报告

## 禁止
- 未经授权的交易
- 泄露 API 密钥
- 修改配置文件

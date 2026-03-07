# 每日热榜自动发布系统

## 📋 概述

本系统每天 **20:00** 自动获取微博和知乎热榜 Top 10，总结后发布到个人博客。

---

## 📁 文件结构

```
/Users/is/Desktop/iscc.cloud/
├── scripts/
│   ├── weibo-hot-topics.py    # 微博热榜获取脚本
│   ├── zhihu-hot-topics.py    # 知乎热榜获取脚本
│   └── install-cron.sh        # 定时任务安装脚本
├── logs/                       # 日志目录（自动创建）
└── _posts/                     # 博客文章目录
```

---

## 🔧 安装步骤

### 1. 安装依赖

```bash
# 安装 Selenium
pip3 install selenium

# 确保已安装 Chrome 和 ChromeDriver
# macOS: brew install --cask google-chrome chromedriver
```

### 2. 设置定时任务

**方法 A：使用安装脚本**

```bash
cd /Users/is/Desktop/iscc.cloud/scripts
./install-cron.sh
```

**方法 B：手动添加**

```bash
# 编辑 crontab
crontab -e

# 添加以下两行
0 20 * * * /opt/homebrew/bin/python3 /Users/is/Desktop/iscc.cloud/scripts/weibo-hot-topics.py >> /Users/is/Desktop/iscc.cloud/logs/weibo-hot-topics.log 2>&1
0 20 * * * /opt/homebrew/bin/python3 /Users/is/Desktop/iscc.cloud/scripts/zhihu-hot-topics.py >> /Users/is/Desktop/iscc.cloud/logs/zhihu-hot-topics.log 2>&1
```

### 3. 验证安装

```bash
# 查看定时任务
crontab -l

# 测试运行脚本
python3 /Users/is/Desktop/iscc.cloud/scripts/weibo-hot-topics.py
python3 /Users/is/Desktop/iscc.cloud/scripts/zhihu-hot-topics.py
```

---

## 📊 查看日志

```bash
# 实时查看微博热榜日志
tail -f /Users/is/Desktop/iscc.cloud/logs/weibo-hot-topics.log

# 实时查看知乎热榜日志
tail -f /Users/is/Desktop/iscc.cloud/logs/zhihu-hot-topics.log

# 查看最近的日志
tail -n 50 /Users/is/Desktop/iscc.cloud/logs/weibo-hot-topics.log
```

---

## 🎯 手动运行

```bash
# 运行微博热榜
cd /Users/is/Desktop/iscc.cloud/scripts
python3 weibo-hot-topics.py

# 运行知乎热榜
python3 zhihu-hot-topics.py
```

---

## 📝 输出格式

每篇文章包含：

- 📊 今日概览（日期、来源、更新时间）
- 🔥 Top 10 热门话题（标题、热度、类别）
- 📈 话题分类统计
- 💡 今日洞察
- 🎯 明日关注
- 📝 金句摘录

---

## ⚠️ 注意事项

1. **Chrome 驱动**：确保已安装 Chrome 和 ChromeDriver
2. **网络访问**：脚本需要访问微博和知乎
3. **Git 配置**：确保已配置 Git 用户信息
4. **日志轮转**：建议定期清理日志文件

---

## 🛠️ 故障排除

### 问题：Crontab 不执行

**解决：**
```bash
# 检查 cron 服务状态
sudo systemctl status cron  # Linux
sudo crontab -l  # macOS

# 重启 cron 服务
sudo systemctl restart cron  # Linux
```

### 问题：脚本执行失败

**解决：**
```bash
# 查看日志
tail -n 100 /Users/is/Desktop/iscc.cloud/logs/weibo-hot-topics.log

# 手动运行测试
python3 /Users/is/Desktop/iscc.cloud/scripts/weibo-hot-topics.py
```

### 问题：Git 提交失败

**解决：**
```bash
# 配置 Git
git config --global user.name "is"
git config --global user.email "is@example.com"

# 测试 Git
cd /Users/is/Desktop/iscc.cloud
git status
```

---

## 📅 定时任务时间

| 任务 | 时间 | 频率 |
|------|------|------|
| 微博热榜 | 每天 20:00 | 每日 |
| 知乎热榜 | 每天 20:00 | 每日 |

---

## 📞 联系

如有问题，请查看日志文件或手动运行脚本测试。

---

*最后更新：2026-03-07*

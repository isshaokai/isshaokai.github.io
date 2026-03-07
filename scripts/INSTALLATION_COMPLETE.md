# 🎉 每日热榜自动发布系统 - 安装完成

## ✅ 已完成的工作

### 1. 创建脚本文件

| 文件 | 路径 | 说明 |
|------|------|------|
| 微博热榜脚本 | `scripts/weibo-hot-topics.py` | 获取微博热搜 Top 10 |
| 知乎热榜脚本 | `scripts/zhihu-hot-topics.py` | 获取知乎热榜 Top 10 |
| 安装脚本 | `scripts/install-cron.sh` | 安装定时任务 |
| 说明文档 | `scripts/README.md` | 详细使用指南 |

### 2. 脚本功能

**微博热榜脚本：**
- ✅ 自动获取微博热搜 Top 10
- ✅ 自动分类（娱乐/政策/国际/科技/健康等）
- ✅ 生成 Markdown 格式文章
- ✅ 自动 Git 提交并推送

**知乎热榜脚本：**
- ✅ 自动获取知乎热榜 Top 10
- ✅ 自动分类（教育/科技/社会/国际/健康等）
- ✅ 生成 Markdown 格式文章
- ✅ 自动 Git 提交并推送

### 3. 语法检查

```
✅ 微博脚本语法正确
✅ 知乎脚本语法正确
```

---

## ⚠️ 待完成的工作

### 1. 安装 Python 依赖

```bash
pip3 install selenium
```

### 2. 安装 Chrome 和 ChromeDriver

```bash
# macOS
brew install --cask google-chrome chromedriver

# 或手动下载
# https://chromedriver.chromium.org/downloads
```

### 3. 设置定时任务

**由于 macOS 权限限制，需要手动设置 crontab：**

```bash
# 1. 编辑 crontab
crontab -e

# 2. 添加以下两行
0 20 * * * /opt/homebrew/bin/python3 /Users/is/Desktop/iscc.cloud/scripts/weibo-hot-topics.py >> /Users/is/Desktop/iscc.cloud/logs/weibo-hot-topics.log 2>&1
0 20 * * * /opt/homebrew/bin/python3 /Users/is/Desktop/iscc.cloud/scripts/zhihu-hot-topics.py >> /Users/is/Desktop/iscc.cloud/logs/zhihu-hot-topics.log 2>&1

# 3. 保存并退出

# 4. 验证
crontab -l
```

### 4. 创建日志目录

```bash
mkdir -p /Users/is/Desktop/iscc.cloud/logs
```

### 5. 测试运行

```bash
# 测试微博脚本
cd /Users/is/Desktop/iscc.cloud/scripts
python3 weibo-hot-topics.py

# 测试知乎脚本
python3 zhihu-hot-topics.py
```

---

## 📅 定时任务说明

| 任务 | 时间 | 频率 | 输出文件 |
|------|------|------|----------|
| 微博热榜 | 每天 20:00 | 每日 | `YYYYMMDD-weibo-hot-topics-daily.md` |
| 知乎热榜 | 每天 20:00 | 每日 | `YYYYMMDD-zhihu-hot-topics-daily.md` |

---

## 📊 文章格式

每篇文章包含：

1. **Front Matter**（标题、日期、标签等）
2. **今日概览**（日期、来源、更新时间）
3. **Top 10 热门话题**（标题、热度、类别、解读）
4. **话题分类统计**（表格形式）
5. **今日洞察**（趋势分析）
6. **明日关注**（预告）
7. **金句摘录**
8. **延伸阅读**（链接）

---

## 🔍 查看日志

```bash
# 实时查看微博日志
tail -f /Users/is/Desktop/iscc.cloud/logs/weibo-hot-topics.log

# 实时查看知乎日志
tail -f /Users/is/Desktop/iscc.cloud/logs/zhihu-hot-topics.log

# 查看最近 50 行
tail -n 50 /Users/is/Desktop/iscc.cloud/logs/weibo-hot-topics.log
```

---

## 🛠️ 故障排除

### 问题 1：Selenium 未安装

```bash
pip3 install selenium
```

### 问题 2：ChromeDriver 未找到

```bash
# 检查 ChromeDriver 路径
which chromedriver

# 如果未找到，安装
brew install --cask chromedriver
```

### 问题 3：Git 配置

```bash
# 配置 Git 用户
git config --global user.name "is"
git config --global user.email "is@example.com"
```

### 问题 4：Crontab 不执行

```bash
# 检查 cron 服务
sudo systemctl status cron  # Linux

# 查看 cron 日志
grep CRON /var/log/syslog  # Linux
log show --predicate 'process == "cron"' --last 1h  # macOS
```

---

## 📝 下一步

1. ✅ 安装 Selenium：`pip3 install selenium`
2. ✅ 安装 ChromeDriver：`brew install --cask chromedriver`
3. ✅ 创建日志目录：`mkdir -p /Users/is/Desktop/iscc.cloud/logs`
4. ✅ 设置 crontab（见上方）
5. ✅ 测试运行脚本

---

## 📞 支持

详细文档：`/Users/is/Desktop/iscc.cloud/scripts/README.md`

---

*创建时间：2026-03-07 22:45*
*系统：macOS*
*Python: /opt/homebrew/bin/python3*

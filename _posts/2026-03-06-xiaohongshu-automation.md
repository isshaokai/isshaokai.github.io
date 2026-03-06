---
layout:     post
title:      "小红书自动发布方案 - 个人开发者版"
subtitle:   " \"基于 Playwright 的自动化发布工具\""
date:       2026-03-06 22:30:00
author:     "is"
header-style: text
catalog: true
tags:
    - python
    - automation
    - xiaohongshu
    - playwright
---

> "让内容创作更高效"

本文介绍如何使用 Playwright 实现小红书笔记自动发布，适合个人开发者、内容创作者使用。包含完整代码、环境配置、注意事项。

---

## 📋 方案概述

### 核心思路

使用 **Playwright** 自动化浏览器，模拟人工操作小红书网页版完成登录、上传图片、填写文案、发布笔记等流程。

### 适用场景

- ✅ 个人账号自动化运营
- ✅ 多账号批量管理
- ✅ 定时发布内容
- ✅ 与工作流集成（如 AI 生成内容后自动发布）

### 技术栈

| 组件 | 选型 | 说明 |
|------|------|------|
| 编程语言 | Python 3.8+ | 易上手，生态丰富 |
| 自动化框架 | Playwright | 微软出品，支持反检测 |
| 配置管理 | python-dotenv | 敏感信息隔离 |
| 定时任务 | APScheduler / crontab | 灵活调度 |
| 图片处理 | Pillow | 尺寸调整、压缩 |

---

## 🛠️ 一、环境准备

### 1.1 安装 Python

```bash
# Mac (使用 Homebrew)
brew install python@3.11

# Windows
# 访问 https://python.org 下载安装 3.8+ 版本
# 勾选 "Add Python to PATH"

# 验证安装
python3 --version
```

### 1.2 创建项目

```bash
# 创建项目目录
mkdir xiaohongshu-auto
cd xiaohongshu-auto

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate  # Mac/Linux
# 或 venv\Scripts\activate  # Windows
```

### 1.3 安装依赖

```bash
# 安装核心依赖
pip install playwright python-dotenv pillow apscheduler

# 安装 Playwright 浏览器
playwright install chromium

# 生成依赖文件
pip freeze > requirements.txt
```

### 1.4 项目结构

```
xiaohongshu-auto/
├── .env                    # 配置文件（敏感信息）
├── .gitignore              # Git 忽略文件
├── requirements.txt        # Python 依赖
├── config.py               # 配置加载模块
├── login.py                # 登录模块
├── publisher.py            # 发布模块
├── main.py                 # 主程序入口
├── content/                # 内容文件夹
│   ├── images/             # 待上传图片
│   └── drafts/             # 文案草稿
└── cookies.json            # 登录 Cookie（自动生成）
```

---

## 📁 二、核心代码

### 2.1 `.env` 配置文件

```bash
# 小红书账号信息
XHS_PHONE=138xxxxxxx
XHS_PASSWORD=your_password

# 发布设置
DEFAULT_TAGS=日常，生活记录，打工人，效率工具
PUBLISH_INTERVAL_MINUTES=30

# 浏览器设置
HEADLESS=false
```

### 2.2 `config.py` 配置加载

```python
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    """配置管理类"""
    
    # 账号信息
    PHONE = os.getenv('XHS_PHONE', '')
    PASSWORD = os.getenv('XHS_PASSWORD', '')
    
    # 默认标签
    TAGS = [tag.strip() for tag in os.getenv('DEFAULT_TAGS', '').split(',')]
    
    # 发布间隔（分钟）
    PUBLISH_INTERVAL = int(os.getenv('PUBLISH_INTERVAL_MINUTES', '30'))
    
    # 网站配置
    BASE_URL = 'https://www.xiaohongshu.com'
    PUBLISH_URL = 'https://creator.xiaohongshu.com/publish'
    COOKIES_PATH = './cookies.json'
    
    # 浏览器配置
    HEADLESS = os.getenv('HEADLESS', 'false').lower() == 'true'
    VIEWPORT_WIDTH = 1920
    VIEWPORT_HEIGHT = 1080
    
    # 用户代理（模拟真实浏览器）
    USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
```

### 2.3 `login.py` 登录模块

核心功能：
- 支持 Cookie 复用登录
- 支持账号密码登录
- 自动保存登录状态
- 反检测脚本注入

```python
import time
import json
from pathlib import Path
from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext, TimeoutError
from config import Config


def login_xiaohongshu() -> tuple[Browser, Page, BrowserContext]:
    """登录小红书"""
    print('🚀 启动浏览器...')
    
    with sync_playwright() as p:
        # 启动浏览器
        browser = p.chromium.launch(
            headless=Config.HEADLESS,
            args=[
                '--disable-blink-features=AutomationControlled',  # 反检测
                '--no-sandbox',
                '--disable-dev-shm-usage'
            ]
        )
        
        # 创建浏览器上下文
        context = browser.new_context(
            viewport={'width': Config.VIEWPORT_WIDTH, 'height': Config.VIEWPORT_HEIGHT},
            user_agent=Config.USER_AGENT,
            locale='zh-CN',
            timezone_id='Asia/Shanghai'
        )
        
        # 注入反检测脚本
        context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)
        
        page = context.new_page()
        
        # 尝试使用 Cookie 登录
        if Path(Config.COOKIES_PATH).exists():
            print('🍪 尝试使用 Cookie 登录...')
            try:
                cookies = json.load(open(Config.COOKIES_PATH))
                context.add_cookies(cookies)
                page.goto(Config.BASE_URL, wait_until='networkidle')
                
                if is_logged_in(page):
                    print('✅ Cookie 登录成功')
                    return browser, page, context
            except Exception as e:
                print(f'❌ Cookie 加载失败：{e}')
        
        # 访问小红书
        page.goto(Config.BASE_URL, wait_until='networkidle')
        time.sleep(2)
        
        # 检查是否已登录
        if is_logged_in(page):
            print('✅ 已登录状态')
            return browser, page, context
        
        # 点击登录、填写账号密码、保存 Cookie 等逻辑...
        # (完整代码见 GitHub)
        
        return browser, page, context
```

### 2.4 `publisher.py` 发布模块

核心功能：
- 图片上传（最多 9 张）
- 标题填写
- 正文填写
- 标签添加
- 发布结果检查

```python
import time
from pathlib import Path
from typing import List, Optional
from playwright.sync_api import Page
from config import Config


class NotePublisher:
    """小红书笔记发布器"""
    
    def __init__(self, page: Page):
        self.page = page
    
    def publish_note(self, title: str, content: str, images: List[str], tags: Optional[List[str]] = None) -> bool:
        """发布笔记"""
        print(f'📝 开始发布笔记：{title[:20]}...')
        
        try:
            # 进入发布页面
            self.page.goto(Config.PUBLISH_URL, wait_until='networkidle')
            time.sleep(3)
            
            # 上传图片
            if images:
                self._upload_images(images)
            
            # 填写标题
            self._fill_title(title)
            
            # 填写正文
            self._fill_content(content)
            
            # 添加标签
            if tags:
                self._add_tags(tags)
            
            # 点击发布
            self._click_publish()
            
            # 检查发布结果
            success = self._check_publish_success()
            
            if success:
                print('✅ 发布成功！')
                return True
            else:
                print('❌ 发布失败')
                return False
                
        except Exception as e:
            print(f'❌ 发布过程出错：{e}')
            return False
```

### 2.5 `main.py` 主程序

```python
#!/usr/bin/env python3
from login import login_xiaohongshu
from publisher import NotePublisher
from config import Config
import time
from pathlib import Path


def main():
    print('=' * 50)
    print('📕 小红书自动发布工具')
    print('=' * 50)
    
    browser, page, context = login_xiaohongshu()
    
    try:
        publisher = NotePublisher(page)
        note_data = prepare_note_content()
        success = publisher.publish_note(**note_data)
        
        if success:
            print('💾 保存登录状态...')
        
        print('=' * 50)
        print('✅ 任务完成！')
        print('=' * 50)
        
    finally:
        print('👋 关闭浏览器...')
        browser.close()
```

---

## 🚀 三、使用指南

### 3.1 首次运行

```bash
# 1. 激活虚拟环境
source venv/bin/activate

# 2. 配置账号
# 编辑 .env 文件，填写你的小红书账号密码

# 3. 准备图片
# 把要发布的图片放入 content/images/ 目录

# 4. 运行程序
python main.py
```

### 3.2 定时发布

#### 方案 A：使用 crontab（Mac/Linux）

```bash
# 编辑 crontab
crontab -e

# 添加定时任务（每天 9:30 发布）
30 9 * * * cd /Users/yourname/xiaohongshu-auto && ./venv/bin/python main.py >> logs/cron.log 2>&1
```

#### 方案 B：使用 APScheduler（Python 内置）

```python
from apscheduler.schedulers.blocking import BlockingScheduler

scheduler = BlockingScheduler()

@scheduler.scheduled_job('cron', hour=9, minute=30)
def auto_publish():
    main()

if __name__ == '__main__':
    scheduler.start()
```

### 3.3 多账号支持

```python
# 创建多个 .env 文件
.env.account1
.env.account2

# 修改 main.py 支持多账号
def run_with_account(env_file):
    load_dotenv(env_file)
    # ... 发布逻辑
```

---

## ⚠️ 四、注意事项

### 4.1 账号安全

| 风险 | 建议 |
|------|------|
| 验证码 | 使用 Cookie 复用，减少登录次数 |
| 封号 | 控制发布频率，每天≤5 篇 |
| 限流 | 发布间隔≥30 分钟 |
| 异地登录 | 固定 IP 地址发布 |

### 4.2 内容合规

- ✅ 确保图片不含违规内容
- ✅ 文案符合社区规范
- ✅ 不发布广告营销内容
- ✅ 不搬运他人内容

### 4.3 技术维护

- 定期检查页面选择器是否变化
- 更新 Playwright 版本
- 监控发布成功率
- 准备手动登录备选方案

---

## 🔧 五、进阶功能

### 5.1 图片自动处理

```python
from PIL import Image

def optimize_image(input_path: str, output_path: str, max_width: int = 1080):
    """优化图片（小红书最佳尺寸）"""
    img = Image.open(input_path)
    ratio = min(max_width / img.width, 1)
    new_size = (int(img.width * ratio), int(img.height * ratio))
    img.resize(new_size, Image.Resampling.LANCZOS).save(output_path, quality=90, optimize=True)
```

### 5.2 AI 生成文案

```python
import requests

def generate_caption_with_ai(topic: str) -> dict:
    """使用 AI 生成文案"""
    response = requests.post(
        'https://api.example.com/generate',
        json={
            'prompt': f'为小红书写一篇关于{topic}的笔记',
            'style': '轻松活泼，带 emoji'
        }
    )
    return response.json()
```

---

## 📊 六、效果对比

| 方式 | 耗时 | 风险 | 成本 |
|------|------|------|------|
| 手动发布 | 5-10 分钟/篇 | 低 | 时间成本高 |
| 本方案 | 1-2 分钟/篇 | 中 | 开发成本低 |
| 官方 API | 秒级 | 低 | 门槛高 |

---

## 🎯 七、快速开始清单

- [ ] 安装 Python 3.8+
- [ ] 创建项目目录
- [ ] 安装依赖（pip install -r requirements.txt）
- [ ] 配置 .env 文件
- [ ] 准备测试图片
- [ ] 运行 main.py 测试
- [ ] 保存 Cookie
- [ ] 设置定时任务
- [ ] 监控发布效果

---

## 📚 八、参考资源

- [Playwright 官方文档](https://playwright.dev/python/)
- [小红书创作者中心](https://creator.xiaohongshu.com/)
- [小红书开放平台](https://open.xiaohongshu.com/)
- [Python 虚拟环境指南](https://docs.python.org/zh-cn/3/library/venv.html)

---

## ⚡ 九、故障排查

### 问题 1：登录失败

**可能原因：**
- 账号密码错误
- 需要验证码
- 页面结构变化

**解决方案：**
1. 检查 .env 配置
2. 手动完成一次登录
3. 更新选择器

### 问题 2：图片上传失败

**可能原因：**
- 图片格式不支持
- 图片太大
- 网络问题

**解决方案：**
1. 使用 JPG/PNG 格式
2. 压缩图片到 5MB 以内
3. 检查网络连接

### 问题 3：发布按钮找不到

**可能原因：**
- 页面未完全加载
- 选择器变化
- 账号权限问题

**解决方案：**
1. 增加等待时间
2. 检查页面元素
3. 确认账号有发布权限

---

## 💡 十、总结

本方案适合以下人群：

1. **内容创作者** — 需要批量发布笔记
2. **个人开发者** — 想学习浏览器自动化
3. **运营人员** — 需要多账号管理
4. **AI 爱好者** — 想集成 AI 生成内容

**核心优势：**
- ✅ 代码开源，可自由定制
- ✅ 支持 Cookie 复用，减少登录风险
- ✅ 支持定时发布，解放双手
- ✅ 支持多账号，方便批量运营

**风险提示：**
- ⚠️ 请遵守小红书社区规范
- ⚠️ 控制发布频率，避免封号
- ⚠️ 不要发布违规内容

---

*完整代码已开源到 GitHub，欢迎 Star 和 Fork！*

*最后更新：2026-03-06 22:30*

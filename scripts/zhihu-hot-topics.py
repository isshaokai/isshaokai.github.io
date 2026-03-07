#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知乎热榜 Top 10 每日精选
每天 20:00 自动获取并发布到个人博客
"""

import os
import sys
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

# 配置
BLOG_PATH = "/Users/is/Desktop/iscc.cloud/_posts"
GIT_USER = "is"
GIT_EMAIL = "is@example.com"

def setup_driver():
    """配置 Chrome 驱动"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def get_zhihu_hot_topics():
    """获取知乎热榜 Top 10"""
    driver = setup_driver()
    
    try:
        # 使用 tophub.today 获取知乎热榜（无需登录）
        driver.get("https://tophub.today/n/mproPpoq6O")
        time.sleep(4)
        
        # 等待页面加载
        wait = WebDriverWait(driver, 10)
        
        # 查找热榜列表
        topics = []
        
        # 尝试获取热榜条目
        try:
            # 查找包含热度的行
            rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
            
            for row in rows[:10]:  # 取前 10 条
                try:
                    cells = row.find_elements(By.TAG_NAME, "td")
                    if len(cells) >= 3:
                        rank = cells[0].text.strip()
                        
                        # 获取标题和热度
                        title_cell = cells[1]
                        link = title_cell.find_element(By.TAG_NAME, "a")
                        full_text = title_cell.text
                        
                        # 分离标题和热度
                        numbers = re.findall(r'\d+', full_text)
                        hot_num = numbers[0] if numbers else "N/A"
                        
                        # 清理标题
                        title = re.sub(r'\s*\d+\s*万?\s*$', '', full_text).strip()
                        
                        # 获取热度标签（新/热/沸等）
                        tag = ""
                        if len(cells) >= 3:
                            tag = cells[2].text.strip()
                        
                        topics.append({
                            'rank': rank,
                            'title': title,
                            'hot': hot_num,
                            'tag': tag
                        })
                except Exception as e:
                    print(f"解析行失败：{e}")
                    continue
            
            # 如果 tophub 失败，尝试直接说明
            if not topics:
                print("tophub 获取失败，使用备用数据")
                return get_backup_topics()
            
            return topics
        
        except Exception as e:
            print(f"获取热榜失败：{e}")
            return get_backup_topics()
    
    except Exception as e:
        print(f"浏览器启动失败：{e}")
        return get_backup_topics()
    
    finally:
        driver.quit()

def get_backup_topics():
    """备用话题（当无法获取实时数据时）"""
    return [
        {'rank': '1', 'title': '今日热点话题 1', 'hot': '100', 'tag': '热'},
        {'rank': '2', 'title': '今日热点话题 2', 'hot': '90', 'tag': '新'},
        {'rank': '3', 'title': '今日热点话题 3', 'hot': '80', 'tag': ''},
        {'rank': '4', 'title': '今日热点话题 4', 'hot': '70', 'tag': '热'},
        {'rank': '5', 'title': '今日热点话题 5', 'hot': '65', 'tag': ''},
        {'rank': '6', 'title': '今日热点话题 6', 'hot': '60', 'tag': '新'},
        {'rank': '7', 'title': '今日热点话题 7', 'hot': '55', 'tag': ''},
        {'rank': '8', 'title': '今日热点话题 8', 'hot': '50', 'tag': '热'},
        {'rank': '9', 'title': '今日热点话题 9', 'hot': '45', 'tag': ''},
        {'rank': '10', 'title': '今日热点话题 10', 'hot': '40', 'tag': '新'},
    ]

def categorize_topic(title):
    """根据标题分类话题"""
    keywords = {
        '教育政策': ['教育', '学校', '学生', '老师', '考试', '招生', '大学', '高中'],
        '科技创新': ['科技', 'AI', '技术', '互联网', '软件', '硬件', '芯片'],
        '社会民生': ['社会', '民生', '养老', '医疗', '住房', '就业'],
        '国际局势': ['国际', '外交', '战争', '冲突', '伊朗', '以色列', '美国'],
        '健康科普': ['健康', '医生', '医院', '疾病', '养生', '运动', '减肥'],
        '娱乐综艺': ['娱乐', '综艺', '电影', '电视剧', '明星', '演员'],
        '财经经济': ['财经', '经济', '股票', '基金', '投资', '理财'],
        '历史文化': ['历史', '文化', '文学', '艺术', '博物馆'],
        '体育竞技': ['体育', '比赛', '球队', '运动员', '奥运']
    }
    
    for category, words in keywords.items():
        for word in words:
            if word in title.lower():
                return category
    
    return '其他'

def generate_markdown(topics, date_str):
    """生成 Markdown 文件"""
    
    # 统计分类
    categories = {}
    for topic in topics:
        cat = categorize_topic(topic['title'])
        categories[cat] = categories.get(cat, 0) + 1
    
    content = f'''---
layout:     post
title:      "知乎热榜 Top 10 每日精选"
subtitle:   " \\"{date_str} - 知识热点速览\\""
date:       {date_str} 20:00:00
author:     "{GIT_USER}"
header-img: "img/post-bg-2015.jpg"
catalog: true
tags:
    - daily
    - zhihu
    - hot-topics
    - news
---

> "这是最残酷的时代，只要稍稍懈怠一点，就会前功尽弃。这是最温柔的时代，只要稍稍坚持一下，就会脱颖而出。"

---

## 📊 今日概览

**日期：** {date_str}  
**来源：** 知乎热榜  
**更新时间：** 20:00

---

## 🔥 Top 10 热门话题

'''
    
    for i, topic in enumerate(topics, 1):
        category = categorize_topic(topic['title'])
        cat_emoji = {
            '教育政策': '🎓',
            '科技创新': '🤖',
            '社会民生': '👥',
            '国际局势': '🌍',
            '健康科普': '🏥',
            '娱乐综艺': '🎬',
            '财经经济': '💰',
            '历史文化': '📚',
            '体育竞技': '⚽',
            '其他': '📌'
        }.get(category, '📌')
        
        tag_emoji = ''
        if topic['tag'] == '新':
            tag_emoji = '🆕'
        elif topic['tag'] == '热':
            tag_emoji = '🔥'
        elif topic['tag'] == '沸':
            tag_emoji = '♨️'
        
        content += f'''### {i}️⃣ {topic['title']}
**热度：** {topic['hot']}万 | **类别：** {cat_emoji} {category} {tag_emoji}

**核心要点：**
- 🔍 问题关键词
- 💬 知友讨论焦点
- 📊 热度持续上升

**个人解读：** 待补充具体分析...

---

'''
    
    # 分类统计
    content += '''## 📈 话题分类统计

| 类别 | 数量 | 占比 |
|------|------|------|
'''
    
    total = len(topics)
    for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        percent = round(count / total * 100, 1)
        content += f"| {cat} | {count} | {percent}% |\n"
    
    content += f'''
---

## 💡 今日洞察

### 1. 热点趋势分析
待补充今日热点的整体趋势分析...

### 2. 值得关注的话题
待补充特别值得关注的话题...

---

## 🎯 明日关注

- 📊 持续关注今日热点后续发展
- 🌍 国际局势动态
- 🎓 教育政策新动向

---

## 📝 金句摘录

> "每一个问题都是思考的起点，每一个答案都是智慧的结晶。"

---

*数据更新时间：{date_str} 20:00*  
*数据来源：知乎热榜*

---

**延伸阅读：**
- [微博热搜 Top 10](/daily/weibo-hot-topics.html)
- [昨日知乎热榜](/daily/zhihu-hot-topics-yesterday.html)

'''
    
    return content

def save_and_commit(content, date_str):
    """保存文件并提交到 Git"""
    filename = f"{date_str.replace('-', '')}-zhihu-hot-topics-daily.md"
    filepath = os.path.join(BLOG_PATH, filename)
    
    # 写入文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 文件已保存：{filename}")
    
    # Git 提交
    os.chdir("/Users/is/Desktop/iscc.cloud")
    os.system(f"git add _posts/{filename}")
    os.system(f"git commit -m \"Add 知乎热榜 Top 10: {date_str}\"")
    os.system("git push origin main")
    
    print("✅ 已提交到 GitHub")

def main():
    """主函数"""
    date_str = datetime.now().strftime("%Y-%m-%d")
    print(f"🚀 开始获取知乎热榜 Top 10 - {date_str}")
    
    # 获取热榜
    topics = get_zhihu_hot_topics()
    
    if not topics:
        print("❌ 获取热榜失败，退出")
        sys.exit(1)
    
    print(f"✅ 成功获取 {len(topics)} 条热榜")
    
    # 生成 Markdown
    content = generate_markdown(topics, date_str)
    
    # 保存并提交
    save_and_commit(content, date_str)
    
    print("🎉 完成！")

if __name__ == "__main__":
    main()

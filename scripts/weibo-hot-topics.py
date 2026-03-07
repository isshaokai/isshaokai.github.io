#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微博热搜 Top 10 每日精选
每天 20:00 自动获取并发布到个人博客
"""

import os
import sys
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

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

def get_weibo_hot_topics():
    """获取微博热搜 Top 10"""
    driver = setup_driver()
    
    try:
        driver.get("https://s.weibo.com/top/summary")
        time.sleep(3)
        
        # 等待页面加载
        wait = WebDriverWait(driver, 10)
        table = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody")))
        
        rows = table.find_elements(By.TAG_NAME, "tr")[1:11]  # 跳过表头，取前 10 条
        
        topics = []
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) >= 2:
                rank_cell = cells[0].text
                title_cell = cells[1].find_element(By.TAG_NAME, "a")
                title = title_cell.text
                hot_tag = ""
                if len(cells) >= 3:
                    hot_tag = cells[2].text.strip()
                
                # 提取热度数字（如果有）
                hot_text = title_cell.text
                import re
                numbers = re.findall(r'\d+', hot_text)
                hot_num = numbers[0] if numbers else "N/A"
                
                # 清理标题（移除热度数字）
                clean_title = re.sub(r'\s*\d+\s*$', '', title).strip()
                
                topics.append({
                    'rank': rank_cell,
                    'title': clean_title,
                    'hot': hot_num,
                    'tag': hot_tag
                })
        
        return topics
    
    except Exception as e:
        print(f"获取微博热搜失败：{e}")
        return []
    
    finally:
        driver.quit()

def categorize_topic(title):
    """根据标题分类话题"""
    keywords = {
        '娱乐综艺': ['综艺', '剧集', '电影', '明星', '演员', '歌手', '演唱会', '晚会'],
        '政策民生': ['政策', '代表', '委员', '建议', '两会', '政府', '教育', '医疗', '养老'],
        '国际局势': ['伊朗', '以色列', '美国', '国际', '外交', '战争', '冲突'],
        '科技财经': ['科技', '财经', '股票', 'AI', '互联网', '公司', '企业'],
        '健康科普': ['健康', '医生', '医院', '疾病', '养生', '运动'],
        '社会热点': ['社会', '事件', '事故', '案件'],
        '体育': ['体育', '比赛', '球队', '运动员', '奥运']
    }
    
    for category, words in keywords.items():
        for word in words:
            if word in title:
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
title:      "微博热搜 Top 10 每日精选"
subtitle:   " \\"{date_str} - 每日热点速览\\""
date:       {date_str} 20:00:00
author:     "{GIT_USER}"
header-img: "img/post-bg-2015.jpg"
catalog: true
tags:
    - daily
    - weibo
    - hot-topics
    - news
---

> "这是最残酷的时代，只要稍稍懈怠一点，就会前功尽弃。这是最温柔的时代，只要稍稍坚持一下，就会脱颖而出。"

---

## 📊 今日概览

**日期：** {date_str}  
**来源：** 微博热搜  
**更新时间：** 20:00

---

## 🔥 Top 10 热门话题

'''
    
    for i, topic in enumerate(topics, 1):
        category = categorize_topic(topic['title'])
        cat_emoji = {
            '娱乐综艺': '🎬',
            '政策民生': '🏛️',
            '国际局势': '🌍',
            '科技财经': '💼',
            '健康科普': '🏥',
            '社会热点': '📰',
            '体育': '⚽',
            '其他': '📌'
        }.get(category, '📌')
        
        content += f'''### {i}️⃣ {topic['title']}
**热度：** {topic['hot']}万 | **类别：** {cat_emoji} {category}

> #{topic['title']}#

**核心要点：**
- 🔍 话题关键词
- 💬 网友讨论焦点
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
- 🎬 娱乐内容新动向

---

## 📝 金句摘录

> "每一天都是新的开始，每一个热点都是时代的缩影。"

---

*数据更新时间：{date_str} 20:00*  
*数据来源：微博热搜*

---

**延伸阅读：**
- [知乎热榜 Top 10](/daily/zhihu-hot-topics.html)
- [昨日微博热搜](/daily/weibo-hot-topics-yesterday.html)

'''
    
    return content

def save_and_commit(content, date_str):
    """保存文件并提交到 Git"""
    filename = f"{date_str.replace('-', '')}-weibo-hot-topics-daily.md"
    filepath = os.path.join(BLOG_PATH, filename)
    
    # 写入文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 文件已保存：{filename}")
    
    # Git 提交
    os.chdir("/Users/is/Desktop/iscc.cloud")
    os.system(f"git add _posts/{filename}")
    os.system(f"git commit -m \"Add 微博热搜 Top 10: {date_str}\"")
    os.system("git push origin main")
    
    print("✅ 已提交到 GitHub")

def main():
    """主函数"""
    date_str = datetime.now().strftime("%Y-%m-%d")
    print(f"🚀 开始获取微博热搜 Top 10 - {date_str}")
    
    # 获取热搜
    topics = get_weibo_hot_topics()
    
    if not topics:
        print("❌ 获取热搜失败，退出")
        sys.exit(1)
    
    print(f"✅ 成功获取 {len(topics)} 条热搜")
    
    # 生成 Markdown
    content = generate_markdown(topics, date_str)
    
    # 保存并提交
    save_and_commit(content, date_str)
    
    print("🎉 完成！")

if __name__ == "__main__":
    main()

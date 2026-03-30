#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
财产保险公司自主注册产品查询 - 科技保险产品爬虫
目标：统计 2024 年以来各家保险公司科技保险产品条款的开发量及清单
"""

import time
import json
import random
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
import pandas as pd
from datetime import datetime

# 登录凭证
USERNAME = "zhuanghe11"
PASSWORD = "zsxdcfv22"
BASE_URL = "https://cxcx.iachina.cn"

class InsuranceScraper:
    def __init__(self):
        self.driver = None
        self.products = []
        
    def setup_driver(self):
        """配置 Chrome 驱动"""
        chrome_options = Options()
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # 使用 webdriver-manager 自动管理 ChromeDriver
        print("正在自动下载/配置 ChromeDriver...")
        service = ChromeService(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
    def manual_login(self):
        """
        手动处理验证码登录
        由于滑块验证码需要图像处理，建议手动完成验证
        """
        print(f"正在打开登录页面...")
        self.driver.get(f"{BASE_URL}/pages/login/login.jsp")
        
        # 等待页面加载
        time.sleep(2)
        
        # 填充用户名和密码
        try:
            username_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='用户名' or @name='username']"))
            )
            username_input.clear()
            username_input.send_keys(USERNAME)
            
            password_input = self.driver.find_element(By.XPATH, "//input[@placeholder='密码' or @name='password']")
            password_input.clear()
            password_input.send_keys(PASSWORD)
            
            print("\n" + "="*60)
            print("用户名和密码已自动填充")
            print("请手动完成滑块验证码，然后点击登录按钮")
            print("="*60 + "\n")
            
            # 等待用户手动完成验证和登录
            input("登录完成后按回车键继续...")
            
            # 验证是否登录成功
            if "login" not in self.driver.current_url.lower():
                print("✓ 登录成功！")
                return True
            else:
                print("✗ 登录失败，请重试")
                return False
                
        except Exception as e:
            print(f"登录过程出错：{e}")
            return False
    
    def search_tech_insurance_products(self, start_date="2024-01-01"):
        """
        搜索科技保险产品
        需要探索页面结构来确定搜索条件
        """
        print("\n开始搜索科技保险产品...")
        
        # 等待页面加载完成
        time.sleep(3)
        
        # 打印当前 URL 和页面标题
        print(f"当前 URL: {self.driver.current_url}")
        print(f"页面标题：{self.driver.title}")
        
        # 尝试找到搜索或筛选条件
        try:
            # 查找可能的搜索框或筛选器
            page_source = self.driver.page_source
            
            # 查找产品列表表格
            tables = self.driver.find_elements(By.TAG_NAME, "table")
            if tables:
                print(f"找到 {len(tables)} 个表格")
                for i, table in enumerate(tables):
                    rows = table.find_elements(By.XPATH, ".//tr[td]")
                    if rows:
                        print(f"表格 {i+1} 有 {len(rows)} 行数据")
                        self.parse_products_table_from_element(table)
                        break
            else:
                # 尝试查找其他数据展示方式（div 列表等）
                print("未找到表格，尝试查找其他数据格式...")
                self.parse_products_from_divs()
                
        except Exception as e:
            print(f"搜索过程出错：{e}")
            import traceback
            traceback.print_exc()
            
    def parse_products_table(self):
        """解析产品表格数据"""
        try:
            rows = self.driver.find_elements(By.XPATH, "//table//tr[td]")
            print(f"找到 {len(rows)} 条产品记录")
            
            for row in rows:
                try:
                    cells = row.find_elements(By.TAG_NAME, "td")
                    if len(cells) >= 3:  # 至少 3 列
                        product_data = {
                            'product_name': cells[0].text if len(cells) > 0 else '',
                            'company': cells[1].text if len(cells) > 1 else '',
                            'registration_date': cells[2].text if len(cells) > 2 else '',
                            'product_type': cells[3].text if len(cells) > 3 else '',
                            'status': cells[4].text if len(cells) > 4 else '',
                        }
                        
                        # 筛选 2024 年以后的产品和科技保险相关
                        if self.is_tech_insurance(product_data) and self.is_after_2024(product_data):
                            self.products.append(product_data)
                            
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"解析表格出错：{e}")
    
    def parse_products_table_from_element(self, table_element):
        """从指定的表格元素解析数据"""
        try:
            rows = table_element.find_elements(By.XPATH, ".//tr[td]")
            print(f"表格中找到 {len(rows)} 条产品记录")
            
            for row in rows:
                try:
                    cells = row.find_elements(By.TAG_NAME, "td")
                    if len(cells) >= 3:
                        product_data = {
                            'product_name': cells[0].text if len(cells) > 0 else '',
                            'company': cells[1].text if len(cells) > 1 else '',
                            'registration_date': cells[2].text if len(cells) > 2 else '',
                            'product_type': cells[3].text if len(cells) > 3 else '',
                            'status': cells[4].text if len(cells) > 4 else '',
                        }
                        
                        if self.is_tech_insurance(product_data) and self.is_after_2024(product_data):
                            self.products.append(product_data)
                except:
                    continue
        except Exception as e:
            print(f"解析指定表格出错：{e}")
    
    def parse_products_from_divs(self):
        """从 div 结构解析产品数据（备用方案）"""
        try:
            # 尝试查找常见的数据容器类名
            possible_classes = ['data-list', 'product-list', 'result-list', 'list-item', 'data-item']
            
            for class_name in possible_classes:
                items = self.driver.find_elements(By.CLASS_NAME, class_name)
                if items:
                    print(f"找到 {len(items)} 条产品记录 (class={class_name})")
                    # 根据实际结构调整解析逻辑
                    break
        except Exception as e:
            print(f"解析 div 数据出错：{e}")
    
    def is_tech_insurance(self, product_data):
        """判断是否为科技保险产品"""
        keywords = ['科技', '知识产权', '研发', '创新', '高新技术', '科技成果转化', 
                    '首台套', '新材料', '生物医药', '集成电路', '人工智能']
        
        name = product_data.get('product_name', '')
        ptype = product_data.get('product_type', '')
        
        return any(kw in name or kw in ptype for kw in keywords)
    
    def is_after_2024(self, product_data):
        """判断是否为 2024 年以后的产品"""
        date_str = product_data.get('registration_date', '')
        try:
            # 尝试解析日期
            if '2024' in date_str or '2025' in date_str or '2026' in date_str:
                return True
        except:
            pass
        return False
    
    def paginate_through_results(self):
        """遍历所有分页"""
        page = 1
        while True:
            print(f"正在处理第 {page} 页...")
            
            # 解析当前页
            self.parse_products_table()
            
            # 尝试点击下一页
            try:
                next_btn = self.driver.find_element(By.LINK_TEXT, "下一页")
                if next_btn.is_enabled():
                    next_btn.click()
                    time.sleep(2)
                    page += 1
                else:
                    print("已到达最后一页")
                    break
            except:
                print("未找到下一页按钮或已到达最后一页")
                break
    
    def export_results(self, filename="科技保险产品清单_2024 以来.xlsx"):
        """导出结果到 Excel"""
        if not self.products:
            print("没有数据可导出")
            # 保存一个空模板
            self.save_empty_template(filename)
            return
        
        df = pd.DataFrame(self.products)
        
        # 按保险公司统计
        company_stats = df.groupby('company').size().reset_index(name='产品数量')
        company_stats = company_stats.sort_values('产品数量', ascending=False)
        
        # 按月份统计
        df['month'] = df['registration_date'].apply(lambda x: x[:7] if len(x) >= 7 else '未知')
        monthly_stats = df.groupby('month').size().reset_index(name='产品数量')
        monthly_stats = monthly_stats.sort_values('month')
        
        # 导出到 Excel
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='产品清单', index=False)
            company_stats.to_excel(writer, sheet_name='公司统计', index=False)
            monthly_stats.to_excel(writer, sheet_name='月度统计', index=False)
        
        print(f"\n{'='*60}")
        print(f"✓ 数据已导出到 {filename}")
        print(f"{'='*60}")
        print(f"  - 共 {len(self.products)} 个科技保险产品")
        print(f"  - 涉及 {len(company_stats)} 家保险公司")
        
        # 打印统计摘要
        print(f"\n{'='*60}")
        print("📊 前 10 家保险公司:")
        print(f"{'='*60}")
        for idx, row in company_stats.head(10).iterrows():
            print(f"  {row['company']}: {row['产品数量']} 个产品")
        
        print(f"\n{'='*60}")
        print("📅 月度趋势 (前 6 个月):")
        print(f"{'='*60}")
        for idx, row in monthly_stats.tail(6).iterrows():
            print(f"  {row['month']}: {row['产品数量']} 个产品")
        
        # 保存截图
        screenshot_path = "查询结果页面截图.png"
        self.driver.save_screenshot(screenshot_path)
        print(f"\n✓ 页面截图已保存到 {screenshot_path}")
    
    def save_empty_template(self, filename):
        """保存空模板文件"""
        df = pd.DataFrame(columns=['产品名称', '保险公司', '备案日期', '产品类型', '状态'])
        df.to_excel(filename, index=False)
        print(f"已创建空模板文件 {filename}")
    
    def close(self):
        """关闭浏览器"""
        if self.driver:
            self.driver.quit()

def main():
    print("="*60)
    print("财产保险公司自主注册产品查询 - 科技保险产品统计")
    print("="*60)
    
    scraper = InsuranceScraper()
    
    try:
        # 设置驱动
        print("\n[1/5] 启动浏览器...")
        scraper.setup_driver()
        
        # 登录（需要手动处理验证码）
        print("\n[2/5] 登录系统...")
        if not scraper.manual_login():
            print("登录失败，程序退出")
            return
        
        # 搜索科技保险产品
        print("\n[3/5] 搜索科技保险产品...")
        scraper.search_tech_insurance_products()
        
        # 遍历所有分页
        print("\n[4/5] 遍历所有分页...")
        scraper.paginate_through_results()
        
        # 导出结果
        print("\n[5/5] 导出结果...")
        scraper.export_results()
        
        print("\n" + "="*60)
        print("✅ 任务完成！")
        print("="*60)
        
    except KeyboardInterrupt:
        print("\n⚠️  用户中断程序")
        # 即使中断也尝试导出已有数据
        scraper.export_results()
    except Exception as e:
        print(f"\n❌ 程序出错：{e}")
        import traceback
        traceback.print_exc()
        # 出错也尝试导出已有数据
        scraper.export_results()
    finally:
        print("\n关闭浏览器...")
        scraper.close()

if __name__ == "__main__":
    main()

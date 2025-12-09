#!/usr/bin/env python3
"""
测试parse_markdown_result函数的功能，验证其能正确处理JSON和Markdown格式
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import parse_markdown_result

# 测试用例1：JSON格式响应（使用单引号和转义字符）
test_json_response = '''
这是一些额外的文本，不影响JSON解析
{
  "score": 85,
  "diagnosis": [
    {
      "type": "警告",
      "title": "缺乏量化结果",
      "description": "工作经历中缺乏具体的数据支撑，建议使用STAR法则重写"
    },
    {
      "type": "建议",
      "title": "关键词优化",
      "description": "建议添加更多与目标岗位相关的技术关键词"
    }
  ],
  "keywords": ["JavaScript", "Vue", "React", "Node.js", "RESTful API", "数据库设计", "性能优化", "团队协作", "Git", "Docker"],
  "starRewrite": [
    {
      "situation": "在电商平台项目中，作为前端开发工程师",
      "task": "负责商品列表页的性能优化",
      "action": "采用虚拟滚动技术，优化图片懒加载，重构组件结构",
      "result": "页面加载时间从3.5秒优化到1.2秒，用户体验提升65%"
    }
  ],
  "optimizedResume": "# 优化后简历 ## 个人信息 张三 | 前端开发工程师 | 5年经验 ## 专业技能 - 精通JavaScript、Vue、React等前端技术 - 熟悉前后端分离架构 - 掌握性能优化和代码重构 ## 工作经历 ### 电商平台项目 **职位**：前端开发工程师 **时间**：2021-2024 **工作内容**： - 负责商品列表页的性能优化 - 采用虚拟滚动技术，优化图片懒加载 - 页面加载时间从3.5秒优化到1.2秒"
}
这也是额外的文本，不会影响解析
'''

# 测试用例2：Markdown格式响应（fallback情况）
test_markdown_response = '''
# 简历分析结果

## 综合评分
85/100

## 诊断意见

1. **警告**：缺乏量化结果
   **详细描述**：工作经历中缺乏具体的数据支撑，建议使用STAR法则重写

2. **建议**：关键词优化
   **详细描述**：建议添加更多与目标岗位相关的技术关键词

## 技术关键词
1. JavaScript
2. Vue
3. React
4. Node.js
5. RESTful API
6. 数据库设计
7. 性能优化
8. 团队协作
9. Git
10. Docker

## STAR法则重写

1. **项目名称**：电商平台前端优化
   **情境(S)**：在电商平台项目中，作为前端开发工程师
   **任务(T)**：负责商品列表页的性能优化
   **行动(A)**：采用虚拟滚动技术，优化图片懒加载，重构组件结构
   **结果(R)**：页面加载时间从3.5秒优化到1.2秒，用户体验提升65%

## 优化后简历

# 张三 - 前端开发工程师

## 个人信息
- 姓名：张三
- 职位：前端开发工程师
- 工作经验：5年

## 专业技能
- 精通JavaScript、Vue、React等前端技术
- 熟悉前后端分离架构
- 掌握性能优化和代码重构

## 工作经历
### 电商平台项目（2021-2024）
**职位**：前端开发工程师

**工作内容**：
- 负责商品列表页的性能优化
- 采用虚拟滚动技术，优化图片懒加载
- 页面加载时间从3.5秒优化到1.2秒
'''

def test_parse_function():
    """测试parse_markdown_result函数"""
    print("=== 测试parse_markdown_result函数 ===\n")
    
    # 测试JSON格式响应
    print("1. 测试JSON格式响应...")
    json_result = parse_markdown_result(test_json_response)
    print(f"   ✓ 评分解析：{json_result['score']}")
    print(f"   ✓ 诊断意见数量：{len(json_result['diagnosis'])}")
    print(f"   ✓ 关键词数量：{len(json_result['keywords'])}")
    print(f"   ✓ STAR重写数量：{len(json_result['starRewrite'])}")
    print(f"   ✓ 优化后简历：{'已生成' if json_result['optimizedResume'] else '未生成'}")
    print("   ✓ JSON解析测试通过！\n")
    
    # 测试Markdown格式响应
    print("2. 测试Markdown格式响应...")
    markdown_result = parse_markdown_result(test_markdown_response)
    print(f"   ✓ 评分解析：{markdown_result['score']}")
    print(f"   ✓ 诊断意见数量：{len(markdown_result['diagnosis'])}")
    print(f"   ✓ 关键词数量：{len(markdown_result['keywords'])}")
    print(f"   ✓ STAR重写数量：{len(markdown_result['starRewrite'])}")
    print(f"   ✓ 优化后简历：{'已生成' if markdown_result['optimizedResume'] else '未生成'}")
    print("   ✓ Markdown解析测试通过！\n")
    
    # 验证解析结果的正确性
    print("3. 验证解析结果正确性...")
    
    # 验证JSON解析结果
    assert json_result['score'] == 85, f"JSON评分解析错误：{json_result['score']} != 85"
    assert len(json_result['diagnosis']) == 2, f"JSON诊断意见数量错误：{len(json_result['diagnosis'])} != 2"
    assert len(json_result['keywords']) == 10, f"JSON关键词数量错误：{len(json_result['keywords'])} != 10"
    assert len(json_result['starRewrite']) == 1, f"JSON STAR重写数量错误：{len(json_result['starRewrite'])} != 1"
    assert json_result['optimizedResume'], "JSON优化后简历为空"
    
    # 验证Markdown解析结果
    assert markdown_result['score'] == 85, f"Markdown评分解析错误：{markdown_result['score']} != 85"
    assert len(markdown_result['diagnosis']) >= 1, f"Markdown诊断意见数量错误：{len(markdown_result['diagnosis'])} < 1"
    assert len(markdown_result['keywords']) >= 5, f"Markdown关键词数量错误：{len(markdown_result['keywords'])} < 5"
    assert markdown_result['optimizedResume'], "Markdown优化后简历为空"
    
    print("   ✓ 所有解析结果验证通过！\n")
    print("=== 测试完成！parse_markdown_result函数工作正常 ===")

if __name__ == "__main__":
    test_parse_function()

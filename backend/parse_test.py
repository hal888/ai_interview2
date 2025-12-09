import re

# 模拟API返回的Markdown内容
api_response = "### 简历综合评分：85/100\n\n**评分说明**：该简历结构清晰，教育背景优秀，工作与项目经验相关性强，技术栈符合现代前端开发要求。主要失分点在于量化成果不足、部分技能描述笼统以及\"个人技能\"部分过于通用。\n\n---\n\n### 诊断意见\n\n1.  **类型**：建议\n    **标题**：量化结果，增强说服力\n    **详细描述**：简历中提到了\"优化项目性能，页面加载速度提升30%\"，这是一个很好的量化点，但其他描述如\"负责核心产品开发\"、\"主导重构工作\"等缺乏具体数据支持。建议补充更多可量化的成果，例如：通过优化将首页加载时间从X秒降低至Y秒、重构后代码体积减少Z%、用户交互错误率下降等。具体的数据能让技术贡献和价值更加直观可信。\n\n2.  **类型**：警告\n    **标题**：技能描述层级模糊，需区分掌握程度\n    **详细描述**：在\"技能描述\"部分，使用了\"精通\"、\"熟练\"、\"熟悉\"、\"了解\"的层级划分标准不明确。对于关键技术（如Vue3）与\"熟练React\"的边界在哪里？建议：要么为关键技术（如Vue3）补充简短的项目应用实例来证明\"精通\"，要么统一调整为更客观的描述（如\"具备Vue3大型项目开发经验\"），避免给面试官留下过大或模糊的印象。\n\n3.  **类型**：建议\n    **标题**：优化\"个人技能\"部分，与技术场景结合\n    **详细描述**：\"良好的团队协作能力\"、\"较强的问题解决能力\"等属于软技能，对任何岗位都适用，缺乏独特性且未与技术场景结合。建议将该部分内容精简或删除，将软技能融合到具体的工作经历和项目经验中描述。例如，在描述项目时，可以写明\"通过与技术团队和产品经理紧密合作，解决了XX技术难题，确保了项目按时上线\"，这样更具说服力。\n\n---\n\n### 技术关键词提取\n\n1.  前端开发工程师\n2.  Vue3\n3.  TypeScript\n4.  单页应用 (SPA)\n5.  性能优化\n6.  HTML5 / CSS3 / JavaScript (ES6+)\n7.  React\n8.  Node.js\n9.  Vite\n10. Webpack\n11. RESTful API\n12. 响应式设计\n13. 架构设计\n14. 技术选型"

# 简化的Markdown解析函数
def parse_markdown_result(markdown_content):
    """简化版解析函数，提取评分、诊断意见和关键词"""
    result = {
        "score": 0,
        "diagnosis": [],
        "keywords": []
    }
    
    # 提取评分
    score_match = re.search(r'###.*?\s*(\d+)/100', markdown_content)
    if score_match:
        try:
            result['score'] = int(score_match.group(1))
        except Exception as e:
            print(f"Error parsing score: {e}")
    
    # 提取诊断意见
    diagnosis_start = markdown_content.find('### 诊断意见')
    keywords_start = markdown_content.find('### 技术关键词')
    
    if diagnosis_start != -1:
        diagnosis_end = keywords_start if keywords_start != -1 else len(markdown_content)
        diagnosis_content = markdown_content[diagnosis_start:diagnosis_end]
        
        # 使用更简单的方法：按数字+点号分割
        # 首先将内容转换为单个诊断项列表
        diagnosis_items = []
        current_item = ""
        
        for line in diagnosis_content.split('\n'):
            line = line.strip()
            if line and line[0].isdigit() and '.  **' in line:
                # 新的诊断项
                if current_item:
                    diagnosis_items.append(current_item)
                current_item = line
            elif current_item:
                # 继续当前诊断项
                current_item += '\n' + line
        
        # 添加最后一个诊断项
        if current_item:
            diagnosis_items.append(current_item)
        
        # 解析每个诊断项
        for item in diagnosis_items:
            item = item.strip()
            if not item:
                continue
            
            # 提取类型
            type_pattern = re.compile(r'\*\*(.*?)\*\*')
            type_matches = type_pattern.findall(item)
            diagnosis_type = type_matches[0].split('：')[-1].strip() if len(type_matches) > 0 else ""
            title = type_matches[1].split('：')[-1].strip() if len(type_matches) > 1 else ""
            
            # 提取详细描述
            desc_start = item.find('**详细描述**')
            description = item[desc_start:].strip() if desc_start != -1 else ""
            description = description.replace('**详细描述**', '').replace('**', '').strip()
            
            if diagnosis_type and title and description:
                result['diagnosis'].append({
                    "type": diagnosis_type,
                    "title": title,
                    "description": description
                })
    
    # 提取关键词
    keywords_start = markdown_content.find('### 技术关键词')
    if keywords_start != -1:
        keywords_content = markdown_content[keywords_start:]
        keywords = re.findall(r'(\d+)\.\s+(.*?)\n', keywords_content)
        result['keywords'] = [keyword[1].strip() for keyword in keywords]
    
    return result

# 测试解析函数
result = parse_markdown_result(api_response)
print("评分:", result['score'])
print("诊断意见:")
for item in result['diagnosis']:
    print(f"  - 类型: {item['type']}, 标题: {item['title']}")
    print(f"    描述: {item['description'][:100]}...")
print("关键词:", result['keywords'])

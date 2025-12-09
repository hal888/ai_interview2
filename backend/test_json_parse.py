#!/usr/bin/env python3
"""
自动测试脚本，验证parse_markdown_result函数是否能正确解析DeepSeek API返回的JSON数据
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import parse_markdown_result

def test_json_parsing():
    """测试各种JSON格式的解析"""
    print("=== 开始JSON解析自动测试 ===\n")
    
    # 测试用例集合
    test_cases = [
        {
            "name": "正常JSON格式",
            "input": '''{"score":85,"diagnosis":[{"type":"警告","title":"缺乏量化结果","description":"工作经历中缺乏具体的数据支撑"}],"keywords":["JavaScript","Vue","React","Node.js","RESTful API","数据库设计","性能优化","团队协作","Git","Docker"],"starRewrite":[{"situation":"在电商项目中","task":"负责前端开发","action":"使用Vue框架开发","result":"提升了页面性能"}],"optimizedResume":"# 优化后简历 ## 个人信息 张三 | 前端开发工程师"}''',
            "expected": {
                "score": 85,
                "diagnosis_count": 1,
                "keywords_count": 10,
                "star_rewrite_count": 1,
                "has_optimized_resume": True
            }
        },
        {
            "name": "带有Markdown代码块的JSON",
            "input": '''```json
{"score":80,"diagnosis":[{"type":"建议","title":"关键词优化","description":"建议添加更多技术关键词"}],"keywords":["Python","Django","PostgreSQL","Redis"],"starRewrite":[],"optimizedResume":"# 优化后简历"}
```''',
            "expected": {
                "score": 80,
                "diagnosis_count": 1,
                "keywords_count": 4,
                "star_rewrite_count": 0,
                "has_optimized_resume": True
            }
        },
        {
            "name": "带有尾随逗号的JSON",
            "input": '''{"score":90,"diagnosis":[{"type":"警告","title":"缺乏量化结果","description":"工作经历中缺乏具体的数据支撑",}],"keywords":["JavaScript","Vue",],"starRewrite":[{"situation":"在电商项目中","task":"负责前端开发","action":"使用Vue框架开发","result":"提升了页面性能",}],"optimizedResume":"# 优化后简历",}''',
            "expected": {
                "score": 90,
                "diagnosis_count": 1,
                "keywords_count": 2,
                "star_rewrite_count": 1,
                "has_optimized_resume": True
            }
        },
        {
            "name": "带有换行符和空格的JSON",
            "input": '''{
  "score": 75,
  "diagnosis": [
    {
      "type": "错误",
      "title": "格式不一致",
      "description": "简历格式不一致"
    }
  ],
  "keywords": ["HTML", "CSS", "JavaScript"],
  "starRewrite": [],
  "optimizedResume": "# 优化后简历\n\n## 个人信息\n李四 | 前端开发工程师"
}''',
            "expected": {
                "score": 75,
                "diagnosis_count": 1,
                "keywords_count": 3,
                "star_rewrite_count": 0,
                "has_optimized_resume": True
            }
        },
        {
            "name": "带有单引号的JSON",
            "input": "{\'score\':85,\'diagnosis\':[{\'type\':\'警告\',\'title\':\'缺乏量化结果\',\'description\':\'工作经历中缺乏具体的数据支撑\'}],\'keywords\':[\'JavaScript\',\'Vue\'],\'starRewrite\':[],\'optimizedResume\':\'# 优化后简历\'}",
            "expected": {
                "score": 85,
                "diagnosis_count": 1,
                "keywords_count": 2,
                "star_rewrite_count": 0,
                "has_optimized_resume": True
            }
        },
        {
            "name": "带有注释的JSON",
            "input": '''{"score":88,"diagnosis":[{"type":"建议","title":"添加项目成果","description":"建议添加量化的项目成果"}],"keywords":["React","Node.js","MongoDB"],"starRewrite":[],"optimizedResume":"# 优化后简历"}''',
            "expected": {
                "score": 88,
                "diagnosis_count": 1,
                "keywords_count": 3,
                "star_rewrite_count": 0,
                "has_optimized_resume": True
            }
        },
        {
            "name": "包含额外内容的JSON",
            "input": '''这是前面的额外内容\n{"score":92,"diagnosis":[{"type":"警告","title":"缺乏项目经验","description":"建议添加更多项目经验"}],"keywords":["Java","Spring","MySQL"],"starRewrite":[],"optimizedResume":"# 优化后简历"}这是后面的额外内容''',
            "expected": {
                "score": 92,
                "diagnosis_count": 1,
                "keywords_count": 3,
                "star_rewrite_count": 0,
                "has_optimized_resume": True
            }
        }
    ]
    
    # 运行测试用例
    passed = 0
    failed = 0
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"测试用例 {i}/{len(test_cases)}: {test_case['name']}")
        print(f"输入长度: {len(test_case['input'])}字符")
        print(f"输入前50字符: {test_case['input'][:50]}...")
        
        try:
            # 执行解析
            result = parse_markdown_result(test_case['input'])
            
            # 验证结果
            actual = {
                "score": result['score'],
                "diagnosis_count": len(result['diagnosis']),
                "keywords_count": len(result['keywords']),
                "star_rewrite_count": len(result['starRewrite']),
                "has_optimized_resume": bool(result['optimizedResume'])
            }
            
            # 检查是否符合预期
            passed_test = True
            
            if actual['score'] != test_case['expected']['score']:
                print(f"  ❌ 评分不符合预期: {actual['score']} != {test_case['expected']['score']}")
                passed_test = False
            
            if actual['diagnosis_count'] < test_case['expected']['diagnosis_count']:
                print(f"  ❌ 诊断意见数量不符合预期: {actual['diagnosis_count']} < {test_case['expected']['diagnosis_count']}")
                passed_test = False
            
            if actual['keywords_count'] < test_case['expected']['keywords_count']:
                print(f"  ❌ 关键词数量不符合预期: {actual['keywords_count']} < {test_case['expected']['keywords_count']}")
                passed_test = False
            
            if actual['star_rewrite_count'] < test_case['expected']['star_rewrite_count']:
                print(f"  ❌ STAR重写数量不符合预期: {actual['star_rewrite_count']} < {test_case['expected']['star_rewrite_count']}")
                passed_test = False
            
            if actual['has_optimized_resume'] != test_case['expected']['has_optimized_resume']:
                print(f"  ❌ 优化后简历不符合预期: {actual['has_optimized_resume']} != {test_case['expected']['has_optimized_resume']}")
                passed_test = False
            
            if passed_test:
                print("  ✓ 测试通过！")
                passed += 1
            else:
                print("  ✗ 测试失败！")
                failed += 1
                print(f"  实际结果: {actual}")
                print(f"  预期结果: {test_case['expected']}")
                
        except Exception as e:
            print(f"  ✗ 测试异常: {type(e).__name__}: {e}")
            failed += 1
        
        print()
    
    # 输出测试报告
    print("=== 测试报告 ===")
    print(f"总测试用例: {len(test_cases)}")
    print(f"通过: {passed}")
    print(f"失败: {failed}")
    print(f"通过率: {passed/len(test_cases)*100:.1f}%")
    
    if failed == 0:
        print("\n🎉 所有测试用例通过！JSON解析功能正常工作。")
        return True
    else:
        print("\n❌ 部分测试用例失败，请检查解析函数。")
        return False

if __name__ == "__main__":
    success = test_json_parsing()
    sys.exit(0 if success else 1)

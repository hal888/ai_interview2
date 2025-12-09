## 问题分析
当前系统的简历ID生成机制存在问题：
1. `save_resume`函数硬编码返回`resume_id = "1"`，没有真正生成唯一ID
2. 这导致所有上传的简历都使用相同的ID，无法区分不同用户的简历

## 解决方案
修改`save_resume`函数，使用UUID生成唯一的resumeId：
1. 移除硬编码的resumeId
2. 使用`uuid`库生成唯一标识符
3. 确保每次调用都生成不同的ID
4. 保持与现有代码的兼容性

## 具体修改
1. 修改`file_service.py`中的`save_resume`函数：
   - 替换硬编码的`resume_id = "1"`
   - 使用`uuid.uuid4().hex[:8]`生成8位唯一ID
   - 确保ID格式符合现有代码预期

2. 验证修改效果：
   - 上传简历后，检查后端返回的resumeId是否唯一
   - 检查localStorage中保存的resumeId是否正确
   - 确保其他页面能正确获取和使用resumeId

## 预期效果
修复后，每次上传简历都会生成一个唯一的resumeId，确保不同用户的简历能被正确区分和保存。
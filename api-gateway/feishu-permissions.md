# 📋 飞书开放平台权限配置指南

## 步骤 1: 创建应用

1. 访问 [飞书开放平台](https://open.feishu.cn/)
2. 登录企业管理员账号
3. 点击「企业自建应用」→「创建应用」
4. 填写应用信息：
   - **应用名称**: 机器人 API 网关
   - **应用图标**: 上传一个图标（可选）
   - **应用描述**: 提供机器人数据库的公开 API 接口

## 步骤 2: 获取应用凭证

1. 进入应用管理页面
2. 点击「凭证与基础信息」
3. 记录以下信息（后续部署需要）：
   - **App ID**: `cli_xxxxxxxxxxxxx`
   - **App Secret**: 点击「获取」并保存（只显示一次！）

## 步骤 3: 配置权限

### 3.1 开通多维表格权限

1. 点击左侧菜单「权限管理」
2. 点击「开通权限」
3. 搜索并添加以下权限：

| 权限名称 | 权限标识 | 用途 |
|----------|----------|------|
| 获取多维表格数据 | `bitable:app` | 读取机器人数据 |
| 编辑多维表格数据 | `bitable:table` | 创建/更新机器人记录 |

4. 点击「申请开通」
5. 等待管理员审批（如果是自己创建的应用，自动通过）

### 3.2 配置权限范围

1. 在「权限管理」页面
2. 确认权限已开通
3. 设置权限范围：
   - 选择「指定应用」
   - 添加你的机器人数据库 Bitable

## 步骤 4: 配置发布范围

1. 点击左侧菜单「版本管理与发布」
2. 点击「发布范围」
3. 添加以下范围：
   - **全公司**（如果内部使用）
   - 或指定部门/人员

## 步骤 5: 启用应用

1. 点击「版本管理与发布」
2. 点击「创建版本」
3. 填写版本号（如 v1.0.0）和更新说明
4. 点击「发布」
5. 状态变为「已启用」

## 步骤 6: 获取 tenant_access_token

使用以下 API 测试凭证是否正确：

```bash
curl -X POST https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal \
  -H "Content-Type: application/json" \
  -d '{
    "app_id": "你的 App ID",
    "app_secret": "你的 App Secret"
  }'
```

成功响应：
```json
{
  "code": 0,
  "msg": "success",
  "tenant_access_token": "t-xxxxxxxxxxxxx",
  "expire": 7140
}
```

## 步骤 7: 测试 API 权限

使用获取的 token 测试读取 Bitable 数据：

```bash
curl -X GET "https://open.feishu.cn/open-apis/bitable/v1/apps/XC2nbCyx3acaPls7bsRcVOBnnOh/tables/tbl6iFEirXgZhoXP/records" \
  -H "Authorization: Bearer t-xxxxxxxxxxxxx"
```

## 常见问题

### Q1: 权限申请被拒绝
- 联系企业管理员审批
- 或自己用管理员账号创建应用

### Q2: tenant_access_token 获取失败
- 检查 App ID/Secret 是否正确
- 确认应用已启用
- 检查企业是否开通开放平台

### Q3: API 返回无权限
- 确认权限已开通
- 检查权限范围是否包含目标 Bitable
- 等待 1-2 分钟让权限生效

## 安全建议

1. **保护 App Secret**
   - 不要提交到代码仓库
   - 使用环境变量或密钥管理服务
   - 定期轮换

2. **最小权限原则**
   - 只申请必要的权限
   - 限制访问范围
   - 定期审查权限

3. **监控异常**
   - 在飞书开放平台查看 API 调用日志
   - 设置异常告警

## 后续步骤

完成权限配置后：
1. ✅ 将 App ID/Secret 配置到 Cloudflare Workers
2. ✅ 测试 API 接口
3. ✅ 创建 API Key 分发给调用方

---

**需要帮助？** 查看 [飞书开放平台文档](https://open.feishu.cn/document/ukTMzUjL4YDM00iN2ATN)

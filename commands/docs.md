# /docs - 文档生成命令

trigger: /docs [module|file] [--type=api|readme|tutorial] [--output=path]

## Description
为指定模块或文件生成技术文档。

## Arguments

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| module|file | string | ✗ | 当前目录 | 目标模块/文件 |
| --type | string | ✗ | auto | 文档类型 (api/readme/tutorial/changelog) |
| --output | string | ✗ | docs/ | 输出目录 |
| --language | string | ✗ | zh-CN | 文档语言 (zh-CN/en) |

## Handler

1. **分析目标**
   - 读取源代码
   - 提取函数/类签名
   - 识别注释和类型

2. **选择模板**
   - 根据 --type 选择文档模板
   - 或自动判断最合适的类型

3. **生成文档**
   - 调用 documentation skill
   - 或启动 documentation-writer agent
   - 填充模板内容

4. **保存输出**
   - 写入指定目录
   - 更新索引文件
   - 报告生成结果

## Examples

```bash
# 为当前模块生成 API 文档
/docs

# 为指定文件生成文档
/docs src/auth.ts

# 生成 README
/docs --type=readme --output=.

# 生成教程
/docs src/ --type=tutorial --output=docs/tutorials/

# 生成英文文档
/docs src/api/ --type=api --language=en
```

## Output Example

```markdown
# Auth Module API 文档

## 概述
认证模块提供用户登录、注册、会话管理等功能。

## 快速开始

### 导入
```typescript
import { AuthService } from './auth';
```

### 初始化
```typescript
const auth = new AuthService({
  secretKey: process.env.AUTH_SECRET,
  tokenExpiry: '24h'
});
```

## API 参考

### `login(credentials)`
用户登录

**参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| credentials | object | ✓ | 登录凭证 |
| credentials.email | string | ✓ | 邮箱 |
| credentials.password | string | ✓ | 密码 |

**返回**: `Promise<AuthToken>`

**示例**:
```typescript
const token = await auth.login({
  email: 'user@example.com',
  password: 'password123'
});
```

**错误**:
| 错误码 | 说明 |
|--------|------|
| INVALID_CREDENTIALS | 凭证无效 |
| ACCOUNT_LOCKED | 账户已锁定 |
```

## Related
- skill: documentation
- agent: documentation-writer
- command: /review, /research

## Notes
- 文档与代码同步更新
- 优先文档化公共 API
- 定期审查文档时效性

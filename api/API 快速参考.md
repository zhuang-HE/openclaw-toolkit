# 🚀 三个数据库 API - 快速参考

## 📌 一句话总结

三个数据库 API 服务已全部部署完成，支持 REST API 调用、Swagger 文档、API Key 认证。

---

## 🌐 快速访问

```bash
# 机器人数据库
http://localhost:8000/docs

# 无人机数据库  
http://localhost:8081/docs

# 临床试验数据库
http://localhost:8082/docs
```

---

## 🔑 API Keys（测试用）

```
机器人：sk_robot_demo_key_123456
无人机：sk_drone_demo_key_123456
临床：sk_clinical_demo_key_123456
```

---

## 💻 快速测试

```bash
# 机器人统计
curl "http://localhost:8000/api/stats" -H "X-API-Key: sk_robot_demo_key_123456"

# 无人机统计
curl "http://localhost:8081/api/stats" -H "X-API-Key: sk_drone_demo_key_123456"

# 临床统计
curl "http://localhost:8082/api/stats" -H "X-API-Key: sk_clinical_demo_key_123456"
```

---

## 🛠️ 运维命令

```bash
# 启动所有
cd /home/admin/.openclaw/workspace/api && bash start_all_apis.sh

# 查看状态
ps aux | grep -E "robot_api|drone_api|clinical_api" | grep -v grep

# 查看端口
netstat -tlnp | grep -E "8000|8081|8082"

# 停止所有
pkill -f robot_api_server.py
pkill -f drone_api_server.py
pkill -f clinical_trial_api_server.py
```

---

## 📊 数据概览

| 数据库 | 数据量 | 主要功能 |
|--------|--------|----------|
| 机器人 | 24 款产品 | 产品搜索、公司统计、事故统计 |
| 无人机 | 17 款机型 | 品牌分布、销量统计、事故分析 |
| 临床 | 10 例事故 | 案例搜索、分期统计、费率查询 |

---

## 📖 详细文档

`/home/admin/.openclaw/workspace/api/三个数据库 API 服务_部署报告.md`

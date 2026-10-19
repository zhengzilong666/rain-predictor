# Rain Predictor - End-to-End MLOps Project

这是一个基于 FastAPI 和机器学习（随机森林）的明日降雨预测系统。项目实现了从数据管理、模型训练到自动化部署的完整 MLOps 生命周期。

## 技术栈
- **数据版本控制**: DVC
- **实验追踪**: MLflow
- **后端**: FastAPI
- **前端**: HTML + JavaScript
- **容器化**: Docker
- **CI/CD**: GitHub Actions

## 分支触发流程
- **Pull Request**: 触发自动化测试和 Docker 构建检查。
- **Push to main**: 触发生产环境的 CI/CD 流水线。

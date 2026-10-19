# Rain Predictor - End-to-End MLOps Project

这是一个基于 FastAPI 和机器学习（随机森林）的明日降雨预测系统。项目实现了从数据管理、模型训练到自动化部署的完整 MLOps 生命周期。

## 技术栈
- **数据版本控制**: DVC
- **实验追踪**: MLflow
- **后端**: FastAPI
- **前端**: HTML + JavaScript
- **容器化**: Docker
- **CI/CD**: GitHub Actions

## 代码流转与 CI/CD 流水线说明

本项目的开发与交付流程严格遵循标准的 DevOps 规范，代码的生命周期流转如下：

1. **提交 (Commit)**：开发者在 `feature/xxx` 分支进行代码开发，并提交至本地 Git。
2. **构建与测试 (Build & Test - CI)**：向 `dev` 或 `staging` 分支发起 Pull Request 时，GitHub Actions 会自动触发 **CI Pipeline**（`.github/workflows/ci.yml`）。
   - 运行 `ruff` 进行静态代码检查。
   - 运行 `pytest` 执行全部边界条件测试。
   - 运行 `docker build` 验证镜像是否可以成功构建。
3. **预发环境 (Staging - CD)**：当代码通过 PR 合并至 `staging` 分支时，流水线会使用 GitHub Secrets 中针对 staging 的环境变量生成 `.env` 文件，并构建带有 `staging` 标签的 Docker 镜像。
4. **生产环境 (Production - CD)**：当 `staging` 验证通过，合并至 `main` 主干时，流水线会自动读取生产环境的 Secrets 生成 `.env`，并构建最终的 `production` Docker 镜像。

### 分支触发规则
- **Pull Request (向 dev/staging/main 发起)**：触发 `test-lint-build` 检查。
- **Push to `staging`**：触发 `test-lint-build` + `deploy-staging`。
- **Push to `main`**：触发 `test-lint-build` + `deploy-production`。
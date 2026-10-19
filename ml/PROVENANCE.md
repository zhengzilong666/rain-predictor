# 模型溯源说明 (Provenance)

本项目通过自动化流程严格记录了模型的血缘关系：
- **代码版本**：训练时自动通过 Git 获取 Commit SHA，并将其记录在 MLflow 的 Tag 中。
- **数据版本**：读取 DVC 文件中的 MD5 哈希值，记录在 MLflow 中。
- **可复现性**：任何人可以通过 `git checkout <commit_sha>` 和 `dvc checkout` 完美复现出产生该生产模型的所有环境和数据。
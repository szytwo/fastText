## fork

https://github.com/facebookresearch/fastText

## 安装

```
python -m venv venv
venv\Scripts\activate

# 1️⃣ 安装核心依赖（FastAPI + uvicorn + fasttext-wheel）
pip install fastapi uvicorn fasttext-wheel -i https://pypi.tuna.tsinghua.edu.cn/simple

# 2️⃣ 卸载现有 numpy（如果有 2.x 的话）
pip uninstall numpy -y

# 3️⃣ 安装兼容 fasttext 的 numpy 1.x
pip install "numpy<2.0" -i https://pypi.tuna.tsinghua.edu.cn/simple

python -m uvicorn fasttext_server:app --host 0.0.0.0 --port 9231 --workers 2


nvidia-smi -L  # 查看GUID

```

## GIT

```
git pull # 拉取
git push # 推送

git branch -r # 查看分支
git branch -m master # 重命名分支
git branch --set-upstream-to=origin/master master #关联远程分支origin/master 

git remote -v # 查看远程仓库
git remote remove origin # 移除远程仓库连接，origin，upstream

# 添加新的远程仓库，origin，upstream
git remote add upstream https://github.com/facebookresearch/fastText.git

git fetch upstream # 从远程仓库拉取更新，origin，upstream
git checkout master # 切换到主分支
git merge upstream/master # 合并到本地分支,主分支名称可能是 ，origin，upstream，master,main 

git reset --hard origin/master # 强制覆盖本地代码

```
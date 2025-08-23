这个项目是仿照git的逻辑来实现一个版本控制系统的，主要功能包括：
- 初始化仓库
- 添加文件到暂存区
- 提交更改
- 查看状态
- 查看提交历史
- 创建分支
- 移动到分支或某次提交
先来设计一下语法
- 主体是sjy 
- 初始化仓库 sjy init 只能在当前文件夹下面初始化，建立一个类似于.git的文件夹
- 添加文件到暂存区 sjy add <file>，只能显式指定文件
- 提交更改 sjy commit -m "message"，只能严格按照这种形式
- 查看状态 sjy status，列出各个文件的状态，有没有被追踪，用不同颜色的文字显示
- 查看提交历史 sjy log，列出当前分支的所有提交信息
- 创建分支 sjy branch <branch_name>
- 移动到分支或某次提交 sjy checkout <branch_name or commit_id>
先写一个test 工具

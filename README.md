**这个项目是仿照git的逻辑来实现一个版本控制系统的，主要功能包括：**
- 初始化仓库
- 添加文件到暂存区
- 提交更改
- 查看状态
- 查看提交历史
- 创建分支
- 移动到分支或某次提交
先来设计一下语法
- 主体是sjy 
- sjy init
- sjy add <file>
- sjy commit -m "message"
- sjy status
- sjy log
- sjy branch <branch_name>
- sjy checkout <branch_name or commit_id>

先写一个test 工具

**具体行为**
- init
  - 在当前目录下建立.sjy文件夹，如果已经有了这个文件夹就不做操作（和git行为不一样，git会重写某些东西，具体可以问gpt）
  - .sjy文件夹下面会有一些文件夹或文件，等用到再说
- add <file>
  - 默认一次只能添加一个文件
  - 在.sjy/index中存文件的相对workind-repo的相对路径和内容的哈希，如果这个文件已经被放在index中可能要更新哈希
  - 把文件压缩之后存在.sjy/objects中的文件里面，这个文件的地址做法和git类似，前两位作为文件夹名字，后面的作为文件名，压缩用gzip压缩，然后二进制存储
  - index采用csv格式存读，和git的二进制不一样，用os.system touch建立index
  - 计算哈希，存入objects中，读取index，如果文件哈希改变了才更新，如果文件不存在，直接加入到最后，然后再排序
- commit -m "message"
  - commit构造tree，tree存放文件名和对应的哈希
  - tree存放在objects中，哈希计算方式和文件一样
  - 还没有支持branch，先建立一个head，存当前的提交哈希，现在的设计还没有支持多分支，没有refs文件
  - 现在.sjy中建一个HEAD


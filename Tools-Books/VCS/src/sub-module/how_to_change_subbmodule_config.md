# 子模块路径错误，如何变更?

1. 删除子模块

   ```bash
   # 逆初始化模块，其中{MOD_NAME}为模块目录，执行后可发现模块目录被清空
   git submodule deinit {MOD_NAME}
   # 删除.gitmodules中记录的模块信息（--cached选项清除.git/modules中的缓存）
   git rm --cached {MOD_NAME}
   # 提交更改到代码库，可观察到'.gitmodules'内容发生变更
   git commit -am "Remove a submodule."
   ```

2. 修改某模块 URL

   - 修改'.gitmodules'文件中对应模块的”url“属性;
   - 使用 git submodule sync 命令，将新的 URL 更新到文件.git/config；

   ```bash
   git submodule sync
   ```

# Single-side-scanner-solution
解决只能进行单面扫描的扫描仪的问题
## 使用
1. 将一叠文稿从进纸器分别进行正反两次扫描，生成两个pdf文件
2. 将脚本复制到保存pdf文件的目录下
3. 运行脚本或在Python命令行/其他Py脚本中import本脚本
设想的扫描情况：奇数页pdf文件正序，偶数页pdf文件倒序，两文件页数相同。如果文档太厚没法一次扫完，奇数页和偶数页可以分别分成多份扫描，使用时先connect，再merge。直接运行脚本使用的不需要看下面两节。

### connector(f1n, f2n, out):

将 `f1n`、`f2n ` 直接连起来，`f1n` 在前，输出成 `out`。在文档太厚没法一次性扫完时使用。

### merger(oname, ename, out)

假设你已经准备好了一份文档的奇数页和偶数页pdf文件，将奇数页文件 `oname` 和偶数页文件 `ename` 合并，输出成 `out`。

## 依赖于

- [PyPDF2](https://github.com/mstamy2/PyPDF2) `pip install PyPDF2`

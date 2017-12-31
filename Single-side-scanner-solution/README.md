# Single-side-scanner-solution
解决只能进行单面扫描的扫描仪的问题
## 使用
1. 将一叠文稿从进纸器分别进行正反两次扫描，生成两个pdf文件
2. 将脚本复制到保存pdf文件的目录下
3. 运行MergePDF脚本，填入奇数页和偶数页的pdf文件名和输出文件名
4. ConnectPDF用来将无法一次扫描的文档连起来（如果纸质版太厚导致塞不进进纸器的话）
## 依赖于
- Python 3.x
- [PyPDF2](https://github.com/mstamy2/PyPDF2) `pip install PyPDF2`

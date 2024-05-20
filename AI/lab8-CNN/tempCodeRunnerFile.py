source_dir="./test"
# destination_dir="./test_plus"
# os.makedirs("./test_plus",False)
# os.makedirs("./test_plus/baihe")
# os.makedirs("./test_plus/dangshen")
# os.makedirs("./test_plus/gouqi")
# os.makedirs("./test_plus/huaihua")
# os.makedirs("./test_plus/jinyinhua")
# ##读取test里面的文件并且转移
# for filename in os.listdir(source_dir):
#     #构建完整的source路径
#     file_path=os.path.join(source_dir,filename)
#     if "baihe" in filename:
#         destination_path="./test_plus/baihe"
#     elif "dangshen" in filename:
#          destination_path="./test_plus/dangshen"
#     elif "gouqi" in filename:
#          destination_path="./test_plus/gouqi"
#     elif "huaihua" in filename:
#          destination_path="./test_plus/huaihua"  
#     elif "jinyinhua" in filename:
#          destination_path="./test_plus/jinyinhua"
#     destination_path=os.path.join(destination_path,filename)
#     shutil.move(file_path, destination_path)  
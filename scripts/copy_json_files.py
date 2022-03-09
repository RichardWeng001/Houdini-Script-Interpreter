import os

#a custom environment variable
#hou.homeHoudiniDirectory() value
home_path = 'C:\\Users\\dell\\Documents\\houdini19.0'

target_dir_path = f'{home_path}\\packages\\hou_interpreter\\'

source_dir_path = f'{os.getcwd()}\\jsons\\'

for file in os.listdir(source_dir_path):
    if file.endswith('.json'):
        #json file
        try:
            source_path = source_dir_path + file
            target_path = target_dir_path + file
            src_fd = os.open(source_path, os.O_RDONLY)
            src_size = os.path.getsize(source_path)
            data = os.read(src_fd, src_size)
            os.close(src_fd)
            tar_fd = os.open(target_path, os.O_RDWR|os.O_CREAT)
            os.write(tar_fd, data)
            os.close(tar_fd)
            print(f'{file} copyed!')
        except:
            raise OSError(source_path, target_path)


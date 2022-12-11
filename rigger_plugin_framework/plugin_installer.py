# -*- coding:utf-8

import os
import tarfile
import shutil
import sys
import zipfile
from rigger_singleton.singleton import singleton

requirements_dir = "requirements"
@singleton
class PluginInstaller:
    """
    插件安装器，用于将指定插件安装到项目中
    """

    @staticmethod
    def install(file_path, dest_dir):
        assert os.path.exists(file_path)
        # 确保安装路径存在且合法
        PluginInstaller.make_sure_dir(dest_dir)

        assert os.path.exists(dest_dir)
        # 获取解压后的文件名
        prefix, file_name = os.path.split(file_path)
        if file_name.endswith(".tar.gz"):
            with tarfile.open(file_path) as fp:
                def is_within_directory(directory, target):
                    
                    abs_directory = os.path.abspath(directory)
                    abs_target = os.path.abspath(target)
                
                    prefix = os.path.commonprefix([abs_directory, abs_target])
                    
                    return prefix == abs_directory
                
                def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
                
                    for member in tar.getmembers():
                        member_path = os.path.join(path, member.name)
                        if not is_within_directory(path, member_path):
                            raise Exception("Attempted Path Traversal in Tar File")
                
                    tar.extractall(path, members, numeric_owner=numeric_owner) 
                    
                
                safe_extract(fp, path=dest_dir)
                fp.close()
            file_name = file_name[: -7]
            info_file: str = os.path.join(dest_dir, file_name, "PKG-INFO")
            if not os.path.exists(info_file):
                raise Exception("now only support pip package style plugin")
            pkg_name = ""
            with open(info_file, "r") as fp:
                for line in fp:
                    if line.startswith("Name:"):
                        pre, pkg_name = line.split(":")
                        pkg_name = pkg_name.strip()
                        break
                fp.close()

            if pkg_name != "":
                pkg_name = os.path.join(dest_dir, pkg_name)
                # 如果原来已经存在，则删除
                if os.path.exists(pkg_name):
                    shutil.rmtree(pkg_name)
                    # 重命名
                os.rename(os.path.join(dest_dir, file_name), pkg_name)
                # 安装插件的依赖
                PluginInstaller.install_requirements(pkg_name, dest_dir)
        elif file_name.endswith(".whl"):
            temp_dir = os.path.join(dest_dir, "temp")
            with zipfile.ZipFile(file_path) as fp:
                fp.extractall(path=temp_dir)
                fp.close()
            # 在临时文件夹中查找WHEEL文件以确定真正的包
            for d in os.listdir(temp_dir):
                p = os.path.join(temp_dir, d)
                if os.path.isdir(p):
                    # 是否存在WHEEL文件
                    if os.path.exists(os.path.join(p, "WHEEL")):
                        continue
                    else:
                        target_name = os.path.join(dest_dir, d)
                        if os.path.exists(target_name):
                            shutil.rmtree(target_name)
                        os.rename(p, target_name)
                        # 移除临时目录
                        shutil.rmtree(temp_dir)
                        # 安装插件的依赖
                        PluginInstaller.install_requirements(target_name, dest_dir)
                        break

    @staticmethod
    def install_requirements(path: str, dest: str):
        path = os.path.join(path, requirements_dir)
        if os.path.exists(path):
            for file in os.listdir(path):
                if PluginInstaller.check_file_name(file):
                    temp = os.path.join(path, file)
                    PluginInstaller.install(temp, dest)

    @staticmethod
    def make_sure_dir(directory):
        if os.path.exists(directory):
            if os.path.isdir(directory):
                pass
            else:
                raise Exception(directory + " is not a valid dir, please check!")
        else:
            os.mkdir(directory)

    @staticmethod
    def check_file_name(file_name: str):
        import os
        (part1, part2) = os.path.splitext(file_name)
        if part2 == "":
            return part1 in [".gz", ".whl"]
        else:
            return part2 in [".gz", ".whl"]





import os
import shutil


def del_dir_contents(dir_name_path):
    print("\n** Deleting files/directories in: {} **\n".format(dir_name_path))
    for filename in os.listdir(dir_name_path):
        filename_path = os.path.join(dir_name_path, filename)
        try:
            if os.path.isfile(filename_path) or os.path.islink(filename_path):
                os.unlink(filename_path)
            elif os.path.isdir(filename_path):
                shutil.rmtree(filename_path)
            print("\n** Deleted file: {} **\n".format(filename_path))
        except Exception as e:
            print("\n** Failed to delete ** : {0} - Reason: {1}\n".format(filename_path, e))


def prepare_dir(dir_name):
    dir_name_path = os.path.join(os.getcwd(), dir_name)
    if os.path.isdir(dir_name_path):
        del_dir_contents(dir_name_path)
    else:
        print("\n** Making directory: {} **\n".format(dir_name_path))
        os.mkdir(dir_name_path)

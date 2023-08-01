import os
import json
import yaml

class sastre_ansible(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def list_files_with_count(self, path):
        file_name_count = dict()
        try:
            for root, subFolder, files in os.walk(path):
                for item in files:
                    if item.endswith(".txt") or item.endswith(".json"):
                        fileNamePath = str(os.path.join(root, item))
                        with open(fileNamePath, 'r') as fp:
                            line_count = len(fp.readlines())
                        file_name_count[fileNamePath] = line_count
                        print(os.path.dirname(os.path.normpath(fileNamePath)))
        except FileNotFoundError as err:
            raise AssertionError(err)
        return file_name_count

    def is_playbook_success(self, task_name, ansible_output, ansible_host=None, msg=None):
        ansible_host = ansible_host or 'localhost'
        ansible_json_str = ansible_output[ansible_output.index('{'):]
        ansible_json_output = json.loads(ansible_json_str)
        if 'stats' in ansible_json_output and ansible_host in ansible_json_output['stats']:
            ansible_stats = ansible_json_output['stats'][ansible_host]
            if ansible_stats['ok'] > 0 and ansible_stats['failures'] == 0 and ansible_stats['unreachable'] == 0:
                return True
        raise AssertionError(msg or f'{task_name} task failed....')

    def compare_show_template_values_attach_detach(self, csv_files_with_attachment, csv_files_with_out_attachment, is_edge: bool,
                                                     msg=None):
        try:
            print(f'path1: {csv_files_with_attachment}, path2: {csv_files_with_out_attachment}, is_edge: {is_edge}, msg: {msg}')
            files_with_attachment = {str(filename) for filename in os.listdir(csv_files_with_attachment)}
            invalid_files = [str(filename) for filename in os.listdir(csv_files_with_out_attachment)
                             if not str(filename).startswith("template_values_vsmart") and 
                             str(filename) in files_with_attachment
                            ] if is_edge else [str(filename) for filename in os.listdir(csv_files_with_out_attachment)
                             if  str(filename).startswith("template_values_vsmart") and 
                             str(filename) in files_with_attachment]
            if len(invalid_files) > 0:
                raise AssertionError(
                    msg or f'show template values no attachment task has invalid files : {invalid_files}')
        except FileNotFoundError as err:
            raise AssertionError(err)
        except Exception as err:
            raise AssertionError(err)

    def csv_folders_should_be_equal(self, csv_folder1, csv_folder2, msg=None):
        try:
            print(f'csv_folder1: {csv_folder1}, csv_folder2: {csv_folder2}, msg: {msg}')
            files_are_equal = True
            csv_files1 = {str(filename) for filename in os.listdir(csv_folder1)}
            csv_files2 = set()
            for filename in os.listdir(csv_folder2):
                if str(filename) not in csv_files1:
                    files_are_equal = False
                csv_files2.add(str(filename))

            if len(csv_files1) != len(csv_files2) or not files_are_equal:
                raise AssertionError(
                    msg or f'Both csv folders has different files - {csv_folder1}:{csv_files1}, {csv_folder2}:{csv_files2}')

            for csv_file in csv_files1:
                with open(os.path.join(csv_folder1, csv_file), 'r') as file1, open(os.path.join(csv_folder2, csv_file), 'r') as file2:
                    file1_csv = file1.readlines()
                    file2_csv = file2.readlines()
                if len(file1_csv) != len(file2_csv):
                    raise AssertionError(
                        msg or f'Both csv folders, this file length is not equal - {csv_folder1}/{csv_file}, {csv_folder2}/{csv_file}')
                for line in file1_csv:
                    if line not in file2_csv:
                        raise AssertionError(
                            msg or f'Both csv folders files are not equal, line "{line}" not found in  {csv_folder2}/{csv_file}')
        except FileNotFoundError as err:
            raise AssertionError(err)
        return True

    def csv_files_should_be_equal(self, csv_file1, csv_file2, columnIndex:int=-1, msg=None):
        try:
            print(f'csv_file1: {csv_file1}, csv_file2: {csv_file2}, columnIndex: {columnIndex}, msg: {msg}')
            with open(os.path.join(csv_file1), 'r') as file1, open(os.path.join(csv_file2), 'r') as file2:
                file1_csv = file1.readlines()
                file2_csv = file2.readlines()
            if len(file1_csv) != len(file2_csv):
                raise AssertionError(
                    msg or f'file length are not equal - {csv_file1}, {csv_file2}')
            if columnIndex == -1: # compares all columns
                for line in file1_csv:
                    if line not in file2_csv:
                        raise AssertionError(
                            msg or f'files are not equal, line "{line}" not found in  {csv_file2}')
            else:# compares specific column given in method arguments (argName : columnIndex)
                column_values1 = set()
                column_values2 = set()
                for line in file1_csv:
                    column_values1.add(line.split(',')[columnIndex])
                for line in file2_csv:
                    column_values2.add(line.split(',')[columnIndex])
                if column_values1 != column_values2:
                    raise AssertionError(
                        msg or f'files are not equal {csv_file1}, {csv_file2}')
        except FileNotFoundError as err:
            raise AssertionError(err)
        return True
    
    def compare_yml_files(self, yml_file1, yml_file2, compare_equal=True, msg=None):
        try:
            print(f'yml_file1: {yml_file1}, yml_file2: {yml_file2}, compare_equal: {compare_equal}, msg: {msg}')
            with open(yml_file1, 'r') as file1:
                data1 = yaml.load(file1, Loader=yaml.FullLoader)
            with open(yml_file2, 'r') as file2:
                data2 = yaml.load(file2, Loader=yaml.FullLoader)

            if compare_equal:
                if data1 != data2:
                    raise AssertionError(
                            msg or f'yaml files are not equal {yml_file1}, {yml_file2}')
            else:
                if data1 == data2:
                    raise AssertionError(
                            msg or f'yaml files are equal {yml_file1}, {yml_file2}')
        except FileNotFoundError as err:
            raise AssertionError(err)
        return True
    def get_files_without_extension(self, base_directory, exclude_names=None, exclude_dirs=None):
        file_names = set()
        exclude_names = exclude_names or []
        exclude_dirs = exclude_dirs or []
        
        for root, dirs, files in os.walk(base_directory, topdown=True):
            # Exclude specific directory names
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for file in files:
                file_name, file_extension = os.path.splitext(file)
                
                # Exclude specific file names
                if file_name not in exclude_names and file_extension:
                    file_names.add(file_name)
        
        return file_names

    def is_transform_rename_success(self, backup, rename_dir, name_suffix=''):
        try:
            print(f'backup: {backup}, transform_rename_output_dir: {rename_dir}, name_suffix: {name_suffix}')
            exclude_names = ['server_info']
            exclude_dirs = ['inventory', 'certificates', 'device_configs']
            file_names_workdir = self.get_files_without_extension(backup, exclude_names, exclude_dirs)
            file_names_transform_rename = self.get_files_without_extension(rename_dir, exclude_names, exclude_dirs)
            for filename in file_names_workdir:
                filename_suffix = filename+name_suffix
                if filename_suffix not in file_names_transform_rename:
                    raise AssertionError(f'filename {filename_suffix} not found in transform_rename_output_dir: {rename_dir}')
        except FileNotFoundError as err:
            raise AssertionError(err)
        return True
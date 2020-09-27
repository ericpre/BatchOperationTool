# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 11:38:34 2015

@author: eric
"""
import os


class FileFilter():
    """
    TODO: consider 'ignore_filename_extension_list'
    """

    def __init__(self, dname, subdirectory_bool, string_list, extension_list,
                 ignore_string_bool, ignore_string_list,
                 ignore_string_path_bool, ignore_string_path_list,
                 ignore_filename_extension_bool=None, ignore_filename_extension_list=None):
        self.dname = dname
        self.subdirectory_bool = subdirectory_bool

        # parameters form the parameters dictionnary
        self.string_list = self._set_list(string_list)
        self.extension_list = self._set_extension_list(extension_list)
        self.ignore_string_bool = ignore_string_bool
        self.ignore_string_list = self._set_list(ignore_string_list)
        self.ignore_string_path_bool = ignore_string_path_bool
        self.ignore_string_path_list = self._set_list(ignore_string_path_list)
        if ignore_filename_extension_bool is None:
            self.ignore_filename_extension_bool = False
        else:
            self.ignore_filename_extension_bool = ignore_filename_extension_bool
            self.ignore_filename_extension_list = self._set_list(
                ignore_filename_extension_list)

        self.files_to_use_list = []
        self.files_to_ignore_list = []

    def _get_conditional_files_list(self, files_list, path):
        for filename in files_list:
            fullfilename = os.path.join(path, filename)
            fname, ext = os.path.splitext(filename)
            if self._pass_ignore_if_same_file_with_extension_condition(path, fname):
                if self._pass_string_in_path_condition(path):
                    if self._pass_ignore_string_in_fname_condition(fname):
                        if self._pass_string_in_fname_condition(fname):
                            if self._pass_extension_condition(ext):
                                self.files_to_use_list.append(fullfilename)
                            else:
                                self.files_to_ignore_list.append(fullfilename)
                        else:
                            self.files_to_ignore_list.append(fullfilename)
                    else:
                        self.files_to_ignore_list.append(fullfilename)
                else:
                    self.files_to_ignore_list.append(fullfilename)
            else:
                self.files_to_ignore_list.append(fullfilename)

    def get_files_lists(self):
        """ Return files to use list and files to ignore list """
        self.files_to_use_list = []
        self.files_to_ignore_list = []

        if self.subdirectory_bool:
            for root, subFolder, files_list in os.walk(self.dname):
                self._get_conditional_files_list(files_list, root)
        else:
            try:
                list_dir = os.listdir(self.dname)
            except FileNotFoundError:
                print("No such directory: '{}'".format(self.dname))
            self._get_conditional_files_list(list_dir, self.dname)

        return sorted(self.files_to_use_list), sorted(self.files_to_ignore_list)

    def _set_extension_list(self, extension_list):
        return [ext if '.' in ext else '.' + ext for ext in self._set_list(extension_list)]

    def _set_list(self, parameter):
        if isinstance(parameter, str):
            parameter = [parameter]
        return parameter

    def _pass_string_in_fname_condition(self, fname):
        """ return True for file going to files_to_use_list, when:
            - string from string_list IS in filename """
        return not self._pass_ignore_condition(True, fname, self.string_list)

    def _pass_ignore_string_in_fname_condition(self, fname):
        """ return True for file going to files_to_use_list, when:
            - ignore_string_bool is False
            OR
            - ignore_string_bool is True
            - string from string_list IS NOT in filename """
        return self._pass_ignore_condition(self.ignore_string_bool, fname,
                                           self.ignore_string_list)

    def _pass_string_in_path_condition(self, path):
        """ return True for file going to files_to_use_list, when:
            - ignore_string_path_bool is False
            OR
            - ignore_string_path_bool is True
            - string from ignore_string_path_list IS NOT in path """
        return self._pass_ignore_condition(self.ignore_string_path_bool, path,
                                           self.ignore_string_path_list)

    def _pass_ignore_if_same_file_with_extension_condition(self, path, fname):
        """ return True for file going to files_to_use_list, when:
            - ignore_filename_extension_bool is False
            OR
            - ignore_filename_extension_bool is True
                AND
            - fname+ext with ext from ignore_filename_extension_list DOES exist """
        if self.ignore_filename_extension_bool:
            for ext in self.ignore_filename_extension_list:
                if os.path.exists(os.path.join(path, '.'.join([fname, ext]))):
                    return True
                else:
                    pass
        else:
            return True
        return False  # when it passes all the case in the for loop

    def _pass_ignore_condition(self, active, string_to_check, string_list):
        """ return True for file going to files_to_use_list, when:
            - active is False
            OR
            - active is True
                AND
            - string IS NOT in string_to_check """
        if active:
            for string in string_list:
                if string in string_to_check:
                    return False
                else:
                    pass
        else:
            return True
        return True  # when it passes all the case in the for loop

    def _pass_extension_condition(self, extension):
        # ignore file if ext is not in the extension_list
        for ext in self.extension_list:
            if extension == ext:
                return True
        return False

__author__ = 'ricky'

import shutil
import logging as log
from os import path, unlink, walk, makedirs

from pandas import read_csv

from stack_trace import StackTrace


class ResourceManager(object):
    @staticmethod
    def is_path_exist(my_path):
        """
        check is a path is absolute path and exist
        :param my_path: path
        :return: boolean
        """

        if path.isabs(my_path):
            if path.exists(my_path):
                return True
            else:
                return False
        else:
            msg = "ResourceManager (is_path_exist()) : %s is not absolute path." % my_path
            log.error(msg)
            raise Exception(msg)

    @staticmethod
    def empty_dir(dir_path):
        """
        :param dir_path: directory absolute path
        :return: directory absolute path
        cleaning a directory. removing files and directory
        """
        try:
            if ResourceManager.is_path_exist(dir_path):
                for root, dirs, files in walk(dir_path):
                    for f in files:
                        log.info("deleting file %s : " % f)
                        unlink(path.join(root, f))
                        log.info("%s file deleted : " % f)
                    for d in dirs:
                        log.info("deleting directory : %s: " % d)
                        shutil.rmtree(path.join(root, d))
                        log.info("%s  directory deleted : " % d)
                log.info("%s  directory path returned : " % dir_path)
            else:
                msg = "%s directory path is not valid." % dir_path
                raise Exception(msg)
        except:
            trace_err = StackTrace.get_stack_trace()
            msg = "ResourceManager (empty_dir()) : %s%s" % ("\n", trace_err)
            log.error(msg)
            raise Exception(msg)

    @staticmethod
    def create_dir(dir_path):
        """
        :param: relative path of directory
        :return: None
        #if directory does not exists , create directory
        """
        try:
            if not ResourceManager.is_path_exist(dir_path):
                log.info("creating %s directory" % dir_path)
                makedirs(dir_path)
                log.info("%s : directory created" % dir_path)
                return dir_path
        except:
            trace_err = StackTrace.get_stack_trace()
            msg = "ResourceManager (create_dir()) : %s%s" % ("\n", trace_err)
            log.error(msg)
            raise Exception(msg)

    @staticmethod
    def read_file(file_abs_path):
        """
        :param : relative path of file
        :return: unique lines as set.
        """
        try:
            if ResourceManager.is_path_exist(file_abs_path):
                log.info("%s exists. Reading file." % file_abs_path)
                names = set()

                with open(file_abs_path, "r") as f:
                    lines = f.read().split("\n")
                    for l in lines:
                        l = l.strip()
                        if l:
                            names.add(l.lower())
                return names
            else:
                raise Exception("%s does not exists" % file_abs_path)
        except:
            trace_err = StackTrace.get_stack_trace()
            msg = "ResourceManager (read_file()) : %s%s" % ("\n", trace_err)
            log.error(msg)
            raise Exception(msg)

    @staticmethod
    def read_product_name_replace_file(csv_file_abs_path):
        """
        :param : reading the product name replace file and make key value pair
        :return: dictionary.
        """
        try:
            if ResourceManager.is_path_exist(csv_file_abs_path):
                result = {}
                log.info("%s exists. Reading csv file." % csv_file_abs_path)
                df = read_csv(csv_file_abs_path)

                for row in df.itertuples():
                    key = row[1].strip().lower()
                    val = row[2].strip().lower()

                    if key and val:
                        result[key] = val
                    else:
                        raise Exception(
                            "%s file has one column element empty. Please verify the csv file. "
                            "The two column should have some value not empty." % csv_file_abs_path)
                return result
            else:
                raise Exception("%s does not exists in resource directory." % csv_file_abs_path)
        except:
            trace_err = StackTrace.get_stack_trace()
            msg = "ResourceManager (read_product_name_replace_file()) : %s%s" % ("\n", trace_err)
            log.error(msg)
            raise Exception(msg)

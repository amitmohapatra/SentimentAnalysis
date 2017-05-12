__author__ = 'Amit Mohapatra'

from os import sep, path
from gc import collect, garbage
from collections import namedtuple

from stack_trace import StackTrace
from resource_manager import ResourceManager


class Config(object):
    """
    Make all configuration related entity to an object.
    """

    def __init__(self, project_env):
        self.base_dir = path.dirname(path.dirname(path.dirname(path.dirname(path.dirname(__file__)))))
        self.setup = self.__setup(project_env)

    def __setup(self, project_env):
        """
        :param project_env: environment type (prod, test, local)
        :return: None
        #read the config from respective folder.
        """
        try:
            config_file_path = sep.join([self.base_dir, "configuration", "%s%s" % (project_env, "_setup"), "config"])

            if ResourceManager.is_path_exist(config_file_path):
                name, val = self.__read_file(config_file_path)
                return self.__create_namedtuple(name, val)
            else:
                msg = project_env + " : config file path is not a valid path."
                raise Exception(msg)
        except:
            trace_err = StackTrace.get_stack_trace()
            msg = "Config (__setup()) : %s%s" % ("\n", trace_err)
            raise Exception(msg)

    def __create_namedtuple(self, name, val):
        """
        :param name: name list
        :param val: corresponding value list
        :return: namedtuple
        """
        try:
            obj = namedtuple('obj', ",".join(name))
            return obj._make(val)
        except:
            trace_err = StackTrace.get_stack_trace()
            msg = "Config (__create_namedtuple()) : %s%s" % ("\n", trace_err)
            raise Exception(msg)

    def __read_file(self, file_path):
        """
        :param file_path: absolute path of the file.
        :return: entity name and value as list inside config file.
        """
        try:
            val = []
            name = []

            with open(file_path, 'r') as f:

                for l in f:
                    l = l.strip()

                    if l != "\n" and l:

                        if l.startswith("#"):
                            continue

                        line = l.split("=")
                        left_side_val = line[0].strip().lower()
                        right_side_val = line[1].strip()
                        name.append(left_side_val)

                        if right_side_val.lower() == 'true':
                            val.append(True)
                        elif right_side_val.lower() == 'false':
                            val.append(False)
                        elif right_side_val.lstrip("+-").isdigit():
                            val.append(int(right_side_val))
                        elif (len(right_side_val.lower()) == 0) or (right_side_val.lower() == "n/a"):
                            val.append(None)
                        else:
                            if left_side_val.lower() in ["gcs_credential_directory_path", "local_upload_path",
                                                         "local_download_path", "local_log_path"]:
                                ResourceManager.create_dir(right_side_val)
                            val.append(right_side_val)
                f.close()
            return name, val
        except:
            trace_err = StackTrace.get_stack_trace()
            msg = "Config (__read_file()) : %s%s" % ("\n", trace_err)
            raise Exception(msg)

    def terminate(self):
        """
        :return: None
        # delete everything from self, so that using this object fails results
        # in an error as quickly as possible
        """

        try:
            for val in self.__dict__.keys():

                try:
                    delattr(self, val)
                except:
                    pass
        except Exception, e:
            pass

        collect()
        del garbage[:]

from src.ProcessType import ProcessType
from src.DLProcess import DLProcess

class ProcessFactory():
    """
    Factory class to obtain Process according to provided type
    """

    @staticmethod
    def get_process(params, process_type):
        """
        Obtains process given type
        :param: parameters for the process
        :param: type enum ProcessType
        """
        if process_type == ProcessType.ONLINE_DL.value:
            return DLProcess(params)
        else:
            error_msg = 'Process type not support. Only {} are accepted'.format(ProcessType)
            raise ValueError(error_msg)
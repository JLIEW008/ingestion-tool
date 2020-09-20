from src.sgx.SGXInfoGenerator import SGXInfoGenerator

class InfoGeneratorFactory():
    """
    Factory class to obtain InfoGenerator according to provided type
    """

    # Current implemented types
    SUPPORTED_TYPES = [
        'sgx'
    ]

    @staticmethod
    def get_info_generator(type):
        """
        Returns correct InfoGenerator class according to provided type
        """
        if type == 'sgx':
            return SGXInfoGenerator()
        else:
            err_msg = 'Factory does not recognise parsing type. ' \
                      + 'Only {} accepted'.format(InfoGeneratorFactory.SUPPORTED_TYPES)
            raise ValueError(err_msg)
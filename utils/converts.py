'''
This module is from samueva97.
Do not modify it
'''
import base64
import pyzstd



def bytes_to_base64(byte):
    '''
    Converts bytes in base64

    Parameters
    ----------
    byte : bytes
        Bytes

    Returns
    -------
    str
    '''
    return base64.b64encode(byte).decode()



def base64_to_bytes(text):
    '''
    Converts base64 to bytes

    Parameters
    ----------
    text : str
        Text in base64

    Returns
    -------
    bytes
    '''
    return base64.b64decode(text.encode())



def bytes_to_zstd(byte):
    '''
    Converts bytes to zstd

    Parameters
    ----------
    byte : bytes
        Bytes

    Returns
    -------
    bytes
    '''
    return pyzstd.compress(byte)



def zstd_to_bytes(byte):
    '''
    Converts zstd to bytes

    Parameters
    ----------
    byte : bytes
        Bytest representing a zst file

    Returns
    -------
    bytes
    '''
    # pylint: disable-next=no-member
    return pyzstd.decompress(byte)

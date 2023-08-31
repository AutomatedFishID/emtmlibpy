"""
Abstraction library for libEMTLib.so from SeaGIS.
Requires a licence to use, this is just a python wrapping function
"""
import ctypes
import dataclasses
import typing
from ctypes import Array, c_char
from enum import IntEnum, auto
from collections import namedtuple
from typing import Tuple

import pandas as pd
import numpy as np

EMTM_MAX_CHARS = 1024
libc = ctypes.CDLL('libEMTMLib.so')


class EMTMResult(IntEnum):
    """
    libStereoLibLX returns result codes.  This enumerates the codes.
    """
    ok = 0
    failed = auto()
    invalid_licence = auto()
    invalid_index = auto()
    buffer_too_small = auto()
    invalid_id = auto()


class TMQuadratData(ctypes.Structure):
    """
    Structure of TM quadrat data
    """
    _fields_ = [
        ('str_filename', ctypes.c_char * EMTM_MAX_CHARS),
        ('n_frame', ctypes.c_int),
        ('d_time_mins', ctypes.c_double),
        ('d_side_length', ctypes.c_double),
        ('str_units', ctypes.c_char * EMTM_MAX_CHARS),
        ('d_image_row_1', ctypes.c_double),
        ('d_image_row_2', ctypes.c_double),
        ('d_image_row_3', ctypes.c_double),
        ('d_image_row_4', ctypes.c_double),
        ('d_image_col_1', ctypes.c_double),
        ('d_image_col_2', ctypes.c_double),
        ('d_image_col_3', ctypes.c_double),
        ('d_image_col_4', ctypes.c_double)
    ]

    def __init__(self,
                 str_filename=b'',
                 n_frame=0,
                 d_time_mins=0,
                 d_side_length=0,
                 str_units=b'',
                 d_image_row_1=0,
                 d_image_row_2=0,
                 d_image_row_3=0,
                 d_image_row_4=0,
                 d_image_col_1=0,
                 d_image_col_2=0,
                 d_image_col_3=0,
                 d_image_col_4=0):
        super().__init__()
        self.str_filename = str_filename
        self.n_frame = n_frame
        self.d_time_mins = d_time_mins
        self.d_side_length = d_side_length
        self.str_units = str_units
        self.d_image_row_1 = d_image_row_1
        self.d_image_row_2 = d_image_row_2
        self.d_image_row_3 = d_image_row_3
        self.d_image_row_4 = d_image_row_4
        self.d_image_col_1 = d_image_col_1
        self.d_image_col_2 = d_image_col_2
        self.d_image_col_3 = d_image_col_3
        self.d_image_col_4 = d_image_col_4


class StringData(ctypes.Structure):
    """
    Generic structure for string data
    """
    _fields_ = [
        ('str1', ctypes.c_char * EMTM_MAX_CHARS),
        ('str2', ctypes.c_char * EMTM_MAX_CHARS),
        ('str3', ctypes.c_char * EMTM_MAX_CHARS),
        ('str4', ctypes.c_char * EMTM_MAX_CHARS),
        ('str5', ctypes.c_char * EMTM_MAX_CHARS),
        ('str6', ctypes.c_char * EMTM_MAX_CHARS)
    ]

    def __init__(self,
                 str1=b'',
                 str2=b'',
                 str3=b'',
                 str4=b'',
                 str5=b'',
                 str6=b''):
        super().__init__()
        self.str1 = str1
        self.str2 = str2
        self.str3 = str3
        self.str4 = str4
        self.str5 = str5
        self.str6 = str6


class EmPointData(ctypes.Structure):
    """
    Point structures used by libEMTLib.so from SeaGIS
    """
    _fields_ = [
        ('str_op_code', ctypes.c_char * EMTM_MAX_CHARS),
        ('str_filename', ctypes.c_char * EMTM_MAX_CHARS),
        ('n_frame', ctypes.c_int),
        ('d_time_mins', ctypes.c_double),
        ('str_period', ctypes.c_char * EMTM_MAX_CHARS),
        ('d_period_time_mins', ctypes.c_double),
        ('d_imx', ctypes.c_double),
        ('d_imy', ctypes.c_double),
        ('d_rectx', ctypes.c_double),
        ('d_recty', ctypes.c_double),
        ('str_family', ctypes.c_char * EMTM_MAX_CHARS),
        ('str_genus', ctypes.c_char * EMTM_MAX_CHARS),
        ('str_species', ctypes.c_char * EMTM_MAX_CHARS),
        ('str_code', ctypes.c_char * EMTM_MAX_CHARS),
        ('str_number', ctypes.c_char * EMTM_MAX_CHARS),
        ('str_stage', ctypes.c_char * EMTM_MAX_CHARS),
        ('str_activity', ctypes.c_char * EMTM_MAX_CHARS),
        ('str_comment', ctypes.c_char * EMTM_MAX_CHARS),
        ('str_att_9', ctypes.c_char * EMTM_MAX_CHARS),
        ('str_att_10', ctypes.c_char * EMTM_MAX_CHARS)
    ]

    def __init__(self, str_op_code=b'',
                 str_filename=b'',
                 n_frame=0,
                 d_time_mins=0.0,
                 str_period=b'',
                 d_period_time_mins=0.0,
                 d_imx=0.0, d_imy=0.0,
                 d_rectx=0.0, d_recty=0.0,
                 str_family=b'', str_genus=b'', str_species=b'',
                 str_code=b'',
                 str_number=b'',
                 str_stage=b'',
                 str_activity=b'',
                 str_comment=b'',
                 str_att_9=b'', str_att_10=b''):
        super().__init__()
        self.str_op_code = str_op_code
        self.str_filename = str_filename
        self.n_frame = n_frame
        self.d_time_mins = d_time_mins
        self.str_period = str_period
        self.d_period_time_mins = d_period_time_mins
        self.d_imx = d_imx
        self.d_imy = d_imy
        self.d_rectx = d_rectx
        self.d_recty = d_recty
        self.str_family = str_family
        self.str_genus = str_genus
        self.str_species = str_species
        self.str_code = str_code
        self.str_number = str_number
        self.str_stage = str_stage
        self.str_activity = str_activity
        self.str_comment = str_comment
        self.str_att_9 = str_att_9
        self.str_att_10 = str_att_10


class Em3DPpointData(ctypes.Structure):
    """
    3DPoint structures used by libEMTLib.so from SeaGIS
    """
    _fields_ = [
        ('str_op_code', ctypes.c_char * EMTM_MAX_CHARS),
        ('str_filename_left', ctypes.c_char * EMTM_MAX_CHARS),
        ('str_filename_right', ctypes.c_char * EMTM_MAX_CHARS),
        ('n_frame_left', ctypes.c_int),
        ('n_frame_right', ctypes.c_int),
        ('d_time_mins', ctypes.c_double),
        ('str_period', ctypes.c_char * EMTM_MAX_CHARS),
        ('d_period_time_mins', ctypes.c_double),
        ('d_imx_left', ctypes.c_double),
        ('d_imy_left', ctypes.c_double),
        ('d_imx_right', ctypes.c_double),
        ('d_imy_right', ctypes.c_double),
        ('dx', ctypes.c_double),
        ('dy', ctypes.c_double),
        ('dz', ctypes.c_double),
        ('dsx', ctypes.c_double),
        ('dsy', ctypes.c_double),
        ('dsz', ctypes.c_double),
        ('d_rms', ctypes.c_double),
        ('d_range', ctypes.c_double),
        ('d_direction', ctypes.c_double),
        ('str_family', ctypes.c_char * EMTM_MAX_CHARS),
        ('str_genus', ctypes.c_char * EMTM_MAX_CHARS),
        ('str_species', ctypes.c_char * EMTM_MAX_CHARS),
        ('str_code', ctypes.c_char * EMTM_MAX_CHARS),
        ('str_number', ctypes.c_char * EMTM_MAX_CHARS),
        ('str_stage', ctypes.c_char * EMTM_MAX_CHARS),
        ('str_activity', ctypes.c_char * EMTM_MAX_CHARS),
        ('str_comment', ctypes.c_char * EMTM_MAX_CHARS),
        ('str_att_9', ctypes.c_char * EMTM_MAX_CHARS),
        ('str_att_10', ctypes.c_char * EMTM_MAX_CHARS)
    ]

    def __init__(self, str_op_code=b'',
                 str_filename_left=b'', str_filename_right=b'',
                 n_frame_left=0, n_frame_right=0,
                 d_time_mins=0.0,
                 str_period=b'',
                 d_period_time_mins=0.0,
                 d_imx_left=0.0, d_imy_left=0.0, d_imx_right=0.0, d_imy_right=0.0,
                 dx=0.0, dy=0.0, dz=0.0,
                 dsx=0.0, dsy=0.0, dsz=0.0,
                 d_rms=0.0,
                 d_range=0.0,
                 d_direction=0.0,
                 str_family=b'', str_genus=b'', str_species=b'',
                 str_code=b'',
                 str_number=b'',
                 str_stage=b'',
                 str_activity=b'',
                 str_comment=b'',
                 str_att_9=b'', str_att_10=b''):
        super().__init__()
        self.str_op_code = str_op_code
        self.str_filename_left = str_filename_left
        self.str_filename_right = str_filename_right
        self.n_frame_left = n_frame_left
        self.n_frame_right = n_frame_right
        self.d_time_mins = d_time_mins
        self.str_period = str_period
        self.d_period_time_mins = d_period_time_mins
        self.d_imx_left = d_imx_left
        self.d_imy_left = d_imy_left
        self.d_imx_right = d_imx_right
        self.d_imy_right = d_imy_right
        self.dx = dx
        self.dy = dy
        self.dz = dz
        self.dsx = dsx
        self.dsy = dsy
        self.dsz = dsz
        self.d_rms = d_rms
        self.d_range = d_range
        self.d_direction = d_direction
        self.str_family = str_family
        self.str_genus = str_genus
        self.str_species = str_species
        self.str_code = str_code
        self.str_number = str_number
        self.str_stage = str_stage
        self.str_activity = str_activity
        self.str_comment = str_comment
        self.str_att_9 = str_att_9
        self.str_att_10 = str_att_10


class EmLengthData(ctypes.Structure):
    """
    Length structures used by libEMTLib.so from SeaGIS
    """
    _fields_ = [
        ('str_op_code', ctypes.c_char * EMTM_MAX_CHARS),
        ('str_filename_left', ctypes.c_char * EMTM_MAX_CHARS),
        ('str_filename_right', ctypes.c_char * EMTM_MAX_CHARS),
        ('n_frame_left', ctypes.c_int),
        ('n_frame_right', ctypes.c_int),
        ('d_time_mins', ctypes.c_double),
        ('str_period', ctypes.c_char * EMTM_MAX_CHARS),
        ('d_period_time_mins', ctypes.c_double),
        ('b_compound_length', ctypes.c_bool),
        ('d_imx1_left', ctypes.c_double),
        ('d_imy1_left', ctypes.c_double),
        ('d_imx1_right', ctypes.c_double),
        ('d_imy1_right', ctypes.c_double),
        ('d_imx2_left', ctypes.c_double),
        ('d_imy2_left', ctypes.c_double),
        ('d_imx2_right', ctypes.c_double),
        ('d_imy2_right', ctypes.c_double),
        ('d_length', ctypes.c_double),
        ('d_precision', ctypes.c_double),
        ('d_rms', ctypes.c_double),
        ('d_range', ctypes.c_double),
        ('d_direction', ctypes.c_double),
        ('dx_mid', ctypes.c_double),
        ('dy_mid', ctypes.c_double),
        ('dz_mid', ctypes.c_double),
        ('str_family', ctypes.c_char * EMTM_MAX_CHARS),
        ('str_genus', ctypes.c_char * EMTM_MAX_CHARS),
        ('str_species', ctypes.c_char * EMTM_MAX_CHARS),
        ('str_code', ctypes.c_char * EMTM_MAX_CHARS),
        ('str_number', ctypes.c_char * EMTM_MAX_CHARS),
        ('str_stage', ctypes.c_char * EMTM_MAX_CHARS),
        ('str_activity', ctypes.c_char * EMTM_MAX_CHARS),
        ('str_comment', ctypes.c_char * EMTM_MAX_CHARS),
        ('str_att_9', ctypes.c_char * EMTM_MAX_CHARS),
        ('str_att_10', ctypes.c_char * EMTM_MAX_CHARS)
    ]

    def __init__(self, str_op_code=b'',
                 str_filename_left=b'', str_filename_right=b'',
                 n_frame_left=0, n_frame_right=0,
                 d_time_mins=0.0,
                 str_period=b'',
                 d_period_time_mins=0.0,
                 b_compound_length=0.0,
                 d_imx1_left=0.0, d_imy1_left=0.0, d_imx1_right=0.0, d_imy1_right=0.0,
                 d_imx2_left=0.0, d_imy2_left=0.0, d_imx2_right=0.0, d_imy2_right=0.0,
                 d_length=0.0,
                 d_precision=0.0,
                 d_rms=0.0,
                 d_range=0.0,
                 d_direction=0.0,
                 dx_mid=0.0, dy_mid=0.0, dz_mid=0.0,
                 str_family=b'', str_genus=b'', str_species=b'',
                 str_code=b'',
                 str_number=b'',
                 str_stage=b'',
                 str_activity=b'',
                 str_comment=b'',
                 str_att_9=b'', str_att_10=b''):
        super().__init__()
        self.str_op_code = str_op_code
        self.str_filename_left = str_filename_left
        self.str_filename_right = str_filename_right
        self.n_frame_left = n_frame_left
        self.n_frame_right = n_frame_right
        self.d_time_mins = d_time_mins
        self.str_period = str_period
        self.d_period_time_mins = d_period_time_mins
        self.b_compound_length = b_compound_length
        self.d_imx1_left = d_imx1_left
        self.d_imy1_left = d_imy1_left
        self.d_imx1_right = d_imx1_right
        self.d_imy1_right = d_imy1_right
        self.d_imx2_left = d_imx2_left
        self.d_imy2_left = d_imy2_left
        self.d_imx2_right = d_imx2_right
        self.d_imy2_right = d_imy2_right
        self.d_length = d_length
        self.d_precision = d_precision
        self.d_rms = d_rms
        self.d_range = d_range
        self.d_direction = d_direction
        self.dx_mid = dx_mid
        self.dy_mid = dy_mid
        self.dz_mid = dz_mid
        self.str_family = str_family
        self.str_genus = str_genus
        self.str_species = str_species
        self.str_code = str_code
        self.str_number = str_number
        self.str_stage = str_stage
        self.str_activity = str_activity
        self.str_comment = str_comment
        self.str_att_9 = str_att_9
        self.str_att_10 = str_att_10


class TmPointData(ctypes.Structure):
    """
    Point structures used by libEMTLib.so from SeaGIS
    """
    _fields_ = [
        ('str_filename', ctypes.c_char * EMTM_MAX_CHARS),
        ('n_frame', ctypes.c_int),
        ('d_time_mins', ctypes.c_double),
        ('d_image_row', ctypes.c_double),
        ('d_image_col', ctypes.c_double),
        ('str_att_1', ctypes.c_char * EMTM_MAX_CHARS),
        ('str_att_2', ctypes.c_char * EMTM_MAX_CHARS),
        ('str_att_3', ctypes.c_char * EMTM_MAX_CHARS),
        ('str_att_4', ctypes.c_char * EMTM_MAX_CHARS),
        ('str_att_5', ctypes.c_char * EMTM_MAX_CHARS),
        ('str_att_6', ctypes.c_char * EMTM_MAX_CHARS),
        ('str_att_7', ctypes.c_char * EMTM_MAX_CHARS),
        ('str_att_8', ctypes.c_char * EMTM_MAX_CHARS)
    ]

    def __init__(self,
                 str_filename=b'',
                 n_frame=0,
                 d_time_mins=0.0,
                 d_image_row=0.0,
                 d_image_col=0.0,
                 str_att_1=b'', str_att_2=b'', str_att_3=b'', str_att_4=b'', str_att_5=b'', str_att_6=b'',
                 str_att_7=b'',
                 str_att_8=b''):
        super().__init__()
        self.str_filename = str_filename
        self.n_frame = n_frame
        self.d_time_mins = d_time_mins
        self.d_image_row = d_image_row
        self.d_image_col = d_image_col
        self.str_att_1 = str_att_1
        self.str_att_2 = str_att_2
        self.str_att_3 = str_att_3
        self.str_att_4 = str_att_4
        self.str_att_5 = str_att_5
        self.str_att_6 = str_att_6
        self.str_att_7 = str_att_7
        self.str_att_8 = str_att_8


def emtm_version() -> tuple[int, int]:
    """
    Return the version number of libStereoLibLX
    :return: (major, minor)
    """

    minor = ctypes.c_int(0)
    major = ctypes.c_int(0)

    libc.EMTMVersion(ctypes.byref(major), ctypes.byref(minor))

    return major.value, minor.value


def emtm_licence_present() -> bool:
    """
    Checks to see if there is a valid licence present
    :return:
    """
    r = libc.EMTMLicencePresent()

    return True if r == 1 else False


def em_load_data(em_file_id: int, filename: str) -> EMTMResult:
    """
    The EventMeasure data file (.EMObs) to load

    Use this function to load an EventMeasure data file.
    The EventMeasure data loaded with this function remains persistent
    within the library until a subsequent call to this function is made, or the
    data is specifically cleared by calling `EMClearData`.

    Essentially all remaining functions that deal with EventMeasure data rely
    on this function to load the actual data.

    You do not need to call `EMClearData` before calling this function.

    :param filename:
    :return: EMTMResult
    """
    r = libc.EMLoadData(em_file_id, bytes(filename, 'UTF-8'))
    return r


def em_remove_all() -> None:
    """
    Use this function to clear data loaded with EMLoadData. The only reason to
    use this function is to specifically release resources used to store the
    current EventMeasure data. Those resources are automatically released
    when the library goes out of scope, or EMLoadData is used to load other
    EventMeasure data.

    :return: None
    """
    libc.EMRemoveAll()


def em_info_count() -> int:
    """
    Use this function to find the number of information fields in EventMeasure
    data
    :return: The count of the iformation fields
    """
    return libc.EMInfoCount()


def em_info_get(n_id: int, n_index: int, n_buff_sz=EMTM_MAX_CHARS) -> tuple[Array[c_char], Array[c_char]]:
    """
    Before using this function you should call EMInfoCount to confirm the
    number of information fields – this provides the upper bound for this
    function’s nIndex parameter.

    The caller is responsible for allocating and deleting the buffers associated
    with the strings pStrHeader, pStrData; and ensuring the buffers are at
    least nBuffSz characters in size.

    If the function returns buffer_too_small, the strings pStrHeader,
    pStrData will be filled to their respective specified capacity (nBuffSz),
    then the string data is truncated to avoid overflow.

    Note that the following indices (nIndex) have fixed headers (pStrHeader)
    as such:

    +---------------------+---------------------+
    |     Index (nIndex)  | Header (pStrHeader) |
    +---------------------+---------------------+
    |     0               | OpCode              |
    |     1               | TapeReader          |
    |     2               | Depth               |
    |     3               | Comment             |
    +---------------------+---------------------+

    The remaining headers (headers for higher information field indices) are
    user configurable.
    To find the OpCode of EventMeasure data, use this function with nIndex = 0.

    """

    p_str_header = ctypes.create_string_buffer(n_buff_sz)
    p_str_data = ctypes.create_string_buffer(n_buff_sz)

    r = libc.EMInfoGet(n_id, n_index, p_str_header, p_str_data, n_buff_sz)

    return p_str_header.value.decode(), p_str_data.value.decode()


def em_info_set(n_id: int, n_index: int, p_str_header: str, p_str_data: str,  n_buff_sz=EMTM_MAX_CHARS) -> EMTMResult:
    """
    Before using this function you should call EMInfoCount to confirm the
    number of information fields – this provides the upper bound for this
    function’s nIndex parameter.
    Use this function to set the information field header (pStrHeader) and
    data (pStrData) for the information field specified by nIndex.
    Note that the following indices (nIndex) have fixed headers (pStrHeader)
    as such:
    +---------------------+---------------------+
    |     Index (nIndex)  | Header (pStrHeader) |
    +---------------------+---------------------+
    |     0               | OpCode              |
    |     1               | TapeReader          |
    |     2               | Depth               |
    |     3               | Comment             |
    +---------------------+---------------------+

    The pStrHeader parameter is ignored for nIndex values [0..3] and the
    library forces the header values in the above table. Remaining headers
    (headers for higher information field indices) are user configurable.

    To set the OpCode of EventMeasure data, use this function with nIndex =
    0 (noting the value of pStrHeader is ignored, the value of pStrData sets
    the OpCode data).
    """

    p_str_header = bytes(p_str_header, 'UTF-8')
    p_str_data = bytes(p_str_data, 'UTF-8')

    r = libc.EMInfoSet(n_id, n_index, p_str_header, p_str_data, n_buff_sz)
    return r




def em_units(em_file_id: int, n_buff_sz: int = EMTM_MAX_CHARS) -> str:
    """
    Use this function to get the 3D measurement units for the currently loaded
    EventMeasure data. The EventMeasure data is loaded using EMLoadData

    :param p_str_units: Address of the buffer to receive the units string. The caller is
    responsible for allocating enough space for at least nBuffSz
    characters in this buffer.
    :param n_buff_sz: The size of the buffer (pStrUnits).
    :return: Will return buffer_too_small if the units string will not fit in the
    supplied buffer, ok for success.
    """

    p_str_units = ctypes.create_string_buffer(n_buff_sz)

    libc.EMUnits(em_file_id, ctypes.byref(p_str_units))

    return p_str_units.value.decode()


def em_unique_fgs(em_file_id: int) -> int:
    """
    Use this function to find the number of unique family, genus, species
    combinations present in all measurements in the currently loaded
    EventMeasure data. All measurement types are considered (points,
    bounding boxes, 3D points and lengths).

    EventMeasure data is loaded using EMLoadData.
    This function must be called before calling EMGetUniqueFGS for two
    reasons:

    • Calling EMUniqueFGS generates a list of unique family, genus, species
    values for the currently loaded EventMeasure data. The library stores
    this list until a new EventMeasure data file is loaded (EMLoadData) or
    the current EventMeasure data is specifically cleared (EMClearData).

    • EMUniqueFGS returns the number of family, genus, species names
    that can be queried using EMGetUniqueFGS.

    It is sufficient to call this function (EMUniqueFGS) once before making
    multiple calls to EMGetUniqueFGS.

    :return:
    """
    return libc.EMUniqueFGS(em_file_id)


def em_get_unique_fgs(em_file_id: int, n_index: int) -> tuple:
    """
    Before using this function:

    • There must be EventMeasure data loaded using EMLoadData.

    • You must call EMUniqueFGS to discover the number of unique family,
    genus, species combinations – this provides the upper bound for this
    function’s nIndex parameter.

    The returned family, genus, species strings will always be lower case,
    regardless of how they were originally stored in the EventMeasure data.
    It is possible (valid) for this function to return empty strings (“”) for the
    family, genus, species. An EventMeasure user may only annotate to the
    family level (so the genus and species are empty), or a user may not
    annotate the family, genus, species at all (for example an annotation or
    measurement that just has a comment attribute).

    The caller is responsible for allocating and deleting the buffers associated
    with the strings pStrFamily, pStrGenus, pStrSpecies; and ensuring the
    buffers are at least nBuffSz characters in size.

    Family, genus, species has some sample test data.
    :return: 
    """

    n_index = ctypes.c_int(n_index)

    p_str_family = ctypes.create_string_buffer(EMTM_MAX_CHARS)
    p_str_genus = ctypes.create_string_buffer(EMTM_MAX_CHARS)
    p_str_species = ctypes.create_string_buffer(EMTM_MAX_CHARS)

    success = libc.EMGetUniqueFGS(em_file_id, n_index,
                                  ctypes.byref(p_str_family), ctypes.byref(p_str_genus), ctypes.byref(p_str_species),
                                  EMTM_MAX_CHARS)

    return p_str_family.value.decode(), p_str_genus.value.decode(), p_str_species.value.decode()


def em_measurement_count_fgs(em_file_id: int, family: str, genus: str, species: str) -> tuple:
    """
    Use this function to query the number of measurements present in the
    currently loaded EventMeasure data, for a specified family/genus/species.
    The EventMeasure data is loaded using EMLoadData.

    The pStrFamily, pStrGenus, pStrSpecies arguments are used to
    query the measurement count for a specific family/genus/species.

    Specification of the family/genus/species is case insensitive.

    A wildcard “*” can be used to ignore a family/genus/species argument. For
    example, to count measurements for species ghi for any family and genus

    the first three arguments of the function call are:
    EMMeasurementCountFGS(“*”, “*”, “ghi”, ...);

    The family/genus/species arguments are case insensitive, so the following

    gives an identical result:
    EMMeasurementCountFGS(“*”, “*”, “GHI”, ...);

    To count measurements for family abc, genus def, species ghi the first

    three arguments of the function call are:
    EMMeasurementCountFGS(“abc”, “def”, “ghi”, ...);

    :param family: The family to use when counting measurements, see examples
    below.
    :param genus: The genus to use when counting measurements.
    :param species: The species to use when counting measurements.
    :return: (n_point, n_box, n_3D_point, n_length, n_cpd_length)
    """

    n_point = ctypes.c_int(0)
    n_box = ctypes.c_int(0)
    n_3D_point = ctypes.c_int(0)
    n_length = ctypes.c_int(0)
    n_cpd_length = ctypes.c_int(0)

    libc.EMMeasurementCountFGS(em_file_id,
                               bytes(family, 'UTF-8'),
                               bytes(genus, 'UTF-8'),
                               bytes(species, 'UTF-8'),
                               ctypes.byref(n_point),
                               ctypes.byref(n_box),
                               ctypes.byref(n_3D_point),
                               ctypes.byref(n_length),
                               ctypes.byref(n_cpd_length))

    FGS = namedtuple('FGS', 'point box xyz_point, length cpd_length')
    fgs = FGS(n_point.value, n_box.value, n_3D_point.value, n_length.value, n_cpd_length.value)

    return fgs


def em_point_count(em_file_id: int) -> tuple:
    """
    Use this function to find the number of point measurements (including
    bounding boxes) in the currently loaded EventMeasure data.
    EventMeasure data is loaded using EMLoadData.

    This function must be called before calling EMGetPoint for two reasons:

    • Calling this function generates an indexed mapping of all point
    measurements in the currently loaded EventMeasure data. The
    library stores this mapping internally until a new EventMeasure data
    file is loaded (EMLoadData) or the current EventMeasure data is
    specifically cleared (EMClearData).

    • The return value of this function is the upper bound of the indices
    allowed by EMGetPoint.

    It is sufficient to call this function once before making multiple calls to
    EMGetPoint.
    :return:
    """

    pn_bbox = ctypes.c_int(0)
    r = libc.EMPointCount(em_file_id, ctypes.byref(pn_bbox))

    PointCount = namedtuple('PointCount', 'total bbox')
    point_count = PointCount(r, pn_bbox.value)

    return point_count


def em_get_point(em_file_id: int, n_index: int) -> EmPointData:
    """
    Use this function to get point measurement data (including bounding box
    data) for a measurement in the currently loaded EventMeasure data.
    Before using this function:

    • There must be EventMeasure data loaded using EMLoadData.
    • You must call EMPointCount to discover the upper bound for this
    function’s nIndex parameter.

    If the function returns buffer_too_small, the string buffers in the
    EMPointData structure will be filled to their allowed capacity, then the
    string data is truncated to avoid overflow
    :param n_index:
    :return:
    """

    p = EmPointData()

    r = libc.EMGetPoint(em_file_id, n_index, ctypes.byref(p))

    return p


def em_3d_point_count(em_file_id: int) -> int:
    """
    Use this function to find the number of 3D point measurements in the
    currently loaded EventMeasure data.
    EventMeasure data is loaded using EMLoadData.

    This function must be called before calling EMGet3DPoint for two reasons:

    • Calling this function generates an indexed mapping of all 3D point
    measurements in the currently loaded EventMeasure data. The
    library stores this mapping internally until a new EventMeasure data
    file is loaded (EMLoadData) or the current EventMeasure data is
    specifically cleared (EMClearData).

    • The return value of this function is the upper bound of the indices
    allowed by EMGet3DPoint.

    It is sufficient to call this function once before making multiple calls to
    EMGet3DPoint

    :return: number of 3D points
    """

    r = libc.EM3DPointCount(em_file_id)
    return r


def em_get_3d_point(em_file_id: int, n_index: int) -> Em3DPpointData:
    """
    Use this function to get 3D point measurement data for a measurement in
    the currently loaded EventMeasure data.

    Before using this function:
    • There must be EventMeasure data loaded using EMLoadData.
    • You must call EM3DPointCount to discover the upper bound for this
    function’s nIndex parameter.

    If the function returns buffer_too_small, the string buffers in the
    EM3DPointData structure will be filled to their allowed capacity, then the
    string data is truncated to avoid overflow.
    :param n_index:
    :return:
    """

    xyz_point = Em3DPpointData()

    r = libc.EMGet3DPoint(em_file_id, n_index, ctypes.byref(xyz_point))

    return xyz_point


def em_get_length_count(em_file_id: int) -> tuple:
    """
    Use this function to find the number of length measurements (including
    compound lengths) in the currently loaded EventMeasure data.
    EventMeasure data is loaded using EMLoadData.

    This function must be called before calling EMGetLength for two reasons:
    • Calling this function generates an indexed mapping of all length
    measurements in the currently loaded EventMeasure data. The
    library stores this mapping internally until a new EventMeasure data
    file is loaded (EMLoadData) or the current EventMeasure data is
    specifically cleared (EMClearData).

    • The return value of this function is the upper bound of the indices
    allowed by EMGetLength.

    It is sufficient to call this function once before making multiple calls to
    EMGetLength.
    :return: The count of length measurements. This includes any compound
    length measurements (that is, the return value is the total number of
    length and compound length measurements). Use pnCompound to
    find the number of compound lengths
    """

    pn_compound = ctypes.c_int(0)

    r = libc.EMLengthCount(em_file_id, pn_compound)

    LengthCount = namedtuple('LengthCount', 'total compound')
    length_count = LengthCount(r, pn_compound.value)

    return length_count


def em_get_length(em_file_id: int, n_index: int) -> EmLengthData:
    """
    Use this function to get length measurement data (including compound
    length data) for a measurement in the currently loaded EventMeasure
    data.
    Before using this function:
    • There must be EventMeasure data loaded using EMLoadData.
    • You must call EMLengthCount to discover the upper bound for this
    function’s nIndex parameter.
    If the function returns buffer_too_small, the string buffers in the
    EMLengthData structure will be filled to their allowed capacity, then the
    string data is truncated to avoid overflow.

    :param n_index: The 0-based index of the required measurement. This value must be
    ≥ 0, and < the value returned by EMLengthCount.
    :return:
    """

    length_data = EmLengthData()

    r = libc.EMGetLength(em_file_id, n_index, ctypes.byref(length_data))

    return length_data


def tm_load_data(tm_file_id: int, filename: str) -> EMTMResult:
    """
    Use this function to load a TransectMeasure data file.
    The TransectMeasure data loaded with this function remains persistent
    within the library until a subsequent call to this function is made, or the
    data is specifically cleared by calling TMClearData.

    Essentially all remaining functions that deal with TransectMeasure data
    rely on this function to load the actual data.

    You do not need to call TMClearData before calling this function.

    :param filename: The TransectMeasure data file (.TMObs) to load.
    :return: Will return invalid_licence if the licence is invalid, failed if the
    TransectMeasure data file (pStrFileName) cannot be read, ok if the
    TransectMeasure data file was read successfully.

    """

    r = libc.TMLoadData(tm_file_id, bytes(filename, 'UTF-8'))
    return EMTMResult(r)


def tm_remove_all() -> None:
    """
    Use this function to clear data loaded with TMLoadData . The only reason to
    use this function is to specifically release resources used to store the
    current TransectMeasure data. Those resources are automatically released
    when the library goes out of scope, or TMLoadData is used to load other
    TransectMeasure data.

    :return:
    """

    libc.TMRemoveAll()


def tm_point_count(tm_file_id: int) -> int:
    """
    Use this function to find the number of point measurements in the
    currently loaded TransectMeasure data.
    TransectMeasure data is loaded using TMLoadData.
    This function must be called before calling TMGetPoint for two reasons:

    • Calling this function generates an indexed mapping of all point
    measurements in the currently loaded TransectMeasure data. The
    library stores this mapping internally until a new TransectMeasure
    data file is loaded (TMLoadData) or the current TransectMeasure
    data is specifically cleared (TMClearData).

    • The return value of this function is the upper bound of the indices
    allowed by TMGetPoint.

    It is sufficient to call this function once before making multiple calls to
    TMGetPoint.

    :return: The count of point measurements.
    """

    return libc.TMPointCount(tm_file_id)


def tm_get_point(tm_file_id: int, n_index) -> TmPointData:
    """
    Use this function to get point measurement data for a measurement in the
    currently loaded TransectMeasure data.
    Before using this function:
    • There must be TransectMeasure data loaded using TMLoadData.
    • You must call TMPointCount to discover the upper bound for this
    function’s nIndex parameter.
    If the function returns buffer_too_small , the string buffers in the
    TMPointData structure will be filled to their allowed capacity, then the
    string data is truncated to avoid overflow.


    :param n_index:
    :return:
    """
    p = TmPointData()

    r = libc.TMGetPoint(tm_file_id, n_index, ctypes.byref(p))

    return p


def tm_get_frame_info_names(tm_file_id: int) -> str:
    """
    Use this function to get the frame information names for the currently
    loaded TransectMeasure data.
    Before using this function:
    • There must be TransectMeasure data loaded using TMLoadData.
    If the function returns buffer_too_small, the string buffers in the
    StringData structure will be filled to their allowed capacity, then the
    string data is truncated to avoid overflow

    :return: The metadata about the frame information
    """
    # string_data = ctypes.create_string_buffer(EMTM_MAX_CHARS)
    string_data = StringData()
    r = libc.TMGetFrameInfoNames(tm_file_id, ctypes.byref(string_data))

    return string_data


def tm_get_frame_info(tm_file_id: int, n_frame) -> str:
    """
    Use this function to get the frame information names for the currently
    loaded TransectMeasure data.
    Before using this function:
    • There must be TransectMeasure data loaded using TMLoadData.
    If the function returns buffer_too_small, the string buffers in the
    StringData structure will be filled to their allowed capacity, then the
    string data is truncated to avoid overflow

    param n_index: The frame number
    :return: information about the frame
    """
    n_frame = ctypes.c_int(n_frame)

    string_data = StringData()
    r = libc.TMGetFrameInfo(tm_file_id, n_frame, ctypes.byref(string_data))

    return string_data


def tm_quadrat_count(tm_file_id: int) -> int:
    """
    Use this function to find the number of quadrat definitions in the currently
    loaded TransectMeasure data.
    TransectMeasure data is loaded using TMLoadData.
    This function must be called before calling TMGetQuadrat for two reasons:
    • Calling this function generates an indexed mapping of all quadrats in
    the currently loaded TransectMeasure data. The library stores this
    mapping internally until a new TransectMeasure data file is loaded
    (TMLoadData) or the current TransectMeasure data is specifically
    cleared (TMClearData).
    • The return value of this function is the upper bound of the indices
    allowed by TMGetQuadrat.
    It is sufficient to call this function once before making multiple calls to
    TMGetQuadrat

    :return:
    """
    quad_count = ctypes.c_int()
    quad_count: object = libc.TMQuadratCount(tm_file_id)
    return quad_count


def tm_get_quadrat(tm_file_id: int, n_index: int) -> TMQuadratData:
    """
    Use this function to get quadrat data for a quadrat in the currently loaded
    TransectMeasure data.
    Before using this function:
    • There must be TransectMeasure data loaded using TMLoadData.
    • You must call TMQuadratCount to discover the upper bound for this
    function’s nIndex parameter.
    If the function returns buffer_too_small, the string buffers in the
    TMQuadratData structure will be filled to their allowed capacity, then the
    string data is truncated to avoid overflow.
    Note that TransectMeasure only allows one quadrat to be defined in any
    given image, so there can be a maximum of one quadrat for any given
    image filename and frame number
    :param n_index:
    :return: The location of the quadrat in pixel coords
    """
    n_index = ctypes.c_int(n_index)
    tm_quadrat_data = TMQuadratData()

    libc.TMGetQuadrat(tm_file_id, tm_quadrat_data, n_index, ctypes.byref(tm_quadrat_data))

    return tm_quadrat_data


def _dataframe_from_count_and_record_reader(count: int, record_read_function: typing.Callable[
    [int], ctypes.Structure]) -> pd.DataFrame:
    """
    A generic helper for generating a Pandas DataFrame from a given count and
    callable, returning a ctypes.Strucutre, representing a data record, given
    the index of the record (e.g. `em_get_length`).

    :param count: The number of records to read. Must be > 0 to get a valid DataFrame.
    :param record_read_function: Function returning records as ctypes.Structure, given an index.
    :return: The Pandas DataFrame
    """

    if count == 0:
        return None
    if count < 0:
        raise ValueError(f"Count must be greater than zero. Got {count}.")

    dtype_template = 'object'
    p = record_read_function(0)

    index = [attr for attr in dir(p) if (not attr.startswith('__') and not attr.startswith('_'))]
    data = np.empty(shape=[count, len(index)], dtype=dtype_template)  # change these

    for jj in range(count):
        p = record_read_function(jj)
        for ii, ind in enumerate(index):
            tmp = p.__getattribute__(ind)
            data[jj][ii] = tmp

    xpdf = pd.DataFrame(data=data, columns=index)
    xpdf = xpdf.convert_dtypes().infer_objects()
    return xpdf


# def em_to_dataframe(em_file_id: int, em_data_type='length') -> pd.DataFrame:
#     """
#     A convenience method for returning a data frame instead of ctypes object.
#
#     :param em_data_type: Either length or point
#     :return: pandas dataframe
#     """
#     if 'length' in em_data_type:
#         count = em_get_length_count(em_file_id).total
#         record_read_function = em_get_length
#     elif 'point' in em_data_type:
#         count = em_point_count(em_file_id).total
#         record_read_function = em_get_point
#     elif 'point3d' in em_data_type:
#         count = em_3d_point_count(em_file_id)
#         record_read_function = em_get_3d_point
#     else:
#         raise RuntimeError(f"Unsupported em_data_type `{em_data_type}`.")
#
#     return _dataframe_from_count_and_record_reader(count, record_read_function)


# @dataclasses.dataclass
# class EmAnnotationDataFrames:
#     """
#     Helper class to represent the Pandas DataFrames which can be read from the an EMObs file and associate them with
#     the relevant loading logic.
#
#     By default, all three possible tables are read automatically, when instantiating this class. To avoid this
#     behaviour for any of the tables, pass an explicit None for that table to the constructor.
#
#     The contained static methods can be used to load only specific tables.
#     """
#
#     @staticmethod
#     def load_points_from_current_em_file(em_file_id: int):
#         return _dataframe_from_count_and_record_reader(em_point_count(em_file_id).total, em_get_point(em_file_id))
#
#     @staticmethod
#     def load_3d_points_from_current_em_file(em_file_id: int):
#         return _dataframe_from_count_and_record_reader(em_3d_point_count(em_file_id), em_get_3d_point(em_file_id))
#
#     @staticmethod
#     def load_lengths_from_current_em_file(em_file_id: int):
#         return _dataframe_from_count_and_record_reader(em_get_length_count(em_file_id).total, em_get_length(em_file_id))
#
#     points: pd.DataFrame = dataclasses.field(default_factory=load_points_from_current_em_file.__get__(object))
#     points3d: pd.DataFrame = dataclasses.field(default_factory=load_3d_points_from_current_em_file.__get__(object))
#     lengths: pd.DataFrame = dataclasses.field(default_factory=load_lengths_from_current_em_file.__get__(object))


def emtm_set_licence_keys(key1: str, key2: str) -> bool:
    """
    Use this function to enable the library using licence keys. Functions such as
    EMLoadData, TMLoadData, EMWriteData will not work without a verified
    licence.

    :param key1: License key 1
    :param key2: License key 2
    :return: True if licence keys were valid and the library has been enabled, False otherwise.
    """
    return libc.EMTMSetLicenceKeys(bytes(key1, 'UTF-8'), bytes(key2, 'UTF-8'))


def em_create(em_file_id: int) -> None:
    """
    Creates an empty EventMeasure data file at ID nID.
    If this ID already exists, any data associated with the ID is cleared.
    """
    libc.EMCreate(em_file_id)


def em_add_point(em_file_id: int, data: EmPointData) -> EMTMResult:
    """
    Use this function to add a point measurement (including a bounding box).
    Point data should only be added to an image considered to be the left
    image where a stereo configuration is being used.

    Data can be added to an existing EventMeasure data file by first loading
    the data file (em_load_data) then adding measurements with em_add_point,
    em_add_3d_point, em_add_length.

    To create a new EventMeasure data file, first call em_clear_data to clear
    any EventMeasure data held by the library, then add measurement data using
    em_add_point, em_3d_add_point, em_add_length.

    When finished adding data, the data can be saved using em_write_data.

    :param data: An EMPointData structure that describes the measurement data
        to be added.

    :return: Will be EMTMResult. ok for success. Otherwise EMTMResult. failed
        if data.strOpCode is not the same as already existing measurements,
        data.strOpCode is “”, data.strFilename is “”, data.nFrame is < 0, or if
        any of the imagecoordinates in the data structure are < 0.
    """
    return libc.EMAddPoint(em_file_id, data)


def em_add_3d_point(em_file_id: int, data: Em3DPpointData):
    """
    Use this function to add a 3D point measurement.

    Data can be added to an existing EventMeasure data file by first loading
    the data file (em_load_data) then adding measurements with em_add_point,
    em_add_3d_point, em_add_length.

    To create a new EventMeasure data file, first call em_clear_data to clear
    any EventMeasure data held by the library, then add measurement data using
    em_add_point, em_3d_add_point, em_add_length.

    When finished adding data, the data can be saved using em_write_data.

    :param data: An EM3DPointData structure that describes the measurement data
        to be added.

    :return: Will be EMTMResult.ok for success. Otherwise EMTMResult.failed if
        data.strOpCode is not the same as already existing measurements,
        data.strOpCode is “”, data.strFilenameLeft or data.strFilenameRight are “”,
        data.nFrameLeft or data.nFrameRight are < 0, or if any of the image
        coordinates in the data structure are less than 0.
    """
    return libc.EMAdd3DPoint(em_file_id, data)


def em_add_length(em_file_id: int, data: EmLengthData) -> EMTMResult:
    """
    Use this function to add a length measurement.

    Data can be added to an existing EventMeasure data file by first loading
    the data file (em_load_data) then adding measurements with em_add_point,
    em_add_3d_point, em_add_length.

    To create a new EventMeasure data file, first call em_clear_data to clear
    any EventMeasure data held by the library, then add measurement data using
    em_add_point, em_3d_add_point, em_add_length.

    When finished adding data, the data can be saved using em_write_data.

    :param data: An EMLengthData structure that describes the measurement data to
        be added.

    :return: Will be EMTMResult.ok for success. Otherwise EMTMResult.failed if
        data.strOpCode is not the same as already existing measurements,
        data.strOpCode is “”, data.strFilenameLeft or data.strFilenameRight are “”,
        data.nFrameLeft or data.nFrameRight are < 0, data.bCompound is true, or if
        any of the image coordinates in the data structure are less than 0.
    """
    return libc.EMAddLength(em_file_id, data)


def em_write_data(em_file_id: int, filename: str):
    """
    Use this function to save the EventMeasure data currently held in the
    library.

    The current EventMeasure data persists in the library after using this
    function.

    If the file already exists, it will be overwritten.

    :param filename: The name of the EventMeasure data file to create. Typically with
        ".EMObs" extension.

    :return: Will return EMTMResult.ok for success. Otherwise EMTMResult.invalid_licence
        if the licence is invalid, or failed if the EventMeasure data file cannot be written.
    """

    return libc.EMWriteData(em_file_id, bytes(filename, 'UTF-8'))

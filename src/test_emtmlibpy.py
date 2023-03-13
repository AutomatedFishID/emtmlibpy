import unittest
import os
import tempfile
import emtmlibpy.emtmlibpy as emtm
from emtmlibpy.emtmlibpy import EMTMResult
from collections import namedtuple
from pathlib import Path

SRC_DIR = os.path.abspath(os.path.dirname(__file__))
TEST_FILES_PATH = os.path.join(SRC_DIR, 'test_files')

assert os.path.exists(TEST_FILES_PATH), f"Please ensure you place the required test files at: {TEST_FILES_PATH}"

assert "EMTM_KEY1" in os.environ, "Must set the EMTM_KEY1 environment variable to a valid licence key"
assert "EMTM_KEY2" in os.environ, "Must set the EMTM_KEY2 environment variable to a valid licence key"

class TestEmtmlibpy(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        key1 = os.environ["EMTM_KEY1"]
        key2 = os.environ["EMTM_KEY2"]
        success = emtm.emtm_set_licence_keys(key1, key2)
        assert success, "Error setting EMTMlib licence keys"

    def setUp(self):
        emtm.em_load_data(os.path.join(TEST_FILES_PATH, 'Test.EMObs'))


    def tearDown(self) -> None:
        emtm.em_clear_data()


    def test_emtm_version(self):
        r = emtm.emtm_version()
        self.assertTupleEqual(r, (2, 1))

    def test_emtm_licence_present(self):
        r = emtm.emtm_licence_present()
        self.assertTrue(r)

    def test_em_load_data(self):
        r = emtm.em_load_data(os.path.join(TEST_FILES_PATH, 'Test.EMObs'))
        self.assertIs(EMTMResult(r), EMTMResult(0))

    def test_em_clear_data(self):
        r = emtm.em_load_data(os.path.join(TEST_FILES_PATH, 'Test.EMObs'))
        self.assertIs(EMTMResult(r), EMTMResult(0))

        emtm.em_clear_data()

    def test_em_op_code(self):
        r = emtm.em_load_data(os.path.join(TEST_FILES_PATH, 'Test.EMObs'))
        self.assertIs(EMTMResult(r), EMTMResult(0))

        r = emtm.em_op_code()
        self.assertEqual(r, 'Test')

    def test_em_units(self):
        r = emtm.em_units()
        self.assertEqual(r, 'mm')

    def test_em_unique_fgs(self):
        r = emtm.em_unique_fgs()
        self.assertEqual(r, 6)

    def test_get_unique_fgs(self):
        r = emtm.em_load_data(os.path.join(TEST_FILES_PATH, 'Test.EMObs'))

        fgs = [('', '', ''),
               ('balistidae', 'abalistes', 'stellatus'),
               ('nemipteridae', 'nemipterus', 'furcosus'),
               ('nemipteridae', 'pentapodus', 'porosus'),
               ('pinguipedidae', 'parapercis', 'xanthozona'),
               ('scombridae', 'scomberomorus', 'queenslandicus')]

        n_unique = emtm.em_unique_fgs()

        for ii in range(n_unique):
            r = emtm.em_get_unique_fgs(ii)
            self.assertTupleEqual(r, fgs[ii])

    def test_em_measurement_count_fgs(self):
        FGS = namedtuple('FGS', 'point box xyz_point, length cpd_length')

        r = emtm.em_measurement_count_fgs('balistidae', 'abalistes', 'stellatus')
        self.assertTupleEqual(r, FGS(point=6, box=1, xyz_point=0, length=4, cpd_length=0))

        r = emtm.em_measurement_count_fgs('*', '*', '*')
        self.assertTupleEqual(r, FGS(point=31, box=4, xyz_point=2, length=21, cpd_length=1))

        r = emtm.em_measurement_count_fgs('nemipteridae', '*', '*')
        self.assertTupleEqual(r, FGS(point=14, box=2, xyz_point=1, length=14, cpd_length=0))

        r = emtm.em_measurement_count_fgs('*', '*', 'furcosus')
        self.assertTupleEqual(r, FGS(point=6, box=0, xyz_point=1, length=4, cpd_length=0))

    def test_em_point_count(self):
        r = emtm.em_load_data(os.path.join(TEST_FILES_PATH, 'Test.EMObs'))

        r = emtm.em_point_count()
        PointCount = namedtuple('PointCount', 'total bbox')
        self.assertTupleEqual(r, PointCount(total=35, bbox=4))

    def test_em_get_point(self):
        r = emtm.em_load_data(os.path.join(TEST_FILES_PATH, 'Test.EMObs'))
        point_count = emtm.em_point_count()
        # print(point_count)
        p = emtm.em_get_point(0)  # just so we can get the fields

        em_point_values = []
        em_point_fields = [field[0] for field in p._fields_]
        # print(em_point_fields)

        for ii in range(point_count.total):
            em_point_values = []
            p = emtm.em_get_point(ii)
            for fields in em_point_fields:
                em_point_values.append(p.__getattribute__(fields))

            # print(em_point_values)  # just so we can get the fields

    def test_em_3d_point_count(self):
        r = emtm.em_load_data(os.path.join(TEST_FILES_PATH, 'Test.EMObs'))
        r = emtm.em_3d_point_count()
        self.assertEqual(r, 2)

    def test_em_get_3d_point(self):
        r = emtm.em_load_data(os.path.join(TEST_FILES_PATH, 'Test.EMObs'))
        point_count = emtm.em_3d_point_count()
        # print(point_count)
        p = emtm.em_get_3d_point(0)  # just so we can get the fields

        em_point_values = []
        em_point_fields = [field[0] for field in p._fields_]
        # print(em_point_fields)

        for ii in range(point_count):
            em_point_values = []
            p = emtm.em_get_3d_point(ii)
            for fields in em_point_fields:
                em_point_values.append(p.__getattribute__(fields))

            # print(em_point_values)

    def test_em_get_length_count(self):
        r = emtm.em_load_data(os.path.join(TEST_FILES_PATH, 'Test.EMObs'))

        pn_compound = emtm.em_get_length_count()
        LengthCount = namedtuple('LengthCount', 'total compound')

        self.assertTupleEqual(pn_compound, LengthCount(total=22, compound=0))

    def test_em_get_length(self):
        r = emtm.em_load_data(os.path.join(TEST_FILES_PATH, 'Test.EMObs'))
        length_count = emtm.em_get_length_count()
        length = emtm.em_get_length(0)

        em_length_values = []
        em_length_fields = [field[0] for field in length._fields_]
        # print(em_point_fields)

        for ii in range(length_count.total):
            # print(ii)
            em_length_values = []
            l = emtm.em_get_length(ii)
            for fields in em_length_fields:
                em_length_values.append(l.__getattribute__(fields))

            # print(em_length_values)

    def test_tm_load_data(self):
        r = emtm.tm_load_data(os.path.join(TEST_FILES_PATH, 'Test.TMObs'))
        self.assertIs(EMTMResult(r), EMTMResult(0))

    def test_tm_clear_data(self):
        r = emtm.tm_load_data(os.path.join(TEST_FILES_PATH, 'Test.TMObs'))
        emtm.tm_clear_data()

    def test_tm_point_count(self):
        r = emtm.tm_load_data(os.path.join(TEST_FILES_PATH, 'Test.TMObs'))
        r = emtm.tm_point_count()
        self.assertEqual(r, 10)

    def test_tm_get_point(self):
        r = emtm.tm_load_data(os.path.join(TEST_FILES_PATH, 'Test.TMObs'))
        point_count = emtm.tm_point_count()
        p = emtm.tm_get_point(0)

        tm_point_values = []
        tm_point_fields = [field[0] for field in p._fields_]
        # print(tm_point_fields)

        for ii in range(point_count):
            tm_point_values = []
            p = emtm.tm_get_point(ii)
            for fields in tm_point_fields:
                tm_point_values.append(p.__getattribute__(fields))

            # print(tm_point_values)

    def test_em_to_dataframe(self):
        emtm.em_load_data(os.path.join(TEST_FILES_PATH, 'Test.EMObs'))
        length_dataframe = emtm.em_to_dataframe(em_data_type='length')
        point_dataframe = emtm.em_to_dataframe(em_data_type='point')

        points_df = emtm.EmAnnotationDataFrames.load_points_from_current_em_file()
        points3d_df = emtm.EmAnnotationDataFrames.load_3d_points_from_current_em_file()
        lengths_df = emtm.EmAnnotationDataFrames.load_lengths_from_current_em_file()
        self.assertEqual(len(points_df), 35)
        self.assertEqual(len(points3d_df), 2)
        self.assertEqual(len(lengths_df), 22)

    def test_starting_with_empty_EmAnnotationDataFrames_object(self):
        emtm.em_load_data(os.path.join(os.path.join(TEST_FILES_PATH, 'Test.EMObs')))
        dfs = emtm.EmAnnotationDataFrames(None, None, None)
        self.assertIs(dfs.points, None)
        self.assertIs(dfs.points3d, None)
        self.assertIs(dfs.lengths, None)
        dfs.points = emtm.EmAnnotationDataFrames.load_points_from_current_em_file()
        self.assertEqual(len(dfs.points), 35)

    def test_starting_with_partially_empty_EmAnnotationDataFrames_object(self):
        emtm.em_load_data(os.path.join(os.path.join(TEST_FILES_PATH, 'Test.EMObs')))
        dfs = emtm.EmAnnotationDataFrames(points=None)
        self.assertIs(dfs.points, None)
        self.assertEqual(len(dfs.points3d), 2)
        self.assertEqual(len(dfs.lengths), 22)

        dfs = emtm.EmAnnotationDataFrames(points=None)
        self.assertIs(dfs.points, None)
        self.assertEqual(len(dfs.points3d), 2)
        self.assertEqual(len(dfs.lengths), 22)

    def test_em_to_dataframes(self):
        emtm.em_load_data(os.path.join(os.path.join(TEST_FILES_PATH, 'Test.EMObs')))
        dfs = emtm.EmAnnotationDataFrames()
        self.assertEqual(len(dfs.points), 35)
        self.assertEqual(len(dfs.points3d), 2)
        self.assertEqual(len(dfs.lengths), 22)

    def test_em_add_point(self):
        new_point = emtm.EmPointData(
            str_op_code=b"Test",
            str_filename=b"image.jpeg",
            n_frame=107,
            d_imx=456.7,
            d_imy=987.6,
            str_family=b'balistidae',
            str_genus=b'abalistes',
            str_species=b'stellatus'
        )
        r = emtm.em_add_point(new_point)
        self.assertEqual(r, emtm.EMTMResult.ok)

        point_count = emtm.em_point_count()[0]
        last_point = emtm.em_get_point(point_count - 1)
        self.assertEqual(
            *(
                (
                    point.str_op_code,
                    point.str_filename,
                    point.n_frame,
                    point.d_imx,
                    point.d_imy,
                    point.str_family,
                    point.str_genus,
                    point.str_species
                )
                for point in (new_point, last_point)
            )
        )

    def test_em_add_3d_point(self):
        new_point = emtm.Em3DPpointData(
            str_op_code=b"Test",
            str_filename_left=b"image_left.jpeg",
            str_filename_right=b"image_right.jpeg",
            n_frame_left=107,
            n_frame_right=112,
            d_imx_left=456.7,
            d_imy_left=987.6,
            d_imx_right=543.7,
            d_imy_right=864.1,
            str_family=b'balistidae',
            str_genus=b'abalistes',
            str_species=b'stellatus'
        )
        r = emtm.em_add_3d_point(new_point)
        self.assertEqual(r, emtm.EMTMResult.ok)

        point_count = emtm.em_3d_point_count()
        last_point = emtm.em_get_3d_point(point_count - 1)
        self.assertEqual(
            *(
                (
                    point.str_op_code,
                    point.str_filename_left,
                    point.str_filename_right,
                    point.n_frame_left,
                    point.n_frame_right,
                    point.d_imx_left,
                    point.d_imy_left,
                    point.d_imx_right,
                    point.d_imy_right,
                    point.str_family,
                    point.str_genus,
                    point.str_species
                )
                for point in (new_point, last_point)
            )
        )

    def test_em_add_length(self):
        new_length = emtm.EmLengthData(
            str_op_code=b"Test",
            str_filename_left=b"image_left.jpeg",
            str_filename_right=b"image_right.jpeg",
            n_frame_left=107,
            n_frame_right=112,
            d_imx1_left=456.7,
            d_imy1_left=987.6,
            d_imx2_left=553.1,
            d_imy2_left=843.2,
            d_imx1_right=543.7,
            d_imy1_right=864.1,
            d_imx2_right=673.7,
            d_imy2_right=794.1,
            str_family=b'balistidae',
            str_genus=b'abalistes',
            str_species=b'stellatus'
        )
        r = emtm.em_add_length(new_length)
        self.assertEqual(r, emtm.EMTMResult.ok)

        length_count = emtm.em_get_length_count()[0]
        last_length = emtm.em_get_length(length_count - 1)
        self.assertEqual(
            *(
                (
                    point.str_op_code,
                    point.str_filename_left,
                    point.str_filename_right,
                    point.n_frame_left,
                    point.n_frame_right,
                    point.d_imx1_left,
                    point.d_imy1_left,
                    point.d_imx2_left,
                    point.d_imy2_left,
                    point.d_imx1_right,
                    point.d_imy1_right,
                    point.d_imx2_right,
                    point.d_imy2_right,
                    point.str_family,
                    point.str_genus,
                    point.str_species
                )
                for point in (new_length, last_length)
            )
        )

    def test_em_write_data(self):
        # Clear the loaded data and add 1 of each type of annotation
        emtm.em_clear_data()

        r = emtm.em_add_point(
            emtm.EmPointData(
                str_op_code=b"Test",
                str_filename=b"image.jpeg",
                n_frame=107,
                d_imx=456.7,
                d_imy=987.6,
                str_family=b'balistidae',
                str_genus=b'abalistes',
                str_species=b'stellatus'
            )
        )
        self.assertEqual(r, emtm.EMTMResult.ok)

        r = emtm.em_add_3d_point(
            emtm.Em3DPpointData(
                str_op_code=b"Test",
                str_filename_left=b"image_left.jpeg",
                str_filename_right=b"image_right.jpeg",
                n_frame_left=107,
                n_frame_right=112,
                d_imx_left=456.7,
                d_imy_left=987.6,
                d_imx_right=543.7,
                d_imy_right=864.1,
                str_family=b'balistidae',
                str_genus=b'abalistes',
                str_species=b'stellatus'
            )
        )
        self.assertEqual(r, emtm.EMTMResult.ok)

        r = emtm.em_add_length(
            emtm.EmLengthData(
                str_op_code=b"Test",
                str_filename_left=b"image_left.jpeg",
                str_filename_right=b"image_right.jpeg",
                n_frame_left=107,
                n_frame_right=112,
                d_imx1_left=456.7,
                d_imy1_left=987.6,
                d_imx2_left=553.1,
                d_imy2_left=843.2,
                d_imx1_right=543.7,
                d_imy1_right=864.1,
                d_imx2_right=673.7,
                d_imy2_right=794.1,
                str_family=b'balistidae',
                str_genus=b'abalistes',
                str_species=b'stellatus'
            )
        )
        self.assertEqual(r, emtm.EMTMResult.ok)

        with tempfile.TemporaryDirectory() as tmpdir:
            # Write out the data we just added and then clear the library
            filename = Path(tmpdir) / "tmp.EMObs"
            emtm.em_write_data(str(filename))
            emtm.em_clear_data()

            # Assert nothing is still in memory
            self.assertEqual(emtm.em_get_length_count()[0], 0)
            self.assertEqual(emtm.em_3d_point_count(), 0)
            self.assertEqual(emtm.em_point_count()[0], 0)

            # Load the file we just created and assert the data is now in memory
            emtm.em_load_data(str(filename))

            self.assertEqual(emtm.em_get_length_count()[0], 1)
            self.assertEqual(emtm.em_3d_point_count(), 1)
            self.assertEqual(emtm.em_point_count()[0], 1)

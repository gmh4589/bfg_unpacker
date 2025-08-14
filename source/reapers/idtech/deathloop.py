import os
from icecream import ic

from source.reaper import Reaper, file_reaper
# from source.reapers.idtech.bimage import Bimage2DDS
# from source.codecs.zip_methods import ZipMethods
from source.ui import localize


class DeathLoop(Reaper):
    # For unpacking *.resource, *.index from DeathLoop
    # TODO: Add oodle support, add Bimage2DDS convert support
    #  Localize text, maybe add to resources.py

    @file_reaper
    def run(self):

        if not self.multi_vol():
            self.update_pb(0, 0, 'Операция прервана пользователем')
            return -1

        master_resources = self.file_name.replace(os.path.basename(self.file_name), 'master_resources.index')
        folder_name = os.path.dirname(self.file_name)

        if not os.path.exists(master_resources):
            print(f"{localize.error}! {localize.file} {master_resources} {localize.do_not_exist}")
            return -1

        with open(master_resources, 'rb') as mrf:
            magic = mrf.read(4)

            if not self.magic([b'SER', ], magic, 'DeathLoop'):
                return -1

            # data_size = int.from_bytes(mrf.read(4), 'big')
            # mrf.seek(0x18, 1)
            mrf.seek(0x1C, 1)
            file_count = int.from_bytes(mrf.read(4), 'big')
            open_archive = open(f"{folder_name}\\{archive_list[0]}", 'rb')

            for i in range(file_count):
                index = int.from_bytes(mrf.read(4), 'little')
                file_type_len1 = int.from_bytes(mrf.read(4), 'little')
                file_type1 = mrf.read(file_type_len1).decode('utf-8', errors='ignore')
                file_type_len2 = int.from_bytes(mrf.read(4), 'little')
                file_type2 = mrf.read(file_type_len2).decode('utf-8', errors='ignore')
                full_name_len = int.from_bytes(mrf.read(4), 'little')
                full_name = mrf.read(full_name_len).decode('utf-8', errors='ignore')
                offset = int.from_bytes(mrf.read(8), 'little')
                zip_size = int.from_bytes(mrf.read(4), 'little')
                unzip_size = int.from_bytes(mrf.read(4), 'little')
                mrf.seek(0xC, 1)
                archive_i = int.from_bytes(mrf.read(2), 'little')
                path = f"{self.output_folder}\\{full_name}"
                ic(index, file_type1, file_type2, zip_size)

                try:
                    if archive_list[archive_i] not in open_archive.name:
                        open_archive.close()
                        open_archive = open(f"{folder_name}\\{archive_list[archive_i]}", 'rb')
                except IndexError:
                    pass

                open_archive.seek(offset)
                data = open_archive.read(unzip_size)
                self.file_save(path, data)

                # if zip_size != unzip_size:
                #     self.unzip(path, ZipMethods.OODLE)

                self.update_pb(file_count, i, full_name)

            open_archive.close()


archive_list = [
    "rsc_decl_0.resources",
    "rsc_gen_0_0.resources",
    "rsc_gen_0_1.resources",
    "map_menu_0.resources",
    "map_antenna_01_p_0.resources",
    "map_antenna_02_p_0.resources",
    "map_antenna_03_p_0.resources",
    "map_antenna_04_p_0.resources",
    "map_island_01_p_0.resources",
    "map_island_02_p_0.resources",
    "map_island_03_p_0.resources",
    "map_outro_p_0.resources",
    "map_outro_02_0.resources",
    "map_tutorial_01_p_0.resources",
    "map_tutorial_02_0.resources",
    "map_upper_antenna_p_0.resources",
    "map_uppercity_01_p_0.resources",
    "map_uppercity_02_p_0.resources",
    "map_uppercity_03_p_0.resources",
    "map_uppercity_04_p_0.resources",
    "map_wharf_01_0.resources",
    "map_wharf_03_0.resources",
    "map_wharf_04_0.resources",
    "rsc_images_0_0.resources",
    "rsc_images_0_1.resources",
    "rsc_images_0_2.resources",
    "rsc_images_0_3.resources",
    "rsc_images_0_4.resources",
    "rsc_images_0_5.resources",
    "rsc_images_0_6.resources",
    "rsc_images_0_7.resources",
    "rsc_images_0_8.resources",
    "rsc_images_0_9.resources",
    "rsc_images_0_10.resources",
    "rsc_images_0_11.resources",
    "rsc_images_0_12.resources",
    "rsc_images_0_13.resources",
    "sfx/rsc_sounds_0_0.resources",
    "sfx/rsc_sounds_0_1.resources",
    "rsc_anims_0_0.resources",
    "rsc_ui_0_0.resources",
    "rsc_ui_0_1.resources",
    "rsc_ui_0_2.resources",
    "rsc_ui_0_3.resources",
    "rsc_ui_0_4.resources",
    "rsc_images_1_0.resources",
    "rsc_images_1_1.resources",
    "rsc_images_1_2.resources",
    "rsc_images_1_3.resources",
    "rsc_images_1_4.resources",
    "rsc_images_1_5.resources",
    "rsc_images_1_6.resources",
    "rsc_images_1_7.resources",
    "rsc_images_1_8.resources",
    "sfx/rsc_sounds_1_0.resources",
    "rsc_anims_1_0.resources",
    "rsc_images_2_0.resources",
    "rsc_images_2_1.resources",
    "sfx/rsc_sounds_2_0.resources",
    "rsc_anims_2_0.resources",
    "rsc_images_3_0.resources",
    "rsc_images_3_1.resources",
    "sfx/rsc_sounds_3_0.resources",
    "rsc_anims_3_0.resources",
    "rsc_images_4_0.resources",
    "sfx/rsc_sounds_4_0.resources",
    "rsc_anims_4_0.resources",
    "rsc_images_5_0.resources",
    "sfx/rsc_sounds_5_0.resources",
    "rsc_anims_5_0.resources",
    "rsc_images_6_0.resources",
    "sfx/rsc_sounds_6_0.resources",
    "rsc_anims_6_0.resources",
    "rsc_images_7_0.resources",
    "sfx/rsc_sounds_7_0.resources",
    "rsc_anims_7_0.resources",
    "rsc_images_8_0.resources",
    "sfx/rsc_sounds_8_0.resources",
    "rsc_anims_8_0.resources",
    "rsc_images_9_0.resources",
    "sfx/rsc_sounds_9_0.resources",
    "rsc_anims_9_0.resources",
    "rsc_images_10_0.resources",
    "sfx/rsc_sounds_10_0.resources",
    "rsc_anims_10_0.resources",
    "rsc_images_11_0.resources",
    "sfx/rsc_sounds_11_0.resources",
    "rsc_anims_11_0.resources",
    "rsc_images_12_0.resources",
    "sfx/rsc_sounds_12_0.resources",
    "rsc_anims_12_0.resources",
    "rsc_images_13_0.resources",
    "sfx/rsc_sounds_13_0.resources",
    "rsc_anims_13_0.resources",
    "rsc_images_14_0.resources",
    "sfx/rsc_sounds_14_0.resources",
    "rsc_anims_14_0.resources",
    "rsc_images_15_0.resources",
    "sfx/rsc_sounds_15_0.resources",
    "rsc_anims_15_0.resources",
    "eLID_English/rsc_sounds_16_0.resources",
    "eLID_French/rsc_sounds_17_0.resources",
    "eLID_Italian/rsc_sounds_18_0.resources",
    "eLID_German/rsc_sounds_19_0.resources",
    "eLID_Spanish/rsc_sounds_20_0.resources",
    "eLID_Russian/rsc_sounds_21_0.resources",
    "eLID_Polish/rsc_sounds_22_0.resources",
    "eLID_MexicanSpanish/rsc_sounds_23_0.resources",
    "eLID_BrazilianPortuguese/rsc_sounds_24_0.resources",
    "eLID_Japanese/rsc_sounds_26_0.resources",
]
